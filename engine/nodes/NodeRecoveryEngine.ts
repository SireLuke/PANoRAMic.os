// engine/nodes/NodeRecoveryEngine.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile"

export function applyNodeRecovery(node: NodeProfile) {
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

  // Base recovery
  actions.push("Applying base node recovery.")
  stabilityIndex *= 1.05
  resilienceIndex *= 1.05

  // High resilience boosts recovery
  if (resilienceIndex > 0.7) {
    actions.push("High resilience — reducing risk and collapse pressure.")
    riskIndex *= 0.9
    collapseRiskIndex *= 0.9
  }

  // Community / systemic recovery concept:
  const dependencyPressure =
    ecologicalDependencyIndex * 0.3 +
    infrastructureDependencyIndex * 0.3 +
    economicDependencyIndex * 0.3

  if (dependencyPressure < 0.5) {
    actions.push("Manageable dependency pressure — boosting stability.")
    stabilityIndex *= 1.1
  }

  // Load reduction
  if (loadIndex > 0.7) {
    actions.push("High load — limiting recovery effectiveness.")
    stabilityIndex *= 0.95
  } else {
    actions.push("Moderate load — supporting recovery.")
    stabilityIndex *= 1.05
  }

  // Collapse recovery trigger
  const recoveryTrigger =
    (1 - collapseRiskIndex) * 0.4 +
    resilienceIndex * 0.3 +
    stabilityIndex * 0.3

  if (recoveryTrigger > 0.7) {
    actions.push("Recovery trigger — significantly reducing risk.")
    riskIndex *= 0.85
    collapseRiskIndex *= 0.85
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
    recoveryTrigger,
  }
}