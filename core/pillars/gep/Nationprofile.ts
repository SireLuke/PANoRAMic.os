// core/pillars/gep/NationProfile.ts

export interface NationProfile {
  name: string
  isoCode: string
  population: number
  gdp: number
  gdpPerCapita: number
  currency: string
  inflationRate: number
  ppp: number
  sovereignDebt: number
  tradeBalance: number
  resourceExports: number
  resourceImports: number
  ecologicalFootprint: number
  infrastructureResilience: number
  corruptionIndex: number        // 0–1 corruption score
  stabilityIndex: number         // 0–1 national stability
  conflictRiskIndex: number      // 0–1 conflict probability
}

export function evaluateNationProfile(nation: NationProfile) {
  // Economic health
  const economicHealth =
    nation.gdpPerCapita * 0.00002 +
    (1 - nation.inflationRate / 100) * 20 +
    (1 - nation.sovereignDebt / (nation.gdp + 1)) * 20

  // Trade health
  const tradeHealth =
    (nation.tradeBalance / (nation.gdp + 1)) * 30 +
    (nation.resourceExports - nation.resourceImports) * 0.00001

  // Ecological health
  const ecologicalHealth =
    (1 - nation.ecologicalFootprint) * 30

  // Infrastructure health
  const infrastructureHealth =
    nation.infrastructureResilience * 40

  // Governance health
  const governanceHealth =
    (1 - nation.corruptionIndex) * 30 +
    nation.stabilityIndex * 30

  // Conflict risk reduces health
  const conflictPenalty =
    nation.conflictRiskIndex * 40

  // Combine all components
  let nationHealthScore =
    economicHealth +
    tradeHealth +
    ecologicalHealth +
    infrastructureHealth +
    governanceHealth -
    conflictPenalty

  // Normalize to 0–100
  nationHealthScore = Math.max(0, Math.min(nationHealthScore, 100))

  // Mode classification
  let nationMode = "stable"
  if (nationHealthScore < 40) nationMode = "critical"
  else if (nationHealthScore < 70) nationMode = "unstable"

  return {
    nationHealthScore,
    nationMode,
    breakdown: {
      economicHealth,
      tradeHealth,
      ecologicalHealth,
      infrastructureHealth,
      governanceHealth,
      conflictPenalty,
    },
  }
}