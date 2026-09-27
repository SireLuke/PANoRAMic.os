// engine/markets/marketRiskEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"

export function computeMarketRisk(market: MarketProfile) {
  // Risk factors:
  // - extraction pressure
  // - corruption
  // - liquidity collapse
  // - velocity collapse
  // - ecological impact
  // - infrastructure dependency
  // - dignity violations
  // - outlawed market types

  const extractionRisk = market.extractivePressureIndex * 40
  const corruptionRisk = market.corruptionIndex * 30

  const liquidityRisk = (1 - market.liquidity) * 20
  const velocityRisk = (1 - market.velocity) * 20

  const ecologicalRisk = market.ecologicalImpactIndex * 25
  const infrastructureRisk = market.infrastructureDependencyIndex * 20

  const dignityRisk = (1 - market.dignityComplianceIndex) * 30

  // Outlawed markets automatically increase risk
  const outlawRisk =
    (market.gamblingAllowed ? 40 : 0) +
    (market.predictionMarketsAllowed ? 40 : 0) +
    (market.speculationAllowed ? 30 : 0)

  let riskScore =
    extractionRisk +
    corruptionRisk +
    liquidityRisk +
    velocityRisk +
    ecologicalRisk +
    infrastructureRisk +
    dignityRisk +
    outlawRisk

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
      extractionRisk,
      corruptionRisk,
      liquidityRisk,
      velocityRisk,
      ecologicalRisk,
      infrastructureRisk,
      dignityRisk,
      outlawRisk,
    },
  }
}