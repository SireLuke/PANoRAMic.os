// engine/gep/globalRiskEngine.ts

import { NationProfile } from "../../core/pillars/gep/NationProfile"
import { CurrencyProfile } from "../../core/pillars/gep/Currency"
import { TradeFlow } from "../../core/pillars/gep/TradeFlows"
import { computeSovereignRisk } from "../../core/pillars/gep/SovereignRisk"
import { computeNationTradeSummary } from "../../core/pillars/gep/TradeFlows"

export function computeGlobalRisk({
  nations,
  currencies,
  tradeFlows,
}: {
  nations: NationProfile[]
  currencies: CurrencyProfile[]
  tradeFlows: TradeFlow[]
}) {
  const sovereignRisks = nations.map(nation => {
    const currency = currencies.find(c => c.code === nation.currency)
    const tradeSummary = computeNationTradeSummary(nation.name, tradeFlows)

    return computeSovereignRisk(nation, currency!, {
      strategicDependencyIndex: tradeSummary.strategicDependencyIndex,
      tradeStabilityIndex: tradeSummary.tradeStabilityIndex,
    })
  })

  // Average sovereign risk
  const avgSovereignRisk =
    sovereignRisks.reduce((sum, r) => sum + r.riskScore, 0) /
    sovereignRisks.length

  // Currency risk
  const avgCurrencyRisk =
    currencies.reduce((sum, c) => sum + c.currencyRiskIndex, 0) /
    currencies.length

  // Trade dependency risk
  const tradeDependencyRisk =
    tradeFlows.reduce(
      (sum, f) => sum + f.strategicImportance * f.importsValue,
      0
    ) / (tradeFlows.length + 1)

  // Conflict risk
  const avgConflictRisk =
    nations.reduce((sum, n) => sum + n.conflictRiskIndex, 0) /
    nations.length

  // Ecological risk
  const avgEcologicalRisk =
    nations.reduce((sum, n) => sum + n.ecologicalFootprint, 0) /
    nations.length

  // Infrastructure risk
  const avgInfrastructureRisk =
    nations.reduce(
      (sum, n) => sum + (1 - n.infrastructureResilience),
      0
    ) / nations.length

  // Combine all risks
  let globalRiskScore =
    avgSovereignRisk * 0.4 +
    avgCurrencyRisk * 20 +
    tradeDependencyRisk * 0.000001 +
    avgConflictRisk * 40 +
    avgEcologicalRisk * 30 +
    avgInfrastructureRisk * 30

  // Normalize
  globalRiskScore = Math.max(0, Math.min(globalRiskScore, 100))

  // Mode classification
  let globalRiskMode = "low"
  if (globalRiskScore >= 75) globalRiskMode = "critical"
  else if (globalRiskScore >= 50) globalRiskMode = "high"
  else if (globalRiskScore >= 25) globalRiskMode = "moderate"

  return {
    globalRiskScore,
    globalRiskMode,
    breakdown: {
      avgSovereignRisk,
      avgCurrencyRisk,
      tradeDependencyRisk,
      avgConflictRisk,
      avgEcologicalRisk,
      avgInfrastructureRisk,
    },
    sovereignRisks,
  }
}