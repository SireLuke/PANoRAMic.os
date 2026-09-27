// engine/gep/globalEconomicsEngine.ts

import { NationProfile } from "../../core/pillars/gep/NationProfile"
import { CurrencyProfile } from "../../core/pillars/gep/Currency"
import { TradeFlow } from "../../core/pillars/gep/TradeFlows"
import { computeSovereignRisk } from "../../core/pillars/gep/SovereignRisk"
import { computeGlobalGDP } from "../../core/pillars/gep/GDP"
import { computeGlobalCurrencyMetrics } from "../../core/pillars/gep/Currency"
import { computeNationTradeSummary, computeGlobalTradeMetrics } from "../../core/pillars/gep/TradeFlows"

export function computeGlobalEconomics({
  nations,
  currencies,
  tradeFlows,
}: {
  nations: NationProfile[]
  currencies: CurrencyProfile[]
  tradeFlows: TradeFlow[]
}) {
  // Global GDP metrics
  const gdpMetrics = computeGlobalGDP(nations)

  // Global currency metrics
  const currencyMetrics = computeGlobalCurrencyMetrics(currencies)

  // Global trade metrics
  const tradeMetrics = computeGlobalTradeMetrics(tradeFlows)

  // Sovereign risk for each nation
  const sovereignRiskReports = nations.map(nation => {
    const currency = currencies.find(c => c.code === nation.currency)
    const tradeSummary = computeNationTradeSummary(nation.name, tradeFlows)

    return computeSovereignRisk(nation, currency!, {
      strategicDependencyIndex: tradeSummary.strategicDependencyIndex,
      tradeStabilityIndex: tradeSummary.tradeStabilityIndex,
    })
  })

  // Average sovereign risk
  const avgSovereignRisk =
    sovereignRiskReports.reduce((sum, r) => sum + r.riskScore, 0) /
    sovereignRiskReports.length

  // Global economics score (0–100)
  let globalEconomicsScore =
    gdpMetrics.totalGDP * 0.0000000001 +
    gdpMetrics.avgGDPPerCapita * 0.00002 +
    (1 - currencyMetrics.avgInflation / 100) * 20 +
    (1 - avgSovereignRisk / 100) * 30 +
    (1 - tradeMetrics.avgStrategicImportance) * 20

  // Normalize
  globalEconomicsScore = Math.max(0, Math.min(globalEconomicsScore, 100))

  // Mode classification
  let globalEconomicsMode = "stable"
  if (globalEconomicsScore < 40) globalEconomicsMode = "critical"
  else if (globalEconomicsScore < 70) globalEconomicsMode = "unstable"

  return {
    globalEconomicsScore,
    globalEconomicsMode,
    gdpMetrics,
    currencyMetrics,
    tradeMetrics,
    sovereignRiskReports,
  }
}