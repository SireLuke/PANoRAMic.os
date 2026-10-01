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
  origin: string; // geographic or cultural origin
  languages: string[]; // multilingual support
  contextuality: number; // 0-1: how context-dependent is this knowledge?
  indirectness: number; // 0-1: directness vs. polite/indirect communication
  collectivism: number; // 0-1: individual vs. group-oriented
  timeOrientation: "past" | "present" | "future" | "cyclical";
  powerDistance: number; // 0-1: acceptance of hierarchy
  uncertaintyTolerance: number; // 0-1: tolerance for ambiguity
  spiritualDimension: boolean; // sacred/spiritual knowledge included?
  iconography: string[]; // symbolic representations
}

export interface NuanceParameters {
  abstractionLevel: number; // 0-1: concrete vs. abstract
  temporalScope: "immediate" | "seasonal" | "generational" | "civilizational";
  systemicDepth: number; // 0-1: surface observation vs. deep systemic understanding
  uncertaintyMargin: number; // 0-1: confidence in the knowledge
  applicabilityRadius: number; // 0-1: universally applicable vs. locally specific
  ethicalDimension: string[]; // ethical considerations
  counterExamples: string[]; // when this knowledge breaks down
  relatedConcepts: string[]; // cross-reference to other knowledge
  updateFrequency: "static" | "seasonal" | "annual" | "continuous";
  relevanceToPAN: number; // 0-1: importance to planetary operations
}

export interface ProvenanceRecord {
  source: string;
  verificationMethod: "academic" | "indigenous" | "field-tested" | "community" | "synthesis";
  dateAcquired: number;
  lastVerified: number;
  verificationChain: string[]; // audit trail
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
  strength: number; // 0-1
  nuanceDiff: number; // how much the target nuance differs
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
  relevanceScore: number; // 0-1
  culturalAlignment: number; // 0-1
  nuanceAlignment: number; // 0-1
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
