// engine/commons/CommonsStabilityEngine.ts

import { CommonsProfile } from "../../core/pillars/commons/CommonsProfile"
import { computeCommonsRisk } from "./CommonsRiskEngine"

export function computeCommonsStability(commons: CommonsProfile) {
  const risk = computeCommonsRisk(commons)

  const stabilityFactor = commons.stabilityIndex * 40
  const regenerationFactor = commons.regenerationIndex * 35
  const stewardshipFactor = commons.stewardshipIndex * 30
  const dignityFactor = commons.dignityIndex * 30

  const extractionPenalty = commons.extractionPressureIndex * 30
  const depletionPenalty = commons.depletionIndex * 30
  const pollutionPenalty = commons.pollutionIndex * 25
  const collapsePenalty = commons.collapseRiskIndex * 35

  const dependencyPenalty =
    commons.ecologicalDependencyIndex * 20 +
    commons.infrastructureDependencyIndex * 20 +
    commons.populationDependencyIndex * 20 +
    commons.governanceDependencyIndex * 20 +
    commons.marketDependencyIndex * 20

  let stabilityScore =
    stabilityFactor +
    regenerationFactor +
    stewardshipFactor +
    dignityFactor -
    extractionPenalty -
    depletionPenalty -
    pollutionPenalty -
    collapsePenalty -
    dependencyPenalty -
    risk.riskScore * 0.2

  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      stabilityFactor,
      regenerationFactor,
      stewardshipFactor,
      dignityFactor,
      extractionPenalty,
      depletionPenalty,
      pollutionPenalty,
      collapsePenalty,
      dependencyPenalty,
      riskScore: risk.riskScore,
    },
  }
}