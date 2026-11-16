/**
 * Bridge between an ArchiveSource and the Library of Alexandria.
 *
 * - findInArchive: title suggestions plus full-text hits, merged and de-duplicated.
 * - promoteToNode: copies one article into the library as a LibraryNode. The caller must supply
 *   the culture and nuance fields; they are never inferred from the text.
 *
 * The library is taken as a structural NodeSink so this file does not import the library module.
 */
import type { CultureEmbedding, LibraryNode, NuanceParameters } from "../types";
import { ArchiveArticle, ArchiveError, ArchiveHit, ArchiveSource } from "./types";

export interface NodeSink {
  addNode(
    id: string,
    category: LibraryNode["category"],
    title: string,
    content: string,
    culture: CultureEmbedding,
    nuance: NuanceParameters,
    trustWeight?: number,
    tags?: string[],
  ): LibraryNode;
}

/**
 * Neutral default trust for archive text. It is a placeholder, not an assessment of the source:
 * nobody has verified these articles against a primary source.
 */
export const ARCHIVE_DEFAULT_TRUST = 0.5;

export async function findInArchive(
  source: ArchiveSource,
  book: string,
  query: string,
  limit = 10,
): Promise<ArchiveHit[]> {
  const [titles, fullText] = await Promise.allSettled([
    source.suggest(book, query, limit),
    source.search(book, query, limit),
  ]);
  if (titles.status === "rejected" && fullText.status === "rejected") throw titles.reason;

  const merged = new Map<string, ArchiveHit>();
  if (titles.status === "fulfilled") for (const h of titles.value) merged.set(h.id, h);
  if (fullText.status === "fulfilled") {
    for (const h of fullText.value) {
      const prior = merged.get(h.id);
      if (!prior) merged.set(h.id, h);
      else if (prior.snippet === "" && h.snippet !== "") merged.set(h.id, { ...prior, snippet: h.snippet });
    }
  }
  return Array.from(merged.values()).slice(0, limit);
}

export interface PromoteOptions {
  id?: string;
  category?: LibraryNode["category"];
  trustWeight?: number;
  tags?: string[];
}

export function promoteToNode(
  library: NodeSink,
  article: ArchiveArticle,
  culture: CultureEmbedding,
  nuance: NuanceParameters,
  options: PromoteOptions = {},
): LibraryNode {
  if (!culture || typeof culture !== "object") throw new ArchiveError("culture must be supplied by the caller");
  if (!nuance || typeof nuance !== "object") throw new ArchiveError("nuance must be supplied by the caller");
  const trust = options.trustWeight ?? ARCHIVE_DEFAULT_TRUST;
  if (!Number.isFinite(trust) || trust < 0 || trust > 1) throw new ArchiveError("trustWeight must be in [0, 1]");
  if (article.text === "") throw new ArchiveError("refusing to promote an empty article");

  const node = library.addNode(
    options.id ?? article.id,
    options.category ?? "knowledge",
    article.title ?? article.path,
    article.text,
    culture,
    nuance,
    trust,
    options.tags ?? ["archive", article.book],
  );
  node.provenance.source = article.id;
  node.provenance.verificationMethod = "community";
  node.provenance.verificationChain = [];
  return node;
}
