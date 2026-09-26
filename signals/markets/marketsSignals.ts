import { MarketsState } from "../../core/pillars/markets/MARKETS_STATE"

export function emitMarketsSignals(state: MarketsState) {
  return {
    cooperativeShare: state.cooperativeMarketShare,
    nonExtractiveTrade: state.nonExtractiveTradeIndex,
    priceStability: state.priceStabilityIndex,
    essentialsAccess: state.accessToEssentialsIndex,
    parFlow: state.parFlowThroughMarkets,
    resilience: state.marketResilienceIndex,
  }
}
