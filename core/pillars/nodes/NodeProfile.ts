// core/pillars/nodes/NodeProfile.ts

export interface NodeProfile {
  name: string
  nodeType:
    | "city"
    | "region"
    | "biome"
    | "infrastructure_cluster"
    | "workforce_cluster"
    | "supply_chain_hub"
    | "planetary_subsystem"
    | "orbital_station"
    | "starship_habitat"

  // Core metrics
  stabilityIndex: number            // 0–1
  riskIndex: number                 // 0–1
  loadIndex: number                 // 0–1
  resilienceIndex: number           // 0–1

  // Dependency metrics
  ecologicalDependencyIndex: number // 0–1
  infrastructureDependencyIndex: number // 0–1
  economicDependencyIndex: number   // 0–1

  // Collapse metrics
  collapseRiskIndex: number         // 0–1
}

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