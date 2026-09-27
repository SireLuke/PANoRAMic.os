// engine/markets/MarketStabilityEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"
import { computeMarketRisk } from "./MarketRiskEngine"

export function computeMarketStability(market: MarketProfile) {
  const risk = computeMarketRisk(market)

  // Stability factors
  const stabilityFactor = market.stabilityIndex * 40
  const resilienceFactor = market.resilienceIndex * 35
  const liquidityFactor = market.liquidityIndex * 30
  const dignityFactor = market.dignityComplianceIndex * 25

  // Penalties
  const volatilityPenalty = market.volatilityIndex * 30
  const predatoryPenalty = market.predatoryPressureIndex * 35
  const loadPenalty = market.loadIndex * 25

  const dependencyPenalty =
    market.ecologicalDependencyIndex * 20 +
    market.infrastructureDependencyIndex * 20 +
    market.workforceDependencyIndex * 20

  const collapsePenalty = market.collapseRiskIndex * 35

  let stabilityScore =
    stabilityFactor +
    resilienceFactor +
    liquidityFactor +
    dignityFactor -
    volatilityPenalty -
    predatoryPenalty -
    loadPenalty -
    dependencyPenalty -
    collapsePenalty -
    risk.riskScore * 0.2

  // Normalize
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      stabilityFactor,
      resilienceFactor,
      liquidityFactor,
      dignityFactor,
      volatilityPenalty,
      predatoryPenalty,
      loadPenalty,
      dependencyPenalty,
      collapsePenalty,
      riskScore: risk.riskScore,
    },
  }
}