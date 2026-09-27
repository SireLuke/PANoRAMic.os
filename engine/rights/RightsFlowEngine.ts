// engine/rights/RightsFlowEngine.ts

import { RightsProfile } from "../../core/pillars/rights/RightsProfile"

export function computeRightsFlow(rights: RightsProfile) {
  const actions: string[] = []

  let {
    dignityIndex,
    autonomyIndex,
    safetyIndex,
    accessIndex,
    fairnessIndex,
    predatoryPressureIndex,
    exclusionIndex,
    exploitationIndex,
    governanceDependencyIndex,
    marketDependencyIndex,
    workforceDependencyIndex,
    infrastructureDependencyIndex,
    ecologicalDependencyIndex,
    collapseRiskIndex,
  } = rights

  // Dignity boosts everything
  if (dignityIndex > 0.7) {
    actions.push("High dignity — strengthening autonomy, safety, and fairness.")
    autonomyIndex *= 1.05
    safetyIndex *= 1.05
    fairnessIndex *= 1.05
  }

  // Autonomy boosts access
  if (autonomyIndex > 0.6) {
    actions.push("Strong autonomy — improving access and reducing exclusion.")
    accessIndex *= 1.05
    exclusionIndex *= 0.9
  }

  // Predatory pressure penalty
  if (predatoryPressureIndex > 0.5) {
    actions.push("High predatory pressure — increasing collapse risk.")
    collapseRiskIndex *= 1.1
    dignityIndex *= 0.95
  }

  // Exploitation penalty
  if (exploitationIndex > 0.5) {
    actions.push("High exploitation — reducing fairness and autonomy.")
    fairnessIndex *= 0.9
    autonomyIndex *= 0.9
  }

  // Dependency pressure
  const dependencyPressure =
    governanceDependencyIndex * 0.2 +
    marketDependencyIndex * 0.2 +
    workforceDependencyIndex * 0.2 +
    infrastructureDependencyIndex * 0.2 +
    ecologicalDependencyIndex * 0.2

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing rights collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Collapse trigger
  const collapseTrigger =
    collapseRiskIndex * 0.4 +
    predatoryPressureIndex * 0.3 +
    exclusionIndex * 0.2 +
    (1 - dignityIndex) * 0.1

  if (collapseTrigger > 0.75) {
    actions.push("Rights collapse risk — forcing critical mode.")
    dignityIndex *= 0.85
    fairnessIndex *= 0.85
  }

  // Normalize
  dignityIndex = Math.max(0, Math.min(dignityIndex, 1))
  autonomyIndex = Math.max(0, Math.min(autonomyIndex, 1))
  safetyIndex = Math.max(0, Math.min(safetyIndex, 1))
  accessIndex = Math.max(0, Math.min(accessIndex, 1))
  fairnessIndex = Math.max(0, Math.min(fairnessIndex, 1))
  predatoryPressureIndex = Math.max(0, Math.min(predatoryPressureIndex, 1))
  exclusionIndex = Math.max(0, Math.min(exclusionIndex, 1))
  exploitationIndex = Math.max(0, Math.min(exploitationIndex, 1))
  governanceDependencyIndex = Math.max(0, Math.min(governanceDependencyIndex, 1))
  marketDependencyIndex = Math.max(0, Math.min(marketDependencyIndex, 1))
  workforceDependencyIndex = Math.max(0, Math.min(workforceDependencyIndex, 1))
  infrastructureDependencyIndex = Math.max(0, Math.min(infrastructureDependencyIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  // Update rights
  rights.dignityIndex = dignityIndex
  rights.autonomyIndex = autonomyIndex
  rights.safetyIndex = safetyIndex
  rights.accessIndex = accessIndex
  rights.fairnessIndex = fairnessIndex
  rights.predatoryPressureIndex = predatoryPressureIndex
  rights.exclusionIndex = exclusionIndex
  rights.exploitationIndex = exploitationIndex
  rights.governanceDependencyIndex = governanceDependencyIndex
  rights.marketDependencyIndex = marketDependencyIndex
  rights.workforceDependencyIndex = workforceDependencyIndex
  rights.infrastructureDependencyIndex = infrastructureDependencyIndex
  rights.ecologicalDependencyIndex = ecologicalDependencyIndex
  rights.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedRights: rights,
    dignityIndex,
    autonomyIndex,
    safetyIndex,
    accessIndex,
    fairnessIndex,
    predatoryPressureIndex,
    exclusionIndex,
    exploitationIndex,
    governanceDependencyIndex,
    marketDependencyIndex,
    workforceDependencyIndex,
    infrastructureDependencyIndex,
    ecologicalDependencyIndex,
    collapseRiskIndex,
    collapseTrigger,
  }
}