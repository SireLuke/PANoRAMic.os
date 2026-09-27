// engine/governance/GovernanceStabilityEngine.ts

import { GovernanceProfile } from "../../core/pillars/governance/GovernanceProfile"
import { computeGovernanceRisk } from "./GovernanceRiskEngine"

export function computeGovernanceStability(gov: GovernanceProfile) {
  const risk = computeGovernanceRisk(gov)

  // Stability factors
  const stabilityFactor = gov.stabilityIndex * 40
  const coordinationFactor = gov.coordinationIndex * 35
  const consensusFactor = gov.consensusIndex * 30
  const dignityFactor = gov.dignityIndex * 30
  const responsivenessFactor = gov.responsivenessIndex * 25

  // Penalties
  const conflictPenalty = gov.conflictIndex * 30
  const collapsePenalty = gov.collapseRiskIndex * 35

  const dependencyPenalty =
    gov.ecologicalDependencyIndex * 20 +
    gov.infrastructureDependencyIndex * 20 +
    gov.workforceDependencyIndex * 20 +
    gov.marketDependencyIndex * 20

  let stabilityScore =
    stabilityFactor +
    coordinationFactor +
    consensusFactor +
    dignityFactor +
    responsivenessFactor -
    conflictPenalty -
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
      coordinationFactor,
      consensusFactor,
      dignityFactor,
      responsivenessFactor,
      conflictPenalty,
      collapsePenalty,
      dependencyPenalty,
      riskScore: risk.riskScore,
    },
  }
}