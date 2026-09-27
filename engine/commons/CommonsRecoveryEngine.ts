// engine/commons/CommonsRecoveryEngine.ts

import { CommonsProfile } from "../../core/pillars/commons/CommonsProfile"

export function applyCommonsRecovery(commons: CommonsProfile) {
  const actions: string[] = []

  let {
    stabilityIndex,
    riskIndex,
    regenerationIndex,
    stewardshipIndex,
    dignityIndex,
    extractionPressureIndex,
    depletionIndex,
    pollutionIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    populationDependencyIndex,
    governanceDependencyIndex,
    marketDependencyIndex,
    collapseRiskIndex,
  } = commons

  actions.push("Applying base commons recovery.")
  regenerationIndex *= 1.05
  stabilityIndex *= 1.05

  if (stewardshipIndex > 0.6) {
    actions.push("Strong stewardship — reducing depletion and collapse pressure.")
    depletionIndex *= 0.9
    collapseRiskIndex *= 0.9
  }

  if (dignityIndex > 0.7) {
    actions.push("High dignity — reinforcing stewardship.")
    stewardshipIndex *= 1.1
  }

  if (pollutionIndex < 0.4) {
    actions.push("Low pollution — boosting regeneration.")
    regenerationIndex *= 1.1
  }

  const dependencyPressure =
    ecologicalDependencyIndex * 0.2 +
    infrastructureDependencyIndex * 0.2 +
    populationDependencyIndex * 0.2 +
    governanceDependencyIndex * 0.2 +
    marketDependencyIndex * 0.2

  if (dependencyPressure < 0.5) {
    actions.push("Low dependency pressure — boosting stability.")
    stabilityIndex *= 1.1
  }

  const recoveryTrigger =
    (1 - collapseRiskIndex) * 0.4 +
    regenerationIndex * 0.3 +
    stewardshipIndex * 0.3

  if (recoveryTrigger > 0.7) {
    actions.push("Recovery trigger — significantly reducing risk.")
    collapseRiskIndex *= 0.85
    extractionPressureIndex *= 0.9
  }

  stabilityIndex = Math.max(0, Math.min(stabilityIndex, 1))
  riskIndex = Math.max(0, Math.min(riskIndex, 1))
  regenerationIndex = Math.max(0, Math.min(regenerationIndex, 1))
  stewardshipIndex = Math.max(0, Math.min(stewardshipIndex, 1))
  dignityIndex = Math.max(0, Math.min(dignityIndex, 1))
  extractionPressureIndex = Math.max(0, Math.min(extractionPressureIndex, 1))
  depletionIndex = Math.max(0, Math.min(depletionIndex, 1))
  pollutionIndex = Math.max(0, Math.min(pollutionIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))
  infrastructureDependencyIndex = Math.max(0, Math.min(infrastructureDependencyIndex, 1))
  populationDependencyIndex = Math.max(0, Math.min(populationDependencyIndex, 1))
  governanceDependencyIndex = Math.max(0, Math.min(governanceDependencyIndex, 1))
  marketDependencyIndex = Math.max(0, Math.min(marketDependencyIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  commons.stabilityIndex = stabilityIndex
  commons.riskIndex = riskIndex
  commons.regenerationIndex = regenerationIndex
  commons.stewardshipIndex = stewardshipIndex
  commons.dignityIndex = dignityIndex
  commons.extractionPressureIndex = extractionPressureIndex
  commons.depletionIndex = depletionIndex
  commons.pollutionIndex = pollutionIndex
  commons.ecologicalDependencyIndex = ecologicalDependencyIndex
  commons.infrastructureDependencyIndex = infrastructureDependencyIndex
  commons.populationDependencyIndex = populationDependencyIndex
  commons.governanceDependencyIndex = governanceDependencyIndex
  commons.marketDependencyIndex = marketDependencyIndex
  commons.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedCommons: commons,
    stabilityIndex,
    riskIndex,
    regenerationIndex,
    stewardshipIndex,
    dignityIndex,
    extractionPressureIndex,
    depletionIndex,
    pollutionIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    populationDependencyIndex,
    governanceDependencyIndex,
    marketDependencyIndex,
    collapseRiskIndex,
    recoveryTrigger,
  }
}