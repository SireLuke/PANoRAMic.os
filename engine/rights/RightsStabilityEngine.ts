// engine/rights/RightsStabilityEngine.ts

import { RightsProfile } from "../../core/pillars/rights/RightsProfile"
import { computeRightsRisk } from "./RightsRiskEngine"

export function computeRightsStability(rights: RightsProfile) {
  const risk = computeRightsRisk(rights)

  // Stability factors
  const dignityFactor = rights.dignityIndex * 40
  const autonomyFactor = rights.autonomyIndex * 35
  const safetyFactor = rights.safetyIndex * 35
  const accessFactor = rights.accessIndex * 30
  const fairnessFactor = rights.fairnessIndex * 30

  // Penalties
  const predatoryPenalty = rights.predatoryPressureIndex * 30
  const exclusionPenalty = rights.exclusionIndex * 25
  const exploitationPenalty = rights.exploitationIndex * 25
  const collapsePenalty = rights.collapseRiskIndex * 35

  const dependencyPenalty =
    rights.governanceDependencyIndex * 20 +
    rights.marketDependencyIndex * 20 +
    rights.workforceDependencyIndex * 20 +
    rights.infrastructureDependencyIndex * 20 +
    rights.ecologicalDependencyIndex * 20

  let stabilityScore =
    dignityFactor +
    autonomyFactor +
    safetyFactor +
    accessFactor +
    fairnessFactor -
    predatoryPenalty -
    exclusionPenalty -
    exploitationPenalty -
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
      riskScore: risk.riskScore,
    },
  }
}