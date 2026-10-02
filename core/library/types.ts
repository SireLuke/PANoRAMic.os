/**
 * Library of Alexandria Types & Interfaces
 * Planetary memory layer with cultural and nuance-aware micro LLM
 */

export interface LibraryNode {
  id: string;
  category: "knowledge" | "engineering" | "ecological" | "humanitarian" | "cultural" | "infrastructure" | "audit";
  title: string;
  content: string;
  timestamp: number;
  trustWeight: number; // 0..1
  cultureEmbedding: CultureEmbedding;
  nuanceParameters: NuanceParameters;
  tags: string[];
  provenance: ProvenanceRecord;
}

export interface CultureEmbedding {
  origin: string;
  languages: string[];
  contextuality: number;
  indirectness: number;
  collectivism: number;
  timeOrientation: "past" | "present" | "future" | "cyclical";
  powerDistance: number;
  uncertaintyTolerance: number;
  spiritualDimension: boolean;
  iconography: string[];
}

export interface NuanceParameters {
  abstractionLevel: number;
  temporalScope: "immediate" | "seasonal" | "generational" | "civilizational";
  systemicDepth: number;
  uncertaintyMargin: number;
  applicabilityRadius: number;
  ethicalDimension: string[];
  counterExamples: string[];
  relatedConcepts: string[];
  updateFrequency: "static" | "seasonal" | "annual" | "continuous";
  relevanceToPAN: number;
}

export interface ProvenanceRecord {
  source: string;
  verificationMethod: "academic" | "indigenous" | "field-tested" | "community" | "synthesis";
  dateAcquired: number;
  lastVerified: number;
  verificationChain: string[];
  challengeCount: number;
}

export interface MicroLLMEmbedding {
  parameterId: string;
  culturalContext: number[];
  nuanceVector: number[];
  semanticValue: number;
  relationships: RelationshipEdge[];
}

export interface RelationshipEdge {
  targetNodeId: string;
  relationshipType: "contradicts" | "extends" | "supports" | "precedes" | "follows" | "culturalVariant";
  strength: number;
  nuanceDiff: number;
}

export interface LibraryQuery {
  query: string;
  culturalContext?: string;
  preferLanguage?: string;
  nuancePreferences?: Partial<NuanceParameters>;
  trustThreshold?: number;
}

export interface LibrarySearchResult {
  nodeId: string;
  title: string;
  relevanceScore: number;
  culturalAlignment: number;
  nuanceAlignment: number;
  snippet: string;
  metadata: {
    category: string;
    origin: string;
    languages: string[];
  };
}

export interface LibrarySnapshot {
  totalNodes: number;
  categoriesRepresented: string[];
  culturesRepresented: string[];
  languagesSupported: string[];
  lastIndexedAt: number;
  trustWeightDistribution: { [key: string]: number };
}

