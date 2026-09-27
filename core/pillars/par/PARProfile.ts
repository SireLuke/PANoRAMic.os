// core/pillars/par/PARProfile.ts

export interface PARProfile {
  name: string

  // Core currency metrics
  parValueIndex: number            // 0–1
  stabilityIndex: number           // 0–1
  riskIndex: number                // 0–1
  liquidityIndex: number           // 0–1
  dignityIndex: number             // 0–1

  // Backing metrics (renewable resource backing)
  ecologicalBackingIndex: number   // 0–1
  infrastructureBackingIndex: number // 0–1
  workforceBackingIndex: number    // 0–1
  marketBackingIndex: number       // 0–1

  // Systemic metrics
  volatilityIndex: number          // 0–1
  collapseRiskIndex: number        // 0–1
}

export function evaluatePARHealth(par: PARProfile) {
  let healthScore =
    par.parValueIndex * 30 +
    par.stabilityIndex * 30 +
    par.liquidityIndex * 20 +
    par.dignityIndex * 20

  healthScore += par.ecologicalBackingIndex * 20
  healthScore += par.infrastructureBackingIndex * 20
  healthScore += par.workforceBackingIndex * 20
  healthScore += par.marketBackingIndex * 20

  healthScore -= par.riskIndex * 25
  healthScore -= par.volatilityIndex * 25
  healthScore -= par.collapseRiskIndex * 30

  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}