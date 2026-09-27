// engine/markets/marketSynthesisEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"
import { computeMarketStability } from "./marketStabilityEngine"
import { computeMarketRisk } from "./marketRiskEngine"

export function computeMarketSynthesis(market: MarketProfile) {
  const stability = computeMarketStability(market)
  const risk = computeMarketRisk(market)

  // Additional synthesis indicators
  const dignityFactor = market.dignityComplianceIndex * 25
  const extractionPenalty = market.extractivePressureIndex * 25
  const ecologyPenalty = market.ecologicalImpactIndex * 20
  const infrastructurePenalty = market.infrastructureDependencyIndex * 15

  const flowFactor =
    market.liquidity * 10 +
    market.velocity * 10

  // Outlawed markets automatically reduce synthesis
  const outlawPenalty =
    (market.gamblingAllowed ? 40 : 0) +
    (market.predictionMarketsAllowed ? 40 : 0) +
    (market.speculationAllowed ? 30 : 0)

  // Synthesis score combines:
  // - stability
  // - inverse risk
  // - dignity
  // - extraction
  // - ecology
  // - infrastructure
  // - flow
  // - outlaw penalties

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    dignityFactor +
    flowFactor -
    extractionPenalty -
    ecologyPenalty -
    infrastructurePenalty -
    outlawPenalty

  // Normalize
  synthesisScore = Math.max(0, Math.min(synthesisScore, 100))

  // Mode classification
  let synthesisMode = "stable"
  if (synthesisScore < 40) synthesisMode = "critical"
  else if (synthesisScore < 70) synthesisMode = "unstable"

  return {
    synthesisScore,
    synthesisMode,
    breakdown: {
      stabilityScore: stability.stabilityScore,
      riskScore: risk.riskScore,
      dignityFactor,
      extractionPenalty,
      ecologyPenalty,
      infrastructurePenalty,
      flowFactor,
      outlawPenalty,
    },
  }
}