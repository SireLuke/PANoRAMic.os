// engine/rights/RightsSynthesisEngine.ts

import { RightsProfile } from "../../core/pillars/rights/RightsProfile"
import { computeRightsRisk } from "./RightsRiskEngine"
import { computeRightsStability } from "./RightsStabilityEngine"

export function computeRightsSynthesis(rights: RightsProfile) {
  const risk = computeRightsRisk(rights)
  const stability = computeRightsStability(rights)

  // Synthesis indicators
  const dignityFactor = rights.dignityIndex * 30
  const autonomyFactor = rights.autonomyIndex * 30
  const safetyFactor = rights.safetyIndex * 25
  const accessFactor = rights.accessIndex * 25
  const fairnessFactor = rights.fairnessIndex * 25

  const predatoryPenalty = rights.predatoryPressureIndex * 30
  const exclusionPenalty = rights.exclusionIndex * 25
  const exploitationPenalty = rights.exploitationIndex * 25
  const collapsePenalty = rights.collapseRiskIndex * 30

  const dependencyPenalty =
    rights.governanceDependencyIndex * 20 +
    rights.marketDependencyIndex * 20 +
    rights.workforceDependencyIndex * 20 +
    rights.infrastructureDependencyIndex * 20 +
    rights.ecologicalDependencyIndex * 20

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    dignityFactor +
    autonomyFactor +
    safetyFactor +
    accessFactor +
    fairnessFactor -
    predatoryPenalty -
    exclusionPenalty -
    exploitationPenalty -
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
      dignityFactor,
      autonomyFactor,
      safetyFactor,
      accessFactor,
      fairnessFactor,
      predatoryPenalty,
      exclusionPenalty,
      exploitationPenalty,
      collapsePenalty,
      dependencyPenalty,
    },
  }
}