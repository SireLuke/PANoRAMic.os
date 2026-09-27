// engine/gep/globalSynthesisEngine.ts

import { NationProfile } from "../../core/pillars/gep/NationProfile"
import { CurrencyProfile } from "../../core/pillars/gep/Currency"
import { TradeFlow } from "../../core/pillars/gep/TradeFlows"
import { computeGlobalEconomics } from "./globalEconomicsEngine"
import { computeGlobalRisk } from "./globalRiskEngine"
import { computeGlobalStability } from "./globalStabilityEngine"

export function computeGlobalSynthesis({
  nations,
  currencies,
  tradeFlows,
}: {
  nations: NationProfile[]
  currencies: CurrencyProfile[]
  tradeFlows: TradeFlow[]
}) {
  const economics = computeGlobalEconomics({ nations, currencies, tradeFlows })
  const risk = computeGlobalRisk({ nations, currencies, tradeFlows })
  const stability = computeGlobalStability({ nations, currencies, tradeFlows })

  // Additional global indicators
  const avgConflictRisk =
    nations.reduce((sum, n) => sum + n.conflictRiskIndex, 0) /
    nations.length

  const avgEcologicalFootprint =
    nations.reduce((sum, n) => sum + n.ecologicalFootprint, 0) /
    nations.length

  const avgInfrastructureResilience =
    nations.reduce((sum, n) => sum + n.infrastructureResilience, 0) /
    nations.length

  // Synthesis score combines:
  // - global economics
  // - global stability
  // - inverse global risk
  // - conflict risk
  // - ecological footprint
  // - infrastructure resilience

  let synthesisScore =
    economics.globalEconomicsScore * 0.35 +
    stability.stabilityScore * 0.35 +
    (100 - risk.globalRiskScore) * 0.3 +
    (1 - avgConflictRisk) * 20 +
    (1 - avgEcologicalFootprint) * 20 +
    avgInfrastructureResilience * 20

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
      economicsScore: economics.globalEconomicsScore,
      stabilityScore: stability.stabilityScore,
      riskScore: risk.globalRiskScore,
      avgConflictRisk,
      avgEcologicalFootprint,
      avgInfrastructureResilience,
    },
  }
}