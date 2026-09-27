// core/pillars/population/PopulationProfile.ts

export interface PopulationProfile {
  name: string

  // Core human metrics
  stabilityIndex: number            // 0–1
  riskIndex: number                 // 0–1
  resilienceIndex: number           // 0–1
  dignityIndex: number              // 0–1

  // Social metrics
  cohesionIndex: number             // 0–1
  conflictIndex: number             // 0–1
  stressIndex: number               // 0–1
  burnoutIndex: number              // 0–1

  // Systemic dependencies
  ecologicalDependencyIndex: number // 0–1
  infrastructureDependencyIndex: number // 0–1
  workforceDependencyIndex: number  // 0–1
  marketDependencyIndex: number     // 0–1
  governanceDependencyIndex: number // 0–1

  // Collapse metrics
  collapseRiskIndex: number         // 0–1
}

export function evaluatePopulationHealth(pop: PopulationProfile) {
  let healthScore =
    pop.stabilityIndex * 35 +
    pop.resilienceIndex * 30 +
    pop.cohesionIndex * 25 +
    pop.dignityIndex * 25

  healthScore -= pop.riskIndex * 25
  healthScore -= pop.conflictIndex * 25
  healthScore -= pop.stressIndex * 20
  healthScore -= pop.burnoutIndex * 20
  healthScore -= pop.collapseRiskIndex * 30

  healthScore -= pop.ecologicalDependencyIndex * 15
  healthScore -= pop.infrastructureDependencyIndex * 15
  healthScore -= pop.workforceDependencyIndex * 15
  healthScore -= pop.marketDependencyIndex * 15
  healthScore -= pop.governanceDependencyIndex * 15

  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}