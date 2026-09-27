// engine/commons/CommonsFlowEngine.ts

import { CommonsProfile } from "../../core/pillars/commons/CommonsProfile"

export function computeCommonsFlow(commons: CommonsProfile) {
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

  // Stewardship boosts regeneration
  if (stewardshipIndex > 0.7) {
    actions.push("High stewardship — boosting regeneration and stability.")
    regenerationIndex *= 1.1
    stabilityIndex *= 1.05
  }

  // Dignity boosts stewardship
  if (dignityIndex > 0.7) {
    actions.push("High dignity — improving stewardship and reducing extraction pressure.")
    stewardshipIndex *= 1.05
    extractionPressureIndex *= 0.9
  }

  // Extraction pressure penalty
  if (extractionPressureIndex > 0.6) {
    actions.push("High extraction pressure — increasing depletion and collapse risk.")
    depletionIndex *= 1.1
    collapseRiskIndex *= 1.1
  }

  // Pollution penalty
  if (pollutionIndex > 0.5) {
    actions.push("High pollution — reducing regeneration.")
    regenerationIndex *= 0.9
  }

  // Dependency pressure
  const dependencyPressure =
    ecologicalDependencyIndex * 0.2 +
    infrastructureDependencyIndex * 0.2 +
    populationDependencyIndex * 0.2 +
    governanceDependencyIndex * 0.2 +
    marketDependencyIndex * 0.2

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing commons collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Collapse trigger
  const collapseTrigger =
    collapseRiskIndex * 0.4 +
    depletionIndex * 0.3 +
    pollutionIndex * 0.2 +
    (1 - stabilityIndex) * 0.1

  if (collapseTrigger > 0.75) {
    actions.push("Commons collapse risk — forcing critical mode.")
    stabilityIndex *= 0.8
    regenerationIndex *= 0.85
  }

  // Normalize
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
    collapseTrigger,
  }
}