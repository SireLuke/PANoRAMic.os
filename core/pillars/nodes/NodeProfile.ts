// core/pillars/nodes/NodeProfile.ts

export type NodeType =
  | "city"
  | "region"
  | "biome"
  | "infrastructure_cluster"
  | "workforce_cluster"
  | "supply_chain_hub"
  | "planetary_subsystem"
  | "orbital_station"
  | "starship_habitat"

// Core definition for any node in PANoRAMic.OS
export interface NodeProfile {
  id: string
  name: string
  nodeType: NodeType

  // Core metrics (0–1)
  stabilityIndex: number
  riskIndex: number
  loadIndex: number
  resilienceIndex: number

  // Dependency metrics (0–1)
  ecologicalDependencyIndex: number
  infrastructureDependencyIndex: number
  economicDependencyIndex: number

  // Collapse metrics (0–1)
  collapseRiskIndex: number

  // Node graph connections
  connections: string[]

  // Optional metadata for planetary-scale nodes
  metadata?: {
    population?: number
    energyOutput?: number
    resourceLoad?: number
    strategicValue?: number
  }
}

// Utility: clamp values to 0–1
export function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value))
}

// Validate a node profile
export function validateNodeProfile(node: NodeProfile) {
  return {
    id: node.id,
    name: node.name,
    nodeType: node.nodeType,
    stabilityIndex: clamp01(node.stabilityIndex),
    riskIndex: clamp01(node.riskIndex),
    loadIndex: clamp01(node.loadIndex),
    resilienceIndex: clamp01(node.resilienceIndex),
    ecologicalDependencyIndex: clamp01(node.ecologicalDependencyIndex),
    infrastructureDependencyIndex: clamp01(node.infrastructureDependencyIndex),
    economicDependencyIndex: clamp01(node.economicDependencyIndex),
    collapseRiskIndex: clamp01(node.collapseRiskIndex),
    connections: node.connections ?? [],
    metadata: node.metadata ?? {},
  }
}

// Health evaluation (used by nodeMap + dashboard)
export function evaluateNodeHealth(node: NodeProfile) {
  let healthScore =
    node.stabilityIndex * 40 +
    node.resilienceIndex * 30 -
    node.loadIndex * 25 -
    node.riskIndex * 25

  healthScore -= node.ecologicalDependencyIndex * 15
  healthScore -= node.infrastructureDependencyIndex * 15
  healthScore -= node.economicDependencyIndex * 15
  healthScore -= node.collapseRiskIndex * 30

  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}

// Default node template
export function createDefaultNode(id: string, name: string, nodeType: NodeType): NodeProfile {
  return {
    id,
    name,
    nodeType,

    stabilityIndex: 0.5,
    riskIndex: 0.3,
    loadIndex: 0.4,
    resilienceIndex: 0.5,

    ecologicalDependencyIndex: 0.3,
    infrastructureDependencyIndex: 0.3,
    economicDependencyIndex: 0.3,

    collapseRiskIndex: 0.2,

    connections: [],
    metadata: {},
  }
}
