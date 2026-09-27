// engine/markets/marketEnforcementEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"
import { computeMarketRisk } from "./marketRiskEngine"
import { computeMarketStability } from "./marketStabilityEngine"

export function enforceMarketRules(market: MarketProfile) {
  const interventions: string[] = []

  // Outlawed markets
  if (market.gamblingAllowed) {
    interventions.push("Gambling market detected — disabling gambling.")
    market.gamblingAllowed = false
  }

  if (market.predictionMarketsAllowed) {
    interventions.push("Prediction market detected — disabling prediction markets.")
    market.predictionMarketsAllowed = false
  }

  if (market.speculationAllowed) {
    interventions.push("Speculative market detected — disabling speculation.")
    market.speculationAllowed = false
  }

  // Extraction pressure enforcement
  if (market.extractivePressureIndex > 0.7) {
    interventions.push("High extraction pressure — applying extraction dampening.")
    market.extractivePressureIndex *= 0.85
  }

  // Dignity enforcement
  if (market.dignityComplianceIndex < 0.5) {
    interventions.push("Dignity violation — boosting dignity compliance.")
    market.dignityComplianceIndex = Math.min(
      1,
      market.dignityComplianceIndex + 0.2
    )
  }

  // Corruption enforcement
  if (market.corruptionIndex > 0.5) {
    interventions.push("High corruption detected — reducing corruption.")
    market.corruptionIndex *= 0.8
  }

  // Ecological enforcement
  if (market.ecologicalImpactIndex > 0.6) {
    interventions.push("High ecological impact — reducing ecological footprint.")
    market.ecologicalImpactIndex *= 0.85
  }

  // Infrastructure enforcement
  if (market.infrastructureDependencyIndex > 0.7) {
    interventions.push("High infrastructure dependency — reducing dependency.")
    market.infrastructureDependencyIndex *= 0.85
  }

  // Flow enforcement (liquidity + velocity)
  if (market.liquidity < 0.4) {
    interventions.push("Liquidity collapse — boosting liquidity.")
    market.liquidity *= 1.2
  }

  if (market.velocity < 0.4) {
    interventions.push("Velocity collapse — boosting velocity.")
    market.velocity *= 1.2
  }

  // Recompute stability + risk after enforcement
  const stability = computeMarketStability(market)
  const risk = computeMarketRisk(market)

  return {
    interventions,
    updatedMarket: market,
    stability,
    risk,
  }
}