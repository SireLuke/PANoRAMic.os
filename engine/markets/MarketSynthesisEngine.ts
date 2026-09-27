// engine/markets/MarketSynthesisEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"
import { computeMarketRisk } from "./MarketRiskEngine"
import { computeMarketStability } from "./MarketStabilityEngine"

export function computeMarketSynthesis(market: MarketProfile) {
  const risk = computeMarketRisk(market)
  const stability = computeMarketStability(market)

  // Additional synthesis indicators
  const stabilityFactor = market.stabilityIndex * 30
  const resilienceFactor = market.resilienceIndex * 30
  const liquidityFactor = market.liquidityIndex * 25
  const dignityFactor = market.dignityComplianceIndex * 25

  const volatilityPenalty = market.volatilityIndex * 30
  const predatoryPenalty = market.predatoryPressureIndex * 35
  const loadPenalty = market.loadIndex * 25

  const dependencyPenalty =
    market.ecologicalDependencyIndex * 20 +
    market.infrastructureDependencyIndex * 20 +
    market.workforceDependencyIndex * 20

  const collapsePenalty = market.collapseRiskIndex * 30

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    stabilityFactor +
    resilienceFactor +
    liquidityFactor +
    dignityFactor -
    volatilityPenalty -
    predatoryPenalty -
    loadPenalty -
    dependencyPenalty -
    collapsePenalty

  // Normalize
  synthesisScore = Math.max(0, Math.min(synthesisScore, 100))

  let synthesisMode = "stable"
  if (synthesisScore < 40) synthesisMode = "critical"
  else if (synthesisScore < 70) synthesisMode = "unstable"

  return {
    synthesisScore,
    synthesisMode,
    breakdown: {
      stabilityScore: stability.stabilityScore,
      riskScore: risk.riskScore,
      stabilityFactor,
      resilienceFactor,
      liquidityFactor,
      dignityFactor,
      volatilityPenalty,
      predatoryPenalty,
      loadPenalty,
      dependencyPenalty,
      collapsePenalty,
    },
  }
}