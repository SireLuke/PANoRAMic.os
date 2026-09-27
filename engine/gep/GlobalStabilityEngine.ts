// engine/gep/globalStabilityEngine.ts

import { NationProfile } from "../../core/pillars/gep/NationProfile"
import { CurrencyProfile } from "../../core/pillars/gep/Currency"
import { TradeFlow } from "../../core/pillars/gep/TradeFlows"
import { computeGlobalEconomics } from "./globalEconomicsEngine"
import { computeGlobalRisk } from "./globalRiskEngine"

export function computeGlobalStability({
  nations,
  currencies,
  tradeFlows,
}: {
  nations: NationProfile[]
  currencies: CurrencyProfile[]
  tradeFlows: TradeFlow[]
}) {
  // Pull global economics + risk
  const economics = computeGlobalEconomics({ nations, currencies, tradeFlows })
  const risk = computeGlobalRisk({ nations, currencies, tradeFlows })

  // Stability is influenced by:
  // - strong economics
  // - low risk
  // - stable currencies
  // - low conflict
  // - low ecological footprint
  // - resilient infrastructure

  const avgCurrencyStability =
    currencies.reduce((sum, c) => sum + c.stabilityIndex, 0) /
    currencies.length

  const avgConflictRisk =
    nations.reduce((sum, n) => sum + n.conflictRiskIndex, 0) /
    nations.length

  const avgEcologicalFootprint =
    nations.reduce((sum, n) => sum + n.ecologicalFootprint, 0) /
    nations.length

  const avgInfrastructureResilience =
    nations.reduce((sum, n) => sum + n.infrastructureResilience, 0) /
    nations.length

  // Compute stability score
  let stabilityScore =
    economics.globalEconomicsScore * 0.4 +
    (100 - risk.globalRiskScore) * 0.3 +
    avgCurrencyStability * 20 +
    (1 - avgConflictRisk) * 20 +
    (1 - avgEcologicalFootprint) * 20 +
    avgInfrastructureResilience * 20

  // Normalize
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  // Mode classification
  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      economicsScore: economics.globalEconomicsScore,
      riskScore: risk.globalRiskScore,
      avgCurrencyStability,
      avgConflictRisk,
      avgEcologicalFootprint,
      avgInfrastructureResilience,
    },
  }
}