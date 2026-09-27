// engine/workforce/WorkforceStabilityEngine.ts

import { WorkforceProfile } from "../../core/pillars/workforce/WorkforceProfile"
import { computeWorkforceRisk } from "./WorkforceRiskEngine"

export function computeWorkforceStability(work: WorkforceProfile) {
  const risk = computeWorkforceRisk(work)

  // Stability factors
  const stabilityFactor = work.stabilityIndex * 40
  const resilienceFactor = work.resilienceIndex * 35

  // Penalties
  const loadPenalty = work.loadIndex * 30
  const burnoutPenalty = work.burnoutIndex * 35
  const dependencyPenalty =
    work.ecologicalDependencyIndex * 20 +
    work.infrastructureDependencyIndex * 20 +
    work.economicDependencyIndex * 20

  const collapsePenalty = work.collapseRiskIndex * 35

  let stabilityScore =
    stabilityFactor +
    resilienceFactor -
    loadPenalty -
    burnoutPenalty -
    dependencyPenalty -
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
      resilienceFactor,
      loadPenalty,
      burnoutPenalty,
      dependencyPenalty,
      collapsePenalty,
      riskScore: risk.riskScore,
    },
  }
}