// engine/rights/RightsCollapseEngine.ts

import { RightsProfile } from "../../core/pillars/rights/RightsProfile"

export function applyRightsCollapse(rights: RightsProfile) {
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

  // Natural collapse pressure
  actions.push("Applying natural rights collapse pressure.")
  collapseRiskIndex *= 1.05

  // Predatory pressure penalty
  if (predatoryPressureIndex > 0.6) {
    actions.push("High predatory pressure — increasing collapse risk and reducing dignity.")
    collapseRiskIndex *= 1.15
    dignityIndex *= 0.9
  }

  // Exclusion penalty
  if (exclusionIndex > 0.5) {
    actions.push("High exclusion — reducing access and fairness.")
    accessIndex *= 0.9
    fairnessIndex *= 0.9
  }

  // Exploitation penalty
  if (exploitationIndex > 0.5) {
    actions.push("High exploitation — reducing autonomy and safety.")
    autonomyIndex *= 0.9
    safetyIndex *= 0.9
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

  // Collapse event trigger
  const collapseEventTrigger =
    collapseRiskIndex * 0.4 +
    predatoryPressureIndex * 0.3 +
    exclusionIndex * 0.2 +
    (1 - dignityIndex) * 0.1

  if (collapseEventTrigger > 0.8) {
    actions.push("Rights collapse event triggered — forcing critical mode.")
    dignityIndex *= 0.8
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
    collapseEventTrigger,
  }
}