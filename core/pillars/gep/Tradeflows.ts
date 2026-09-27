// core/pillars/gep/TradeFlows.ts

export interface TradeFlow {
  fromNation: string
  toNation: string
  exportsValue: number       // USD value of exports
  importsValue: number       // USD value of imports
  resourceType: string       // e.g., oil, food, metals, tech
  strategicImportance: number // 0–1 importance score
}

export interface NationTradeSummary {
  nation: string
  totalExports: number
  totalImports: number
  netTradeBalance: number
  strategicDependencyIndex: number // 0–1 dependency score
  tradeStabilityIndex: number      // 0–1 stability score
}

export function computeNationTradeSummary(
  nation: string,
  flows: TradeFlow[]
): NationTradeSummary {
  const nationFlows = flows.filter(
    f => f.fromNation === nation || f.toNation === nation
  )

  const totalExports = nationFlows
    .filter(f => f.fromNation === nation)
    .reduce((sum, f) => sum + f.exportsValue, 0)

  const totalImports = nationFlows
    .filter(f => f.toNation === nation)
    .reduce((sum, f) => sum + f.importsValue, 0)

  const netTradeBalance = totalExports - totalImports

  // Strategic dependency: imports of high-importance resources
  const strategicImports = nationFlows
    .filter(f => f.toNation === nation)
    .reduce(
      (sum, f) => sum + f.importsValue * f.strategicImportance,
      0
    )

  const strategicExports = nationFlows
    .filter(f => f.fromNation === nation)
    .reduce(
      (sum, f) => sum + f.exportsValue * f.strategicImportance,
      0
    )

  const strategicDependencyIndex =
    strategicImports / (strategicExports + strategicImports + 1)

  // Trade stability: balanced flows + low dependency
  let tradeStabilityIndex =
    (1 - strategicDependencyIndex) * 0.6 +
    (netTradeBalance >= 0 ? 0.4 : 0.2)

  // Normalize
  tradeStabilityIndex = Math.max(0, Math.min(tradeStabilityIndex, 1))

  return {
    nation,
    totalExports,
    totalImports,
    netTradeBalance,
    strategicDependencyIndex,
    tradeStabilityIndex,
  }
}

export function computeGlobalTradeMetrics(flows: TradeFlow[]) {
  const totalGlobalExports = flows.reduce(
    (sum, f) => sum + f.exportsValue,
    0
  )

  const totalGlobalImports = flows.reduce(
    (sum, f) => sum + f.importsValue,
    0
  )

  const avgStrategicImportance =
    flows.reduce((sum, f) => sum + f.strategicImportance, 0) /
    flows.length

  return {
    totalGlobalExports,
    totalGlobalImports,
    avgStrategicImportance,
  }
}