// engine/governance/GovernanceSynthesisEngine.ts

import { GovernanceProfile } from "../../core/pillars/governance/GovernanceProfile"
import { computeGovernanceRisk } from "./GovernanceRiskEngine"
import { computeGovernanceStability } from "./GovernanceStabilityEngine"

export function computeGovernanceSynthesis(gov: GovernanceProfile) {
  const risk = computeGovernanceRisk(gov)
  const stability = computeGovernanceStability(gov)

  // Synthesis indicators
  const stabilityFactor = gov.stabilityIndex * 30
  const coordinationFactor = gov.coordinationIndex * 30
  const consensusFactor = gov.consensusIndex * 25
  const dignityFactor = gov.dignityIndex * 25
  const responsivenessFactor = gov.responsivenessIndex * 20

  const conflictPenalty = gov.conflictIndex * 30
  const collapsePenalty = gov.collapseRiskIndex * 30

  const dependencyPenalty =
    gov.ecologicalDependencyIndex * 20 +
    gov.infrastructureDependencyIndex * 20 +
    gov.workforceDependencyIndex * 20 +
    gov.marketDependencyIndex * 20

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    stabilityFactor +
    coordinationFactor +
    consensusFactor +
    dignityFactor +
    responsivenessFactor -
    conflictPenalty -
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
      coordinationFactor,
      consensusFactor,
      dignityFactor,
      responsivenessFactor,
      conflictPenalty,
      collapsePenalty,
      dependencyPenalty,
    },
  }
}