/**
 * Library of Alexandria
 * Planetary Memory Layer with Micro LLM Integration
 *
 * Preserves and retrieves knowledge with cultural sensitivity and nuance awareness
 */

import { LibraryNode, LibraryQuery, LibrarySearchResult, LibrarySnapshot, CultureEmbedding, NuanceParameters } from "./types";
import { MicroLLMEncoder } from "./microLLM";

export class LibraryOfAlexandria {
  private nodes: Map<string, LibraryNode> = new Map();
  private encoder: MicroLLMEncoder;
  private indexedAt: number = 0;

  constructor() {
    this.encoder = new MicroLLMEncoder();
  }

  /**
   * Add a knowledge node to the library
   */
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

  /**
   * Search the library for knowledge matching query + cultural/nuance preferences
   */
  search(query: LibraryQuery): LibrarySearchResult[] {
    const results: LibrarySearchResult[] = [];

    for (const [nodeId, node] of this.nodes) {
      // Filter by trust threshold
      if (query.trustThreshold && node.trustWeight < query.trustThreshold) {
        continue;
      }

      // Calculate relevance score based on keyword matching
      const relevanceScore = this.computeRelevance(query.query, node.content);
      if (relevanceScore < 0.1) continue;

      // Calculate cultural alignment
      let culturalAlignment = 0.5; // neutral default
      if (query.culturalContext) {
        culturalAlignment = this.computeCulturalAlignment(query.culturalContext, node.cultureEmbedding);
      }

      // Calculate nuance alignment
      let nuanceAlignment = 0.5; // neutral default
      if (query.nuancePreferences) {
        nuanceAlignment = this.computeNuanceAlignment(query.nuancePreferences, node.nuanceParameters);
      }

      const finalScore = relevanceScore * 0.5 + culturalAlignment * 0.25 + nuanceAlignment * 0.25;

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

    // Sort by final score descending
    return results.sort((a, b) => b.relevanceScore - a.relevanceScore);
  }

  /**
   * Compute keyword relevance (simplified)
   */
  private computeRelevance(query: string, content: string): number {
    const queryTerms = query.toLowerCase().split(/\s+/);
    const contentLower = content.toLowerCase();

    let matches = 0;
    queryTerms.forEach((term) => {
      if (contentLower.includes(term)) matches++;
    });

    return Math.min(1.0, matches / queryTerms.length);
  }

  /**
   * Compute cultural alignment between query context and node culture
   */
  private computeCulturalAlignment(context: string, culture: CultureEmbedding): number {
    // Simplified: check if context matches origin or languages
    if (culture.origin.toLowerCase().includes(context.toLowerCase())) {
      return 0.9;
    }
    if (culture.languages.some((lang) => lang.toLowerCase().includes(context.toLowerCase()))) {
      return 0.8;
    }
    return 0.5; // neutral
  }

  /**
   * Compute nuance alignment between query preferences and node nuance parameters
   */
  private computeNuanceAlignment(prefs: Partial<NuanceParameters>, nuance: NuanceParameters): number {
    let alignmentScore = 0;
    let paramCount = 0;

    if (prefs.abstractionLevel !== undefined) {
      alignmentScore += Math.max(0, 1 - Math.abs(prefs.abstractionLevel - nuance.abstractionLevel));
      paramCount++;
    }
    if (prefs.systemicDepth !== undefined) {
      alignmentScore += Math.max(0, 1 - Math.abs(prefs.systemicDepth - nuance.systemicDepth));
      paramCount++;
    }
    if (prefs.applicabilityRadius !== undefined) {
      alignmentScore += Math.max(0, 1 - Math.abs(prefs.applicabilityRadius - nuance.applicabilityRadius));
      paramCount++;
    }
    if (prefs.relevanceToPAN !== undefined) {
      alignmentScore += Math.max(0, 1 - Math.abs(prefs.relevanceToPAN - nuance.relevanceToPAN));
      paramCount++;
    }

    return paramCount > 0 ? alignmentScore / paramCount : 0.5;
  }

  /**
   * Get a snapshot of the library's current state
   */
  getSnapshot(): LibrarySnapshot {
    const categories = new Set<string>();
    const cultures = new Set<string>();
    const languages = new Set<string>();
    const trustWeights: { [key: string]: number } = {};

    for (const node of this.nodes.values()) {
      categories.add(node.category);
      cultures.add(node.cultureEmbedding.origin);
      node.cultureEmbedding.languages.forEach((lang) => languages.add(lang));

      const trustBucket = Math.floor(node.trustWeight * 10) / 10;
      trustWeights[trustBucket.toFixed(1)] = (trustWeights[trustBucket.toFixed(1)] || 0) + 1;
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

  /**
   * Get a specific node by ID
   */
  getNode(id: string): LibraryNode | undefined {
    return this.nodes.get(id);
  }

  /**
   * List all nodes in a category
   */
  getByCategory(category: LibraryNode["category"]): LibraryNode[] {
    return Array.from(this.nodes.values()).filter((node) => node.category === category);
  }
}

export const libraryOfAlexandria = new LibraryOfAlexandria();
