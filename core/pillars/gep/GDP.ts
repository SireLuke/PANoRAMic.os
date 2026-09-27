// core/pillars/gep/GDP.ts

export interface NationGDP {
  nation: string
  gdp: number            // total GDP in USD
  gdpPerCapita: number   // GDP per person
  population: number
  currency: string
  inflationRate: number
  ppp: number            // purchasing power parity
  sovereignDebt: number  // national debt in USD
  tradeBalance: number   // exports - imports
  resourceExports: number
  resourceImports: number
  ecologicalFootprint: number
  infrastructureResilience: number
}

export function computeGlobalGDP(nations: NationGDP[]) {
  const totalGDP = nations.reduce((sum, n) => sum + n.gdp, 0)
  const avgGDPPerCapita =
    nations.reduce((sum, n) => sum + n.gdpPerCapita, 0) / nations.length

  const globalInflation =
    nations.reduce((sum, n) => sum + n.inflationRate, 0) / nations.length

  const globalPPP =
    nations.reduce((sum, n) => sum + n.ppp, 0) / nations.length

  const globalDebt = nations.reduce((sum, n) => sum + n.sovereignDebt, 0)

  const globalTradeBalance = nations.reduce(
    (sum, n) => sum + n.tradeBalance,
    0
  )

  const globalEcology =
    nations.reduce((sum, n) => sum + n.ecologicalFootprint, 0) /
    nations.length

  const globalInfrastructure =
    nations.reduce((sum, n) => sum + n.infrastructureResilience, 0) /
    nations.length

  return {
    totalGDP,
    avgGDPPerCapita,
    globalInflation,
    globalPPP,
    globalDebt,
    globalTradeBalance,
    globalEcology,
    globalInfrastructure,
  }
}
