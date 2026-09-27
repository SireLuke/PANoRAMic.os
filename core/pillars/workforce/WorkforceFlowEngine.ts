// engine/workforce/WorkforceFlowEngine.ts

import { WorkforceProfile } from "../../core/pillars/workforce/WorkforceProfile"

export function computeWorkforceFlow(work: WorkforceProfile) {
  const actions: string[] = []

  let {
    stabilityIndex,
    riskIndex,
    loadIndex,
    resilienceIndex,
    burnoutIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    economicDependencyIndex,
    collapseRiskIndex,
  } = work

  // Load effects
  if (loadIndex > 0.7) {
    actions.push("High workload — increasing burnout and collapse pressure.")
    burnoutIndex *= 1.15
    collapseRiskIndex *= 1.2
  }

  // Resilience boost
  if (resilienceIndex > 0.7) {
    actions.push("High resilience — reducing burnout and risk.")
    burnoutIndex *= 0.9
    riskIndex *= 0.9
  }

  // Burnout penalty
  if (burnoutIndex > 0.6) {
    actions.push("High burnout — reducing stability.")
    stabilityIndex *= 0.9
  }

  // Dependency penalties
  if (ecologicalDependencyIndex > 0.6) {
    actions.push("High ecological dependency — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
  }

  if (infrastructureDependencyIndex > 0.6) {
    actions.push("High infrastructure dependency — increasing risk.")
    riskIndex *= 1.1
  }

  if (economicDependencyIndex > 0.6) {
    actions.push("High economic dependency — reducing stability.")
    stabilityIndex *= 0.9
  }

  // Collapse trigger
  const collapseTrigger =
    riskIndex * 0.3 +
    burnoutIndex * 0.3 +
    loadIndex * 0.2 +
    (1 - resilienceIndex) * 0.2

  if (collapseTrigger > 0.75) {
    actions.push("Workforce collapse risk — boosting stability and reducing burnout.")
    stabilityIndex *= 1.2
    burnoutIndex *= 0.85
  }

  // Normalize
  stabilityIndex = Math.max(0, Math.min(stabilityIndex, 1))
  riskIndex = Math.max(0, Math.min(riskIndex, 1))
  loadIndex = Math.max(0, Math.min(loadIndex, 1))
  resilienceIndex = Math.max(0, Math.min(resilienceIndex, 1))
  burnoutIndex = Math.max(0, Math.min(burnoutIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))
  infrastructureDependencyIndex = Math.max(0, Math.min(infrastructureDependencyIndex, 1))
  economicDependencyIndex = Math.max(0, Math.min(economicDependencyIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  // Update work
  work.stabilityIndex = stabilityIndex
  work.riskIndex = riskIndex
  work.loadIndex = loadIndex
  work.resilienceIndex = resilienceIndex
  work.burnoutIndex = burnoutIndex
  work.ecologicalDependencyIndex = ecologicalDependencyIndex
  work.infrastructureDependencyIndex = infrastructureDependencyIndex
  work.economicDependencyIndex = economicDependencyIndex
  work.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedWorkforce: work,
    stabilityIndex,
    riskIndex,
    loadIndex,
    resilienceIndex,
    burnoutIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    economicDependencyIndex,
    collapseRiskIndex,
    collapseTrigger,
  }
}