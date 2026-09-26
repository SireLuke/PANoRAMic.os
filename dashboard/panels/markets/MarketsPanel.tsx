import React from "react"

export function MarketsPanel({ data }) {
  return (
    <div>
      <h2>Cooperative Markets</h2>
      <p>Cooperative Market Share: {data.cooperativeMarketShare}</p>
      <p>Non-Extractive Trade: {data.nonExtractiveTradeIndex}</p>
      <p>Price Stability: {data.priceStabilityIndex}</p>
      <p>Access to Essentials: {data.accessToEssentialsIndex}</p>
      <p>PAR Flow Through Markets: {data.parFlowThroughMarkets}</p>
      <p>Market Resilience: {data.marketResilienceIndex}</p>
    </div>
  )
}
