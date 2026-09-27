// engine/population/PopulationRecoveryEngine.ts

import { PopulationProfile } from "../../core/pillars/population/PopulationProfile"

export function applyPopulationRecovery(pop: PopulationProfile) {
  const actions: string[] = []

  let {
    stabilityIndex,
    riskIndex,
    resilienceIndex,
    dignityIndex,
    cohesionIndex,
    conflictIndex,
    stressIndex,
    burnoutIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    workforceDependencyIndex,
    marketDependencyIndex,
    governanceDependencyIndex,
    collapseRiskIndex,
  } = pop

  // Base recovery
  actions.push("Applying base population recovery.")
  stabilityIndex *= 1.05
  resilienceIndex *= 1.05

  // Cohesion boosts recovery
  if (cohesionIndex > 0.6) {
    actions.push("Strong cohesion — reducing conflict and collapse pressure.")
    conflictIndex *= 0.9
    collapseRiskIndex *= 0.9
  }

  // Dignity boosts stability
  if (dignityIndex > 0.7) {
    actions.push("High dignity — stabilizing population behavior.")
    stabilityIndex *= 1.1
    riskIndex *= 0.9
  }

  // Stress recovery
  if (stressIndex < 0.4) {
    actions.push("Low stress — boosting resilience.")
    resilienceIndex *= 1.1
  }

  // Burnout recovery
  if (burnoutIndex < 0.4) {
    actions.push("Low burnout — improving stability.")
    stabilityIndex *= 1.05
  }

  // Dependency pressure recovery
  const dependencyPressure =
    ecologicalDependencyIndex * 0.2 +
    infrastructureDependencyIndex * 0.2 +
    workforceDependencyIndex * 0.2 +
    marketDependencyIndex * 0.2 +
    governanceDependencyIndex * 0.2

  if (dependencyPressure < 0.5) {
    actions.push("Low dependency pressure — boosting stability.")
    stabilityIndex *= 1.1
  }

  // Recovery trigger
  const recoveryTrigger =
    (1 - collapseRiskIndex) * 0.4 +
    stabilityIndex * 0.3 +
    dignityIndex * 0.3

  if (recoveryTrigger > 0.7) {
    actions.push("Recovery trigger — significantly reducing risk.")
    riskIndex *= 0.85
    collapseRiskIndex *= 0.85
  }

  // Normalize
  stabilityIndex = Math.max(0, Math.min(stabilityIndex, 1))
  riskIndex = Math.max(0, Math.min(riskIndex, 1))
  resilienceIndex = Math.max(0, Math.min(resilienceIndex, 1))
  dignityIndex = Math.max(0, Math.min(dignityIndex, 1))
  cohesionIndex = Math.max(0, Math.min(cohesionIndex, 1))
  conflictIndex = Math.max(0, Math.min(conflictIndex, 1))
  stressIndex = Math.max(0, Math.min(stressIndex, 1))
  burnoutIndex = Math.max(0, Math.min(burnoutIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))
  infrastructureDependencyIndex = Math.max(0, Math.min(infrastructureDependencyIndex, 1))
  workforceDependencyIndex = Math.max(0, Math.min(workforceDependencyIndex, 1))
  marketDependencyIndex = Math.max(0, Math.min(marketDependencyIndex, 1))
  governanceDependencyIndex = Math.max(0, Math.min(governanceDependencyIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  // Update pop
  pop.stabilityIndex = stabilityIndex
  pop.riskIndex = riskIndex
  pop.resilienceIndex = resilienceIndex
  pop.dignityIndex = dignityIndex
  pop.cohesionIndex = cohesionIndex
  pop.conflictIndex = conflictIndex
  pop.stressIndex = stressIndex
  pop.burnoutIndex = burnoutIndex
  pop.ecologicalDependencyIndex = ecologicalDependencyIndex
  pop.infrastructureDependencyIndex = infrastructureDependencyIndex
  pop.workforceDependencyIndex = workforceDependencyIndex
  pop.marketDependencyIndex = marketDependencyIndex
  pop.governanceDependencyIndex = governanceDependencyIndex
  pop.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedPopulation: pop,
    stabilityIndex,
    riskIndex,
    resilienceIndex,
    dignityIndex,
    cohesionIndex,
    conflictIndex,
    stressIndex,
    burnoutIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    workforceDependencyIndex,
    marketDependencyIndex,
    governanceDependencyIndex,
    collapseRiskIndex,
    recoveryTrigger,
  }
}