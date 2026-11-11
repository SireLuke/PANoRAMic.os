import type { LibrarySearchResult } from "./types";

export interface RedundancyReductionOptions {
  /** Relevance weight in MMR; 1 selects by relevance only, 0 maximizes novelty. */
  lambda?: number;
  /** Maximum number of results to return. */
  maxResults?: number;
}

export interface RedundancySelectionStep {
  nodeId: string;
  relevance: number;
  maxRedundancy: number;
  mmrScore: number;
}

export interface RedundancySelectionResult {
  results: LibrarySearchResult[];
  trace: RedundancySelectionStep[];
}

function tokenize(text: string): string[] {
  return (text.toLocaleLowerCase().match(/[\p{L}\p{N}]+/gu) ?? []);
}

/** Unigram + adjacent-bigram Jaccard features; deterministic and dependency-free. */
function lexicalFeatures(text: string): Set<string> {
  const words = tokenize(text);
  const features = new Set<string>();
  for (let i = 0; i < words.length; i++) {
    features.add(`w:${words[i]}`);
    if (i > 0) features.add(`b:${words[i - 1]} ${words[i]}`);
  }
  return features;
}

function jaccardSimilarity(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 || b.size === 0) return 0;
  let intersection = 0;
  for (const feature of a) if (b.has(feature)) intersection++;
  const union = a.size + b.size - intersection;
  return union === 0 ? 0 : intersection / union;
}

/**
 * Greedy maximal-marginal-relevance selection over existing Library search results.
 *
 * MMR(d) = lambda * relevance(d)
 *          - (1 - lambda) * max_similarity(d, already_selected)
 *
 * Similarity is lexical Jaccard over unigrams and adjacent bigrams. This is an
 * explainable baseline, not a semantic embedding model. The input array and
 * result objects are never mutated; ties retain original search order.
 */
export function selectRedundancyReducedResults(
  results: LibrarySearchResult[],
  contentByNodeId: ReadonlyMap<string, string>,
  options: RedundancyReductionOptions = {}
): RedundancySelectionResult {
  const lambda = options.lambda ?? 0.6;
  const maxResults = options.maxResults ?? results.length;

  if (!Number.isFinite(lambda) || lambda < 0 || lambda > 1) {
    throw new RangeError("lambda must be a finite number in [0, 1]");
  }
  if (!Number.isInteger(maxResults) || maxResults < 0) {
    throw new RangeError("maxResults must be a non-negative integer");
  }

  const candidates = results.map((result, index) => ({
    result,
    index,
    relevance: Number.isFinite(result.relevanceScore)
      ? Math.max(0, Math.min(1, result.relevanceScore))
      : 0,
    features: lexicalFeatures(
      `${result.title} ${contentByNodeId.get(result.nodeId) ?? result.snippet}`
    ),
  }));

  const selected: typeof candidates = [];
  const remaining = candidates.slice();
  const trace: RedundancySelectionStep[] = [];

  while (remaining.length > 0 && selected.length < maxResults) {
    let bestPosition = 0;
    let bestScore = Number.NEGATIVE_INFINITY;
    let bestRedundancy = 0;

    for (let position = 0; position < remaining.length; position++) {
      const candidate = remaining[position];
      let maxRedundancy = 0;
      for (const chosen of selected) {
        maxRedundancy = Math.max(
          maxRedundancy,
          jaccardSimilarity(candidate.features, chosen.features)
        );
      }
      const score =
        lambda * candidate.relevance - (1 - lambda) * maxRedundancy;

      // Strict comparison preserves original order for exact ties.
      if (score > bestScore) {
        bestPosition = position;
        bestScore = score;
        bestRedundancy = maxRedundancy;
      }
    }

    const [chosen] = remaining.splice(bestPosition, 1);
    selected.push(chosen);
    trace.push({
      nodeId: chosen.result.nodeId,
      relevance: chosen.relevance,
      maxRedundancy: bestRedundancy,
      mmrScore: bestScore,
    });
  }

  return {
    results: selected.map((item) => item.result),
    trace,
  };
}
