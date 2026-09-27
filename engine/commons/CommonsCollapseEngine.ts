// engine/commons/CommonsCollapseEngine.ts

import { CommonsProfile } from "../../core/pillars/commons/CommonsProfile"

export function applyCommonsCollapse(commons: CommonsProfile) {
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

  actions.push("Applying natural commons collapse pressure.")
  collapseRiskIndex *= 1.05

  if (extractionPressureIndex > 0.6) {
    actions.push("High extraction — increasing depletion and collapse risk.")
    depletionIndex *= 1.15
    collapseRiskIndex *= 1.1
  }

  if (pollutionIndex > 0.5) {
    actions.push("High pollution — reducing regeneration.")
    regenerationIndex *= 0.9
  }

  if (stewardshipIndex < 0.4) {
    actions.push("Low stewardship — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
  }

  const dependencyPressure =
    ecologicalDependencyIndex * 0.2 +
    infrastructureDependencyIndex * 0.2 +
    populationDependencyIndex * 0.2 +
    governanceDependencyIndex * 0.2 +
    marketDependencyIndex * 0.2

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing collapse risk.")
    collapseRiskIndex *= 1.1
  }

  const collapseEventTrigger =
    collapseRiskIndex * 0.4 +
    depletionIndex * 0.3 +
    pollutionIndex * 0.2 +
    (1 - stabilityIndex) * 0.1

  if (collapseEventTrigger > 0.8) {
    actions.push("Commons collapse event triggered — forcing critical mode.")
    stabilityIndex *= 0.7
    regenerationIndex *= 0.85
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
    collapseEventTrigger,
  }
}