// engine/nodes/NodeSynthesisEngine.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile"
import { computeNodeRisk } from "./NodeRiskEngine"
import { computeNodeStability } from "./NodeStabilityEngine"

export function computeNodeSynthesis(node: NodeProfile) {
  const risk = computeNodeRisk(node)
  const stability = computeNodeStability(node)

  // Additional synthesis indicators
  const stabilityFactor = node.stabilityIndex * 30
  const resilienceFactor = node.resilienceIndex * 30

  const loadPenalty = node.loadIndex * 25
  const dependencyPenalty =
    node.ecologicalDependencyIndex * 20 +
    node.infrastructureDependencyIndex * 20 +
    node.economicDependencyIndex * 20

  const collapsePenalty = node.collapseRiskIndex * 30

  // Synthesis score combines:
  // - stability
  // - inverse risk
  // - stability + resilience
  // - penalties for load, dependencies, collapse

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    stabilityFactor +
    resilienceFactor -
    loadPenalty -
    dependencyPenalty -
    collapsePenalty

  // Normalize
  synthesisScore = Math.max(0, Math.min(synthesisScore, 100))

  let synthesisMode = "stable"
  if (synthesisScore < 40) synthesisMode = "critical"
  else if (synthesisScore < 70) synthesisMode = "unstable"

  return {
    synthesisScore,
    synthesisMode,
    breakdown: {
      stabilityScore: stability.stabilityScore,
      riskScore: risk.riskScore,
      stabilityFactor,
      resilienceFactor,
      loadPenalty,
      dependencyPenalty,
      collapsePenalty,
    },
  }
}