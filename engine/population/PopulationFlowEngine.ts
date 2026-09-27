// engine/population/PopulationFlowEngine.ts

import { PopulationProfile } from "../../core/pillars/population/PopulationProfile"

export function computePopulationFlow(pop: PopulationProfile) {
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

  // Cohesion boosts stability
  if (cohesionIndex > 0.7) {
    actions.push("High cohesion — improving stability and reducing conflict.")
    stabilityIndex *= 1.05
    conflictIndex *= 0.9
  }

  // Dignity boosts resilience
  if (dignityIndex > 0.7) {
    actions.push("High dignity — boosting resilience and reducing collapse pressure.")
    resilienceIndex *= 1.1
    collapseRiskIndex *= 0.9
  }

  // Stress penalty
  if (stressIndex > 0.6) {
    actions.push("High stress — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
    stabilityIndex *= 0.9
  }

  // Burnout penalty
  if (burnoutIndex > 0.5) {
    actions.push("High burnout — reducing resilience.")
    resilienceIndex *= 0.9
  }

  // Conflict penalty
  if (conflictIndex > 0.5) {
    actions.push("High conflict — increasing collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Dependency pressure
  const dependencyPressure =
    ecologicalDependencyIndex * 0.2 +
    infrastructureDependencyIndex * 0.2 +
    workforceDependencyIndex * 0.2 +
    marketDependencyIndex * 0.2 +
    governanceDependencyIndex * 0.2

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing population collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Collapse trigger
  const collapseTrigger =
    collapseRiskIndex * 0.4 +
    conflictIndex * 0.3 +
    stressIndex * 0.2 +
    (1 - stabilityIndex) * 0.1

  if (collapseTrigger > 0.75) {
    actions.push("Population collapse risk — forcing critical mode.")
    stabilityIndex *= 0.8
    resilienceIndex *= 0.85
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
    collapseTrigger,
  }
}