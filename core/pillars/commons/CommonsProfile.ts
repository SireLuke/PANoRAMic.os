// core/pillars/commons/CommonsProfile.ts

export interface CommonsProfile {
  name: string

  // Core commons metrics
  stabilityIndex: number            // 0–1
  riskIndex: number                 // 0–1
  regenerationIndex: number         // 0–1
  stewardshipIndex: number          // 0–1
  dignityIndex: number              // 0–1

  // Pressure metrics
  extractionPressureIndex: number   // 0–1
  depletionIndex: number            // 0–1
  pollutionIndex: number            // 0–1

  // Systemic dependencies
  ecologicalDependencyIndex: number // 0–1
  infrastructureDependencyIndex: number // 0–1
  populationDependencyIndex: number // 0–1
  governanceDependencyIndex: number // 0–1
  marketDependencyIndex: number     // 0–1

  // Collapse metrics
  collapseRiskIndex: number         // 0–1
}

export function evaluateCommonsHealth(commons: CommonsProfile) {
  let healthScore =
    commons.stewardshipIndex * 35 +
    commons.regenerationIndex * 30 +
    commons.stabilityIndex * 30 +
    commons.dignityIndex * 25

  healthScore -= commons.extractionPressureIndex * 30
  healthScore -= commons.depletionIndex * 30
  healthScore -= commons.pollutionIndex * 25
  healthScore -= commons.collapseRiskIndex * 30

  healthScore -= commons.ecologicalDependencyIndex * 15
  healthScore -= commons.infrastructureDependencyIndex * 15
  healthScore -= commons.populationDependencyIndex * 15
  healthScore -= commons.governanceDependencyIndex * 15
  healthScore -= commons.marketDependencyIndex * 15

  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}