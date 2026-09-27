// core/pillars/gep/SovereignRisk.ts

import { NationProfile } from "./NationProfile"
import { CurrencyProfile } from "./Currency"

export interface SovereignRiskReport {
  nation: string
  riskScore: number
  riskMode: "low" | "moderate" | "high" | "critical"
  breakdown: {
    debtRisk: number
    inflationRisk: number
    currencyRisk: number
    tradeRisk: number
    corruptionRisk: number
    conflictRisk: number
    ecologicalRisk: number
    infrastructureRisk: number
  }
}

export function computeSovereignRisk(
  nation: NationProfile,
  currency: CurrencyProfile,
  tradeSummary: {
    strategicDependencyIndex: number
    tradeStabilityIndex: number
  }
): SovereignRiskReport {
  // Debt risk: debt/GDP ratio
  const debtRisk =
    (nation.sovereignDebt / (nation.gdp + 1)) * 40

  // Inflation risk
  const inflationRisk = nation.inflationRate * 1.5

  // Currency risk
  const currencyRisk =
    currency.currencyRiskIndex * 40 +
    (1 - currency.stabilityIndex) * 30

  // Trade risk
  const tradeRisk =
    tradeSummary.strategicDependencyIndex * 40 +
    (1 - tradeSummary.tradeStabilityIndex) * 30

  // Corruption risk
  const corruptionRisk = nation.corruptionIndex * 40

  // Conflict risk
  const conflictRisk = nation.conflictRiskIndex * 50

  // Ecological risk
  const ecologicalRisk = nation.ecologicalFootprint * 30

  // Infrastructure risk
  const infrastructureRisk =
    (1 - nation.infrastructureResilience) * 40

  // Combine all risks
  let riskScore =
    debtRisk +
    inflationRisk +
    currencyRisk +
    tradeRisk +
    corruptionRisk +
    conflictRisk +
    ecologicalRisk +
    infrastructureRisk

  // Normalize to 0–100
  riskScore = Math.max(0, Math.min(riskScore, 100))

  // Risk mode
  let riskMode: SovereignRiskReport["riskMode"] = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    nation: nation.name,
    riskScore,
    riskMode,
    breakdown: {
      debtRisk,
      inflationRisk,
      currencyRisk,
      tradeRisk,
      corruptionRisk,
      conflictRisk,
      ecologicalRisk,
      infrastructureRisk,
    },
  }
}