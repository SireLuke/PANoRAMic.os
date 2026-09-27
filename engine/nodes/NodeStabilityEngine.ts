// engine/nodes/NodeStabilityEngine.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile"
import { computeNodeRisk } from "./NodeRiskEngine"

export function computeNodeStability(node: NodeProfile) {
  const risk = computeNodeRisk(node)

  // Stability factors
  const stabilityFactor = node.stabilityIndex * 40
  const resilienceFactor = node.resilienceIndex * 35

  // Penalties
  const loadPenalty = node.loadIndex * 30
  const dependencyPenalty =
    node.ecologicalDependencyIndex * 20 +
    node.infrastructureDependencyIndex * 20 +
    node.economicDependencyIndex * 20

  const collapsePenalty = node.collapseRiskIndex * 35

  let stabilityScore =
    stabilityFactor +
    resilienceFactor -
    loadPenalty -
    dependencyPenalty -
    collapsePenalty -
    risk.riskScore * 0.2

  // Normalize
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      stabilityFactor,
      resilienceFactor,
      loadPenalty,
      dependencyPenalty,
      collapsePenalty,
      riskScore: risk.riskScore,
    },
  }
}