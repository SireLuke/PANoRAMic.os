// engine/nodes/NodeFlowEngine.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile"

export function computeNodeFlow(node: NodeProfile) {
  const actions: string[] = []

  let {
    stabilityIndex,
    riskIndex,
    loadIndex,
    resilienceIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    economicDependencyIndex,
    collapseRiskIndex,
  } = node

  // Load effects
  if (loadIndex > 0.7) {
    actions.push("High node load — increasing risk and collapse pressure.")
    riskIndex *= 1.15
    collapseRiskIndex *= 1.2
  }

  // Resilience boost
  if (resilienceIndex > 0.7) {
    actions.push("High resilience — reducing risk and collapse pressure.")
    riskIndex *= 0.9
    collapseRiskIndex *= 0.85
  }

  // Ecological dependency penalty
  if (ecologicalDependencyIndex > 0.6) {
    actions.push("High ecological dependency — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
  }

  // Infrastructure dependency penalty
  if (infrastructureDependencyIndex > 0.6) {
    actions.push("High infrastructure dependency — increasing risk.")
    riskIndex *= 1.1
  }

  // Economic dependency penalty
  if (economicDependencyIndex > 0.6) {
    actions.push("High economic dependency — reducing stability.")
    stabilityIndex *= 0.9
  }

  // Collapse triggers
  const collapseTrigger =
    riskIndex * 0.4 +
    loadIndex * 0.3 +
    (1 - resilienceIndex) * 0.2 +
    (ecologicalDependencyIndex + infrastructureDependencyIndex + economicDependencyIndex) * 0.1

  if (collapseTrigger > 0.75) {
    actions.push("Node collapse risk — boosting stability and reducing risk.")
    stabilityIndex *= 1.2
    riskIndex *= 0.85
  }

  // Normalize
  stabilityIndex = Math.max(0, Math.min(stabilityIndex, 1))
  riskIndex = Math.max(0, Math.min(riskIndex, 1))
  loadIndex = Math.max(0, Math.min(loadIndex, 1))
  resilienceIndex = Math.max(0, Math.min(resilienceIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))
  infrastructureDependencyIndex = Math.max(0, Math.min(infrastructureDependencyIndex, 1))
  economicDependencyIndex = Math.max(0, Math.min(economicDependencyIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  // Update node
  node.stabilityIndex = stabilityIndex
  node.riskIndex = riskIndex
  node.loadIndex = loadIndex
  node.resilienceIndex = resilienceIndex
  node.ecologicalDependencyIndex = ecologicalDependencyIndex
  node.infrastructureDependencyIndex = infrastructureDependencyIndex
  node.economicDependencyIndex = economicDependencyIndex
  node.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedNode: node,
    stabilityIndex,
    riskIndex,
    loadIndex,
    resilienceIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    economicDependencyIndex,
    collapseRiskIndex,
    collapseTrigger,
  }
}