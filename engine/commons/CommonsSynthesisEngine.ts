// engine/commons/CommonsSynthesisEngine.ts

import { CommonsProfile } from "../../core/pillars/commons/CommonsProfile"
import { computeCommonsRisk } from "./CommonsRiskEngine"
import { computeCommonsStability } from "./CommonsStabilityEngine"

export function computeCommonsSynthesis(commons: CommonsProfile) {
  const risk = computeCommonsRisk(commons)
  const stability = computeCommonsStability(commons)

  const stabilityFactor = commons.stabilityIndex * 30
  const regenerationFactor = commons.regenerationIndex * 30
  const stewardshipFactor = commons.stewardshipIndex * 25
  const dignityFactor = commons.dignityIndex * 25

  const extractionPenalty = commons.extractionPressureIndex * 30
  const depletionPenalty = commons.depletionIndex * 30
  const pollutionPenalty = commons.pollutionIndex * 25
  const collapsePenalty = commons.collapseRiskIndex * 30

  const dependencyPenalty =
    commons.ecologicalDependencyIndex * 20 +
    commons.infrastructureDependencyIndex * 20 +
    commons.populationDependencyIndex * 20 +
    commons.governanceDependencyIndex * 20 +
    commons.marketDependencyIndex * 20

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    stabilityFactor +
    regenerationFactor +
    stewardshipFactor +
    dignityFactor -
    extractionPenalty -
    depletionPenalty -
    pollutionPenalty -
    collapsePenalty -
    dependencyPenalty

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
      regenerationFactor,
      stewardshipFactor,
      dignityFactor,
      extractionPenalty,
      depletionPenalty,
      pollutionPenalty,
      collapsePenalty,
      dependencyPenalty,
    },
  }
}