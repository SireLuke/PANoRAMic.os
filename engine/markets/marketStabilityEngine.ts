// engine/markets/marketStabilityEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"

export function computeMarketStability(market: MarketProfile) {
  // Stability is influenced by:
  // - low extraction pressure
  // - high dignity compliance
  // - low corruption
  // - healthy liquidity + velocity
  // - low ecological impact
  // - low infrastructure dependency
  // - outlawed markets automatically destabilize

  const extractionFactor = (1 - market.extractivePressureIndex) * 30
  const dignityFactor = market.dignityComplianceIndex * 25
  const corruptionPenalty = market.corruptionIndex * 25

  const flowFactor =
    (market.liquidity * 10) +
    (market.velocity * 10)

  const ecologyPenalty = market.ecologicalImpactIndex * 20
  const infrastructurePenalty = market.infrastructureDependencyIndex * 15

  // Outlawed markets automatically destabilize
  const outlawPenalty =
    (market.gamblingAllowed ? 30 : 0) +
    (market.predictionMarketsAllowed ? 30 : 0) +
    (market.speculationAllowed ? 20 : 0)

  let stabilityScore =
    extractionFactor +
    dignityFactor +
    flowFactor -
    corruptionPenalty -
    ecologyPenalty -
    infrastructurePenalty -
    outlawPenalty

  // Normalize
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      extractionFactor,
      dignityFactor,
      corruptionPenalty,
      flowFactor,
      ecologyPenalty,
      infrastructurePenalty,
      outlawPenalty,
    },
  }
}