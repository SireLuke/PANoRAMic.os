// engine/population/PopulationSynthesisEngine.ts

import { PopulationProfile } from "../../core/pillars/population/PopulationProfile"
import { computePopulationRisk } from "./PopulationRiskEngine"
import { computePopulationStability } from "./PopulationStabilityEngine"

export function computePopulationSynthesis(pop: PopulationProfile) {
  const risk = computePopulationRisk(pop)
  const stability = computePopulationStability(pop)

  // Synthesis indicators
  const stabilityFactor = pop.stabilityIndex * 30
  const resilienceFactor = pop.resilienceIndex * 30
  const cohesionFactor = pop.cohesionIndex * 25
  const dignityFactor = pop.dignityIndex * 25

  const conflictPenalty = pop.conflictIndex * 30
  const stressPenalty = pop.stressIndex * 25
  const burnoutPenalty = pop.burnoutIndex * 25
  const collapsePenalty = pop.collapseRiskIndex * 30

  const dependencyPenalty =
    pop.ecologicalDependencyIndex * 20 +
    pop.infrastructureDependencyIndex * 20 +
    pop.workforceDependencyIndex * 20 +
    pop.marketDependencyIndex * 20 +
    pop.governanceDependencyIndex * 20

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    stabilityFactor +
    resilienceFactor +
    cohesionFactor +
    dignityFactor -
    conflictPenalty -
    stressPenalty -
    burnoutPenalty -
    collapsePenalty -
    dependencyPenalty

  // Normalize
  synthesisScore = Math.max(0, Math.min(synthesisScore, 100))

  let synthesisMode = "stable"
  if (synthesisScore < 40) synthesisMode = "critical"
  else if (synthesisScore < 70) synthesisMode = "unstable"

  return {
    synthesisScore,
    synthesisMode,
    breakdown: {
      stabilityScore: stability.stabilityScore,
      riskScore: risk.riskScore,
      stabilityFactor,
      resilienceFactor,
      cohesionFactor,
      dignityFactor,
      conflictPenalty,
      stressPenalty,
      burnoutPenalty,
      collapsePenalty,
      dependencyPenalty,
    },
  }
}