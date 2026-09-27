// core/pillars/markets/MarketProfile.ts

export interface MarketProfile {
  name: string
  marketType: "resource" | "labor" | "cooperative" | "technology" | "energy" | "food" | "transport" | "finance"
  
  // Stability + extraction
  stabilityIndex: number        // 0–1
  extractivePressureIndex: number // 0–1

  // Flow metrics
  liquidity: number             // 0–2 normalized
  velocity: number              // 0–2 normalized

  // Dignity + ethics
  dignityComplianceIndex: number // 0–1
  corruptionIndex: number        // 0–1

  // Ecology + infrastructure
  ecologicalImpactIndex: number  // 0–1
  infrastructureDependencyIndex: number // 0–1

  // Outlawed market types
  gamblingAllowed: boolean
  predictionMarketsAllowed: boolean
  speculationAllowed: boolean
}

export function evaluateMarketHealth(market: MarketProfile) {
  // Base health
  let healthScore =
    market.stabilityIndex * 40 +
    (1 - market.extractivePressureIndex) * 30 +
    market.dignityComplianceIndex * 20 +
    (1 - market.corruptionIndex) * 20

  // Ecology penalty
  healthScore -= market.ecologicalImpactIndex * 20

  // Infrastructure penalty
  healthScore -= market.infrastructureDependencyIndex * 10

  // Outlawed markets automatically penalized
  if (market.gamblingAllowed) healthScore -= 30
  if (market.predictionMarketsAllowed) healthScore -= 30
  if (market.speculationAllowed) healthScore -= 20

  // Normalize
  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}