// engine/governance/GovernanceRiskEngine.ts

import { GovernanceProfile } from "../../core/pillars/governance/GovernanceProfile"

export function computeGovernanceRisk(gov: GovernanceProfile) {
  // Risk factors
  const conflictRisk = gov.conflictIndex * 35
  const stabilityRisk = (1 - gov.stabilityIndex) * 35
  const coordinationRisk = (1 - gov.coordinationIndex) * 30
  const dignityRisk = (1 - gov.dignityIndex) * 30
  const responsivenessRisk = (1 - gov.responsivenessIndex) * 25

  const dependencyRisk =
    gov.ecologicalDependencyIndex * 20 +
    gov.infrastructureDependencyIndex * 20 +
    gov.workforceDependencyIndex * 20 +
    gov.marketDependencyIndex * 20

  const collapseRisk = gov.collapseRiskIndex * 40

  let riskScore =
    conflictRisk +
    stabilityRisk +
    coordinationRisk +
    dignityRisk +
    responsivenessRisk +
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
      conflictRisk,
      stabilityRisk,
      coordinationRisk,
      dignityRisk,
      responsivenessRisk,
      dependencyRisk,
      collapseRisk,
    },
  }
}