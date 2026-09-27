// engine/par/parLiquidityEngine.ts

export function computeParLiquidity({
  par,
  markets,
  infrastructure,
  microAi,
  nodes,
}: {
  par: any
  markets: any
  infrastructure: any
  microAi: any
  nodes: any[]
}) {
  // Base liquidity from velocity + mint rate
  let liquidity = par.parVelocity * 0.6 + par.parMintRate * 0.0001

  // Cooperative markets increase liquidity
  liquidity += markets.cooperativeMarketShare * 0.3

  // Extraction pressure reduces liquidity
  liquidity -= markets.extractivePressureIndex * 0.4

  // Infrastructure resilience boosts liquidity
  liquidity += infrastructure.resilienceIndex * 0.2

  // Micro-AI coverage improves flow efficiency
  liquidity += microAi.microAiCoverageIndex * 0.25

  // Node connectivity improves distribution
  const nodeConnectivityBoost =
    nodes.reduce((sum, n) => sum + n.nodeConnectivityIndex, 0) * 0.02
  liquidity += nodeConnectivityBoost

  // Bound liquidity between 0.1 and 5.0
  liquidity = Math.max(0.1, Math.min(liquidity, 5.0))

  return liquidity
}
