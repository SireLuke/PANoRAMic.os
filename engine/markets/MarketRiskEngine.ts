// engine/markets/MarketRiskEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"

export function computeMarketRisk(market: MarketProfile) {
  // Risk factors
  const volatilityRisk = market.volatilityIndex * 35
  const stabilityRisk = (1 - market.stabilityIndex) * 35
  const resilienceRisk = (1 - market.resilienceIndex) * 30
  const loadRisk = market.loadIndex * 30

  const predatoryRisk = market.predatoryPressureIndex * 40

  const dependencyRisk =
    market.ecologicalDependencyIndex * 25 +
    market.infrastructureDependencyIndex * 25 +
    market.workforceDependencyIndex * 25

  const collapseRisk = market.collapseRiskIndex * 40

  let riskScore =
    volatilityRisk +
    stabilityRisk +
    resilienceRisk +
    loadRisk +
    predatoryRisk +
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
      volatilityRisk,
      stabilityRisk,
      resilienceRisk,
      loadRisk,
      predatoryRisk,
      dependencyRisk,
      collapseRisk,
    },
  }
}