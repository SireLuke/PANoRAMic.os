// engine/nodes/NodeRiskEngine.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile"

export function computeNodeRisk(node: NodeProfile) {
  // Risk factors
  const loadRisk = node.loadIndex * 35
  const stabilityRisk = (1 - node.stabilityIndex) * 35
  const resilienceRisk = (1 - node.resilienceIndex) * 30
  const dependencyRisk =
    node.ecologicalDependencyIndex * 25 +
    node.infrastructureDependencyIndex * 25 +
    node.economicDependencyIndex * 25

  const collapseRisk = node.collapseRiskIndex * 40

  let riskScore =
    loadRisk +
    stabilityRisk +
    resilienceRisk +
    dependencyRisk +
    collapseRisk

  // Normalize
  riskScore = Math.max(0, Math.min(riskScore, 100))

  let riskMode = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    riskScore,
    riskMode,
    breakdown: {
      loadRisk,
      stabilityRisk,
      resilienceRisk,
      dependencyRisk,
      collapseRisk,
    },
  }
}