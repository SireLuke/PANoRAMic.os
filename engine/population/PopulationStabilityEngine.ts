// engine/population/PopulationStabilityEngine.ts

import { PopulationProfile } from "../../core/pillars/population/PopulationProfile"
import { computePopulationRisk } from "./PopulationRiskEngine"

export function computePopulationStability(pop: PopulationProfile) {
  const risk = computePopulationRisk(pop)

  // Stability factors
  const stabilityFactor = pop.stabilityIndex * 40
  const resilienceFactor = pop.resilienceIndex * 35
  const cohesionFactor = pop.cohesionIndex * 30
  const dignityFactor = pop.dignityIndex * 30

  // Penalties
  const conflictPenalty = pop.conflictIndex * 30
  const stressPenalty = pop.stressIndex * 25
  const burnoutPenalty = pop.burnoutIndex * 25
  const collapsePenalty = pop.collapseRiskIndex * 35

  const dependencyPenalty =
    pop.ecologicalDependencyIndex * 20 +
    pop.infrastructureDependencyIndex * 20 +
    pop.workforceDependencyIndex * 20 +
    pop.marketDependencyIndex * 20 +
    pop.governanceDependencyIndex * 20

  let stabilityScore =
    stabilityFactor +
    resilienceFactor +
    cohesionFactor +
    dignityFactor -
    conflictPenalty -
    stressPenalty -
    burnoutPenalty -
    collapsePenalty -
    dependencyPenalty -
    risk.riskScore * 0.2

  // Normalize
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      stabilityFactor,
      resilienceFactor,
      cohesionFactor,
      dignityFactor,
      conflictPenalty,
      stressPenalty,
      burnoutPenalty,
      collapsePenalty,
      dependencyPenalty,
      riskScore: risk.riskScore,
    },
  }
}