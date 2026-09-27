// engine/par/PARSynthesisEngine.ts

import { PARProfile } from "../../core/pillars/par/PARProfile"
import { computePARRisk } from "./PARRiskEngine"
import { computePARStability } from "./PARStabilityEngine"

export function computePARSynthesis(par: PARProfile) {
  const risk = computePARRisk(par)
  const stability = computePARStability(par)

  // Synthesis indicators
  const stabilityFactor = par.stabilityIndex * 30
  const liquidityFactor = par.liquidityIndex * 25
  const dignityFactor = par.dignityIndex * 25

  const backingFactor =
    par.ecologicalBackingIndex * 25 +
    par.infrastructureBackingIndex * 25 +
    par.workforceBackingIndex * 25 +
    par.marketBackingIndex * 25

  const volatilityPenalty = par.volatilityIndex * 30
  const collapsePenalty = par.collapseRiskIndex * 30

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    stabilityFactor +
    liquidityFactor +
    dignityFactor +
    backingFactor -
    volatilityPenalty -
    collapsePenalty

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
      liquidityFactor,
      dignityFactor,
      backingFactor,
      volatilityPenalty,
      collapsePenalty,
    },
  }
}