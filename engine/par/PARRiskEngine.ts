// engine/par/PARRiskEngine.ts

import { PARProfile } from "../../core/pillars/par/PARProfile"

export function computePARRisk(par: PARProfile) {
  // Risk factors
  const volatilityRisk = par.volatilityIndex * 35
  const stabilityRisk = (1 - par.stabilityIndex) * 35
  const liquidityRisk = (1 - par.liquidityIndex) * 30
  const dignityRisk = (1 - par.dignityIndex) * 30

  const backingRisk =
    (1 - par.ecologicalBackingIndex) * 25 +
    (1 - par.infrastructureBackingIndex) * 25 +
    (1 - par.workforceBackingIndex) * 25 +
    (1 - par.marketBackingIndex) * 25

  const collapseRisk = par.collapseRiskIndex * 40

  let riskScore =
    volatilityRisk +
    stabilityRisk +
    liquidityRisk +
    dignityRisk +
    backingRisk +
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
      volatilityRisk,
      stabilityRisk,
      liquidityRisk,
      dignityRisk,
      backingRisk,
      collapseRisk,
    },
  }
}