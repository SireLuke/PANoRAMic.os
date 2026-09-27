// engine/par/PARStabilityEngine.ts

import { PARProfile } from "../../core/pillars/par/PARProfile"
import { computePARRisk } from "./PARRiskEngine"

export function computePARStability(par: PARProfile) {
  const risk = computePARRisk(par)

  // Stability factors
  const stabilityFactor = par.stabilityIndex * 40
  const liquidityFactor = par.liquidityIndex * 35
  const dignityFactor = par.dignityIndex * 30

  const backingFactor =
    par.ecologicalBackingIndex * 25 +
    par.infrastructureBackingIndex * 25 +
    par.workforceBackingIndex * 25 +
    par.marketBackingIndex * 25

  // Penalties
  const volatilityPenalty = par.volatilityIndex * 30
  const collapsePenalty = par.collapseRiskIndex * 35

  let stabilityScore =
    stabilityFactor +
    liquidityFactor +
    dignityFactor +
    backingFactor -
    volatilityPenalty -
    collapsePenalty -
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
      liquidityFactor,
      dignityFactor,
      backingFactor,
      volatilityPenalty,
      collapsePenalty,
      riskScore: risk.riskScore,
    },
  }
}