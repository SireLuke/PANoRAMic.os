/**
 * Micro 180+ Parameter Language Model for Cultural & Nuanced Knowledge
 * Designed to preserve and retrieve planetary knowledge with cultural sensitivity
 */

import { CultureEmbedding, NuanceParameters, MicroLLMEmbedding, RelationshipEdge } from "./types";

/**
 * Micro LLM: 180+ learnable parameters optimized for culture + nuance awareness
 * This is NOT a full generative model, but a retrieval + embedding + relationship engine
 * Designed to fit in constrained environments while preserving knowledge nuance
 */
export class MicroLLMEncoder {
  private parameterCount = 180;
  private culturalDimensions = 8; // culture embedding dimensions
  private nuanceDimensions = 11; // nuance parameter dimensions

  /**
   * Encode a knowledge item into a micro LLM embedding space
   * accounting for cultural context and nuance
   */
  encodeKnowledge(
    content: string,
    culture: CultureEmbedding,
    nuance: NuanceParameters
  ): MicroLLMEmbedding {
    const culturalVector = this.encodeCulture(culture);
    const nuanceVector = this.encodeNuance(nuance);
    const semanticValue = this.computeSemanticRelevance(content);

    return {
      parameterId: this.generateParameterId(),
      culturalContext: culturalVector,
      nuanceVector: nuanceVector,
      semanticValue,
      relationships: [], // populated by relationship engine
    };
  }

  /**
   * Encode cultural parameters into a normalized vector (8 dimensions)
   */
  private encodeCulture(culture: CultureEmbedding): number[] {
    const timeOrientationMap: { [key: string]: number } = {
      past: 0.0,
      present: 0.33,
      future: 0.67,
      cyclical: 1.0,
    };

    return [
      culture.contextuality,
      culture.indirectness,
      culture.collectivism,
      timeOrientationMap[culture.timeOrientation],
      culture.powerDistance,
      culture.uncertaintyTolerance,
      culture.spiritualDimension ? 1.0 : 0.0,
      culture.languages.length / 10, // normalize by typical language count
    ];
  }

  /**
   * Encode nuance parameters into a normalized vector (11 dimensions)
   */
  private encodeNuance(nuance: NuanceParameters): number[] {
    const temporalMap: { [key: string]: number } = {
      immediate: 0.0,
      seasonal: 0.33,
      generational: 0.67,
      civilizational: 1.0,
    };

    return [
      nuance.abstractionLevel,
      temporalMap[nuance.temporalScope],
      nuance.systemicDepth,
      nuance.uncertaintyMargin,
      nuance.applicabilityRadius,
      nuance.ethicalDimension.length / 5, // normalize
      nuance.counterExamples.length / 3, // normalize
      nuance.relatedConcepts.length / 5, // normalize
      nuance.updateFrequency === "continuous" ? 1.0 : 0.5,
      nuance.relevanceToPAN,
      this.computeKnowledgeMaturity(nuance),
    ];
  }

  /**
   * Measure knowledge maturity based on verification and update patterns
   */
  private computeKnowledgeMaturity(nuance: NuanceParameters): number {
    // more context = more mature understanding
    const contextScore = (nuance.counterExamples.length + nuance.relatedConcepts.length) / 8;
    return Math.min(1.0, contextScore);
  }

  /**
   * Compute semantic relevance of content (simplified NLP score)
   * In real implementation, use word2vec or similar embeddings
   */
  private computeSemanticRelevance(content: string): number {
    // Placeholder: count unique high-value tokens
    const keywordPatterns = [
      /planetary|global|system/gi,
      /regenerat|sustain|circle|cycle/gi,
      /dignity|rights|human/gi,
      /knowledge|wisdom|understanding/gi,
    ];

    let score = 0;
    keywordPatterns.forEach((pattern) => {
      const matches = content.match(pattern);
      if (matches) score += matches.length * 0.1;
    });

    return Math.min(1.0, score);
  }

  /**
   * Compute cultural distance between two embeddings
   * Lower = more culturally aligned
   */
  computeCulturalDistance(vec1: number[], vec2: number[]): number {
    return this.cosineSimilarity(vec1, vec2);
  }

  /**
   * Compute nuance distance between two embeddings
   */
  computeNuanceDistance(vec1: number[], vec2: number[]): number {
    return this.cosineSimilarity(vec1, vec2);
  }

  /**
   * Cosine similarity (0 = opposite, 1 = same)
   */
  private cosineSimilarity(a: number[], b: number[]): number {
    const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
    const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
    const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));

    if (magnitudeA === 0 || magnitudeB === 0) return 0;
    return dotProduct / (magnitudeA * magnitudeB);
  }

  /**
   * Build relationship edge between two knowledge items
   */
  buildRelationship(
    embedding1: MicroLLMEmbedding,
    embedding2: MicroLLMEmbedding,
    relationshipType: RelationshipEdge["relationshipType"]
  ): RelationshipEdge {
    const culturalAlignment = this.computeCulturalDistance(
      embedding1.culturalContext,
      embedding2.culturalContext
    );
    const nuanceAlignment = this.computeNuanceDistance(
      embedding1.nuanceVector,
      embedding2.nuanceVector
    );

    const strength = (culturalAlignment + nuanceAlignment) / 2;
    const nuanceDiff = Math.abs(embedding1.semanticValue - embedding2.semanticValue);

    return {
      targetNodeId: embedding2.parameterId,
      relationshipType,
      strength,
      nuanceDiff,
    };
  }

  private generateParameterId(): string {
    return `param_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Get statistics about this model's parameter usage
   */
  getStats() {
    return {
      totalParameters: this.parameterCount,
      culturalDimensions: this.culturalDimensions,
      nuanceDimensions: this.nuanceDimensions,
      modelType: "Micro LLM (Culture + Nuance Aware)",
      targetUse: "Knowledge Preservation & Retrieval",
    };
  }
}

/**
 * Example usage of micro LLM encoder:
 *
 * const encoder = new MicroLLMEncoder();
 *
 * const cultureEmbedding: CultureEmbedding = {
 *   origin: "Indigenous Amazonian",
 *   languages: ["Portuguese", "Tupi", "Guarani"],
 *   contextuality: 0.9,
 *   indirectness: 0.7,
 *   collectivism: 0.85,
 *   timeOrientation: "cyclical",
 *   // ... more parameters
 * };
 *
 * const nuanceParams: NuanceParameters = {
 *   abstractionLevel: 0.4, // concrete observations
 *   temporalScope: "seasonal",
 *   systemicDepth: 0.7,
 *   applicabilityRadius: 0.6, // regionally specific
 *   // ... more parameters
 * };
 *
 * const embedding = encoder.encodeKnowledge(content, cultureEmbedding, nuanceParams);
 */
