// engine/workforce/WorkforceRecoveryEngine.ts

import { WorkforceProfile } from "../../core/pillars/workforce/WorkforceProfile"

export function applyWorkforceRecovery(work: WorkforceProfile) {
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

  // Base recovery
  actions.push("Applying base workforce recovery.")
  stabilityIndex *= 1.05
  resilienceIndex *= 1.05

  // High resilience boosts recovery
  if (resilienceIndex > 0.7) {
    actions.push("High resilience — reducing burnout and collapse pressure.")
    burnoutIndex *= 0.9
    collapseRiskIndex *= 0.9
  }

  // Manageable load supports recovery
  if (loadIndex < 0.6) {
    actions.push("Moderate workload — supporting recovery.")
    stabilityIndex *= 1.1
  } else {
    actions.push("High workload — limiting recovery effectiveness.")
    stabilityIndex *= 0.95
  }

  // Burnout recovery
  if (burnoutIndex > 0.5) {
    actions.push("High burnout — applying burnout recovery dampening.")
    burnoutIndex *= 0.9
  }

  // Dependency pressure recovery
  const dependencyPressure =
    ecologicalDependencyIndex * 0.3 +
    infrastructureDependencyIndex * 0.3 +
    economicDependencyIndex * 0.3

  if (dependencyPressure < 0.5) {
    actions.push("Low dependency pressure — boosting stability.")
    stabilityIndex *= 1.1
  }

  // Recovery trigger
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
    recoveryTrigger,
  }
}