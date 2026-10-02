/**
 * Micro 180+ Parameter Language Model for Cultural & Nuanced Knowledge
 * Designed to preserve and retrieve planetary knowledge with cultural sensitivity
 */

import { CultureEmbedding, NuanceParameters, MicroLLMEmbedding, RelationshipEdge } from "./types";

export class MicroLLMEncoder {
  private parameterCount = 180;
  private culturalDimensions = 8;
  private nuanceDimensions = 11;

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
      nuanceVector,
      semanticValue,
      relationships: [],
    };
  }

  private encodeCulture(culture: CultureEmbedding): number[] {
    const timeOrientationMap = {
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
      culture.languages.length / 10,
    ];
  }

  private encodeNuance(nuance: NuanceParameters): number[] {
    const temporalMap = {
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
      nuance.ethicalDimension.length / 5,
      nuance.counterExamples.length / 3,
      nuance.relatedConcepts.length / 5,
      nuance.updateFrequency === "continuous" ? 1.0 : 0.5,
      nuance.relevanceToPAN,
      this.computeKnowledgeMaturity(nuance),
    ];
  }

  private computeKnowledgeMaturity(nuance: NuanceParameters): number {
    const contextScore = (nuance.counterExamples.length + nuance.relatedConcepts.length) / 8;
    return Math.min(1.0, contextScore);
  }

  private computeSemanticRelevance(content: string): number {
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

  computeCulturalDistance(vec1: number[], vec2: number[]): number {
    return this.cosineSimilarity(vec1, vec2);
  }

  computeNuanceDistance(vec1: number[], vec2: number[]): number {
    return this.cosineSimilarity(vec1, vec2);
  }

  private cosineSimilarity(a: number[], b: number[]): number {
    const dot = a.reduce((sum, val, i) => sum + val * b[i], 0);
    const magA = Math.sqrt(a.reduce((s, v) => s + v * v, 0));
    const magB = Math.sqrt(b.reduce((s, v) => s + v * v, 0));
    if (magA === 0 || magB === 0) return 0;
    return dot / (magA * magB);
  }

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
