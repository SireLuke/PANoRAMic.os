/**
 * Library of Alexandria
 * Planetary Memory Layer with Micro LLM Integration
 */

import {
  LibraryNode,
  LibraryQuery,
  LibrarySearchResult,
  LibrarySnapshot,
  CultureEmbedding,
  NuanceParameters,
} from "./types";
import { MicroLLMEncoder } from "./microLLM";

export class LibraryOfAlexandria {
  private nodes: Map<string, LibraryNode> = new Map();
  private encoder: MicroLLMEncoder;
  private indexedAt = 0;

  constructor() {
    this.encoder = new MicroLLMEncoder();
  }

  addNode(
    id: string,
    category: LibraryNode["category"],
    title: string,
    content: string,
    culture: CultureEmbedding,
    nuance: NuanceParameters,
    trustWeight: number = 0.7,
    tags: string[] = []
  ): LibraryNode {
    const node: LibraryNode = {
      id,
      category,
      title,
      content,
      timestamp: Date.now(),
      trustWeight,
      cultureEmbedding: culture,
      nuanceParameters: nuance,
      tags,
      provenance: {
        source: culture.origin,
        verificationMethod: "community",
        dateAcquired: Date.now(),
        lastVerified: Date.now(),
        verificationChain: [],
        challengeCount: 0,
      },
    };

    this.nodes.set(id, node);
    this.indexedAt = Date.now();
    return node;
  }

  search(query: LibraryQuery): LibrarySearchResult[] {
    const results: LibrarySearchResult[] = [];

    for (const [nodeId, node] of this.nodes) {
      if (query.trustThreshold && node.trustWeight < query.trustThreshold) continue;

      const relevanceScore = this.computeRelevance(query.query, node.content);
      if (relevanceScore < 0.1) continue;

      let culturalAlignment = 0.5;
      if (query.culturalContext) {
        culturalAlignment = this.computeCulturalAlignment(query.culturalContext, node.cultureEmbedding);
      }

      let nuanceAlignment = 0.5;
      if (query.nuancePreferences) {
        nuanceAlignment = this.computeNuanceAlignment(query.nuancePreferences, node.nuanceParameters);
      }

      const finalScore =
        relevanceScore * 0.5 + culturalAlignment * 0.25 + nuanceAlignment * 0.25;

      results.push({
        nodeId,
        title: node.title,
        relevanceScore: finalScore,
        culturalAlignment,
        nuanceAlignment,
        snippet: node.content.substring(0, 150) + "...",
        metadata: {
          category: node.category,
          origin: node.cultureEmbedding.origin,
          languages: node.cultureEmbedding.languages,
        },
      });
    }

    return results.sort((a, b) => b.relevanceScore - a.relevanceScore);
  }

  private computeRelevance(query: string, content: string): number {
    const terms = query.toLowerCase().split(/\s+/);
    const lower = content.toLowerCase();

    let matches = 0;
    terms.forEach((t) => {
      if (lower.includes(t)) matches++;
    });

    return Math.min(1.0, matches / terms.length);
  }

  private computeCulturalAlignment(context: string, culture: CultureEmbedding): number {
    if (culture.origin.toLowerCase().includes(context.toLowerCase())) return 0.9;
    if (culture.languages.some((l) => l.toLowerCase().includes(context.toLowerCase()))) return 0.8;
    return 0.5;
  }

  private computeNuanceAlignment(
    prefs: Partial<NuanceParameters>,
    nuance: NuanceParameters
  ): number {
    let score = 0;
    let count = 0;

    if (prefs.abstractionLevel !== undefined) {
      score += Math.max(0, 1 - Math.abs(prefs.abstractionLevel - nuance.abstractionLevel));
      count++;
    }
    if (prefs.systemicDepth !== undefined) {
      score += Math.max(0, 1 - Math.abs(prefs.systemicDepth - nuance.systemicDepth));
      count++;
    }
    if (prefs.applicabilityRadius !== undefined) {
      score += Math.max(0, 1 - Math.abs(prefs.applicabilityRadius - nuance.applicabilityRadius));
      count++;
    }
    if (prefs.relevanceToPAN !== undefined) {
      score += Math.max(0, 1 - Math.abs(prefs.relevanceToPAN - nuance.relevanceToPAN));
      count++;
    }

    return count > 0 ? score / count : 0.5;
  }

  getSnapshot(): LibrarySnapshot {
    const categories = new Set<string>();
    const cultures = new Set<string>();
    const languages = new Set<string>();
    const trustWeights: { [key: string]: number } = {};

    for (const node of this.nodes.values()) {
      categories.add(node.category);
      cultures.add(node.cultureEmbedding.origin);
      node.cultureEmbedding.languages.forEach((l) => languages.add(l));

      const bucket = Math.floor(node.trustWeight * 10) / 10;
      trustWeights[bucket.toFixed(1)] = (trustWeights[bucket.toFixed(1)] || 0) + 1;
    }

    return {
      totalNodes: this.nodes.size,
      categoriesRepresented: Array.from(categories),
      culturesRepresented: Array.from(cultures),
      languagesSupported: Array.from(languages),
      lastIndexedAt: this.indexedAt,
      trustWeightDistribution: trustWeights,
    };
  }

  getNode(id: string): LibraryNode | undefined {
    return this.nodes.get(id);
  }

  getByCategory(category: LibraryNode["category"]): LibraryNode[] {
    return Array.from(this.nodes.values()).filter((n) => n.category === category);
  }
}

export const libraryOfAlexandria = new LibraryOfAlexandria();
