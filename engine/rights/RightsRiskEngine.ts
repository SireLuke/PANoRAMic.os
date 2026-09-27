// engine/rights/RightsRiskEngine.ts

import { RightsProfile } from "../../core/pillars/rights/RightsProfile"

export function computeRightsRisk(rights: RightsProfile) {
  // Risk factors
  const dignityRisk = (1 - rights.dignityIndex) * 35
  const autonomyRisk = (1 - rights.autonomyIndex) * 30
  const safetyRisk = (1 - rights.safetyIndex) * 30
  const accessRisk = (1 - rights.accessIndex) * 25
  const fairnessRisk = (1 - rights.fairnessIndex) * 25

  const predatoryRisk = rights.predatoryPressureIndex * 35
  const exclusionRisk = rights.exclusionIndex * 30
  const exploitationRisk = rights.exploitationIndex * 30

  const dependencyRisk =
    rights.governanceDependencyIndex * 20 +
    rights.marketDependencyIndex * 20 +
    rights.workforceDependencyIndex * 20 +
    rights.infrastructureDependencyIndex * 20 +
    rights.ecologicalDependencyIndex * 20

  const collapseRisk = rights.collapseRiskIndex * 40

  let riskScore =
    dignityRisk +
    autonomyRisk +
    safetyRisk +
    accessRisk +
    fairnessRisk +
    predatoryRisk +
    exclusionRisk +
    exploitationRisk +
    dependencyRisk +
    collapseRisk

  // Normalize
  riskScore = Math.max(0, Math.min(riskScore, 100))

  let riskMode = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    riskScore,
    riskMode,
    breakdown: {
      dignityRisk,
      autonomyRisk,
      safetyRisk,
      accessRisk,
      fairnessRisk,
      predatoryRisk,
      exclusionRisk,
      exploitationRisk,
      dependencyRisk,
      collapseRisk,
    },
  }
}