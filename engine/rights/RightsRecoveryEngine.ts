// engine/rights/RightsRecoveryEngine.ts

import { RightsProfile } from "../../core/pillars/rights/RightsProfile"

export function applyRightsRecovery(rights: RightsProfile) {
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

  // Base recovery
  actions.push("Applying base rights recovery.")
  dignityIndex *= 1.05
  fairnessIndex *= 1.05

  // Autonomy boosts recovery
  if (autonomyIndex > 0.6) {
    actions.push("Strong autonomy — reducing exclusion and exploitation.")
    exclusionIndex *= 0.9
    exploitationIndex *= 0.9
  }

  // Safety boosts stability
  if (safetyIndex > 0.7) {
    actions.push("High safety — reducing collapse pressure.")
    collapseRiskIndex *= 0.9
  }

  // Access boosts dignity
  if (accessIndex > 0.6) {
    actions.push("Strong access — reinforcing dignity.")
    dignityIndex *= 1.05
  }

  // Dependency pressure recovery
  const dependencyPressure =
    governanceDependencyIndex * 0.2 +
    marketDependencyIndex * 0.2 +
    workforceDependencyIndex * 0.2 +
    infrastructureDependencyIndex * 0.2 +
    ecologicalDependencyIndex * 0.2

  if (dependencyPressure < 0.5) {
    actions.push("Low dependency pressure — boosting rights stability.")
    fairnessIndex *= 1.1
  }

  // Recovery trigger
  const recoveryTrigger =
    (1 - collapseRiskIndex) * 0.4 +
    dignityIndex * 0.3 +
    fairnessIndex * 0.3

  if (recoveryTrigger > 0.7) {
    actions.push("Recovery trigger — significantly reducing risk.")
    collapseRiskIndex *= 0.85
    predatoryPressureIndex *= 0.9
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
    recoveryTrigger,
  }
}