// engine/commons/CommonsRiskEngine.ts

import { CommonsProfile } from "../../core/pillars/commons/CommonsProfile"

export function computeCommonsRisk(commons: CommonsProfile) {
  const extractionRisk = commons.extractionPressureIndex * 35
  const depletionRisk = commons.depletionIndex * 35
  const pollutionRisk = commons.pollutionIndex * 30

  const stabilityRisk = (1 - commons.stabilityIndex) * 30
  const regenerationRisk = (1 - commons.regenerationIndex) * 30
  const stewardshipRisk = (1 - commons.stewardshipIndex) * 25
  const dignityRisk = (1 - commons.dignityIndex) * 25

  const dependencyRisk =
    commons.ecologicalDependencyIndex * 20 +
    commons.infrastructureDependencyIndex * 20 +
    commons.populationDependencyIndex * 20 +
    commons.governanceDependencyIndex * 20 +
    commons.marketDependencyIndex * 20

  const collapseRisk = commons.collapseRiskIndex * 40

  let riskScore =
    extractionRisk +
    depletionRisk +
    pollutionRisk +
    stabilityRisk +
    regenerationRisk +
    stewardshipRisk +
    dignityRisk +
    dependencyRisk +
    collapseRisk

  riskScore = Math.max(0, Math.min(riskScore, 100))

  let riskMode = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    riskScore,
    riskMode,
    breakdown: {
      extractionRisk,
      depletionRisk,
      pollutionRisk,
      stabilityRisk,
      regenerationRisk,
      stewardshipRisk,
      dignityRisk,
      dependencyRisk,
      collapseRisk,
    },
  }
}