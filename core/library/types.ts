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


// ---------------------------------------------------------------------------
// Matter layer (declared v0). Additive: nothing above this line changed.
//
// Ownership: the V8 coordinate schema is owned by pan-fractal-kernel. These types only
// MIRROR it so the Library can carry V8 states; if they disagree, the kernel wins.
// A MatterNode does not extend LibraryNode on purpose: cultural and nuance fields would
// have to be invented for an element. It links to a LibraryNode by id instead.
// Nothing here is a physical claim: V8 states of elements are a declared hypothesis.
// ---------------------------------------------------------------------------

export type V8Coordinate = "h" | "R" | "u" | "d" | "tau" | "chi" | "s" | "f";

/** chi in [-1, 1], all others in [0, 1]. null = unassigned or no source value (never 0 as a stand-in). */
export type V8State = { [K in V8Coordinate]: number | null };

export type MatterKind = "element" | "molecule" | "ion";

export type MatterClaimLevel = "declared-hypothesis" | "canonical";

export interface V8MappingRef {
  id: string; // e.g. "matter-element-v8-map"
  version: string; // e.g. "v0"
  claimLevel: MatterClaimLevel;
  schemaOwner: "pan-fractal-kernel";
  /** Declared source of each channel, in words; "unassigned" where none. */
  channelSources: { [K in V8Coordinate]: string };
  researchNote: string; // repo path of the note describing the map and its test
}

export interface MatterSource {
  id: string;
  file: string; // repo path
  sha256: string | null;
  origin: string; // as stated by whoever supplied it
  verified: boolean; // false until checked against a primary source
}

export interface MatterMeasuredValue {
  name: string;
  value: number | null;
  unit: string | null;
  unitVerified: boolean;
  sourceId: string;
}

export interface GridPlacement {
  row: number; // 1..9 (rows 8 and 9 are the f-block rows)
  col: number; // 1..18
  period: number;
  group: number | null; // null in the f-block
  block: "s" | "p" | "d" | "f";
}

export interface ElementData {
  atomicNumber: number;
  symbol: string;
  name: string;
  grid: GridPlacement;
}

export interface MoleculeData {
  formula: string;
  smiles: string | null;
  charge: number;
  bondName: string;
  bondLengthAngstrom: number;
  angleName: string | null;
  bondAngleDegrees: number | null;
  sourceId: string;
}

export type MatterViewKind = "grid" | "orbitals" | "nucleus" | "molecule";

export interface MatterView {
  kind: MatterViewKind;
  status: "available" | "planned";
  ref: string | null; // repo path of the data behind an available view
}

export interface MatterNode {
  id: string; // "matter:element:H", "matter:molecule:H2O", "matter:ion:H3+"
  kind: MatterKind;
  title: string;
  libraryNodeId: string | null; // LibraryNode carrying culture/nuance, if one exists
  element: ElementData | null;
  molecule: MoleculeData | null;
  v8: V8State;
  v8Mapping: V8MappingRef | null; // null when no map is declared for this kind
  measured: MatterMeasuredValue[];
  views: MatterView[];
  sourceIds: string[];
  claimLevel: MatterClaimLevel;
}

export interface MatterCatalog {
  schema: string;
  sources: MatterSource[];
  nodes: MatterNode[];
}
