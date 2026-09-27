// engine/population/PopulationRiskEngine.ts

import { PopulationProfile } from "../../core/pillars/population/PopulationProfile"

export function computePopulationRisk(pop: PopulationProfile) {
  // Risk factors
  const conflictRisk = pop.conflictIndex * 35
  const stabilityRisk = (1 - pop.stabilityIndex) * 35
  const resilienceRisk = (1 - pop.resilienceIndex) * 30
  const dignityRisk = (1 - pop.dignityIndex) * 30

  const stressRisk = pop.stressIndex * 30
  const burnoutRisk = pop.burnoutIndex * 30

  const dependencyRisk =
    pop.ecologicalDependencyIndex * 20 +
    pop.infrastructureDependencyIndex * 20 +
    pop.workforceDependencyIndex * 20 +
    pop.marketDependencyIndex * 20 +
    pop.governanceDependencyIndex * 20

  const collapseRisk = pop.collapseRiskIndex * 40

  let riskScore =
    conflictRisk +
    stabilityRisk +
    resilienceRisk +
    dignityRisk +
    stressRisk +
    burnoutRisk +
    dependencyRisk +
    collapseRisk

  // Normalize
  riskScore = Math.max(0, Math.min(riskScore, 100))

  let riskMode = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    riskScore,
    riskMode,
    breakdown: {
      conflictRisk,
      stabilityRisk,
      resilienceRisk,
      dignityRisk,
      stressRisk,
      burnoutRisk,
      dependencyRisk,
      collapseRisk,
    },
  }
}