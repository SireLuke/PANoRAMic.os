// engine/nodes/NodeCollapseEngine.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile"

export function applyNodeCollapse(node: NodeProfile) {
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

  // Natural collapse pressure
  actions.push("Applying natural node collapse pressure.")
  collapseRiskIndex *= 1.05

  // High load increases collapse
  if (loadIndex > 0.7) {
    actions.push("High load — increasing collapse risk and reducing stability.")
    collapseRiskIndex *= 1.15
    stabilityIndex *= 0.9
  }

  // High risk increases collapse
  if (riskIndex > 0.6) {
    actions.push("High risk — accelerating collapse pressure.")
    collapseRiskIndex *= 1.1
  }

  // Low resilience penalty
  if (resilienceIndex < 0.4) {
    actions.push("Low resilience — reducing stability further.")
    stabilityIndex *= 0.85
  }

  // High dependency penalty
  const dependencyPressure =
    ecologicalDependencyIndex * 0.3 +
    infrastructureDependencyIndex * 0.3 +
    economicDependencyIndex * 0.3

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Collapse event trigger
  const collapseEventTrigger =
    collapseRiskIndex * 0.4 +
    riskIndex * 0.3 +
    (1 - stabilityIndex) * 0.2 +
    loadIndex * 0.1

  if (collapseEventTrigger > 0.8) {
    actions.push("Node collapse event triggered — forcing critical mode.")
    stabilityIndex *= 0.7
    resilienceIndex *= 0.8
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
    collapseEventTrigger,
  }
}