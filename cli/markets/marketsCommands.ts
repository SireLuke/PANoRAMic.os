import { MarketsState } from "../../core/pillars/markets/MARKETS_STATE"
import { emitMarketsSignals } from "../../signals/markets/marketsSignals"

export function showMarkets(state: MarketsState) {
  const signals = emitMarketsSignals(state)

  console.log("Cooperative Markets Status")
  console.log("--------------------------")
  console.log("Cooperative Market Share:", signals.cooperativeShare)
  console.log("Non-Extractive Trade:", signals.nonExtractiveTrade)
  console.log("Price Stability:", signals.priceStability)
  console.log("Access to Essentials:", signals.essentialsAccess)
  console.log("PAR Flow Through Markets:", signals.parFlow)
  console.log("Market Resilience:", signals.resilience)
}
