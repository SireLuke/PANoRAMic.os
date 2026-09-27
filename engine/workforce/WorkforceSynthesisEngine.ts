// engine/workforce/WorkforceSynthesisEngine.ts

import { WorkforceProfile } from "../../core/pillars/workforce/WorkforceProfile"
import { computeWorkforceRisk } from "./WorkforceRiskEngine"
import { computeWorkforceStability } from "./WorkforceStabilityEngine"

export function computeWorkforceSynthesis(work: WorkforceProfile) {
  const risk = computeWorkforceRisk(work)
  const stability = computeWorkforceStability(work)

  // Additional synthesis indicators
  const stabilityFactor = work.stabilityIndex * 30
  const resilienceFactor = work.resilienceIndex * 30
  const burnoutPenalty = work.burnoutIndex * 35

  const loadPenalty = work.loadIndex * 25
  const dependencyPenalty =
    work.ecologicalDependencyIndex * 20 +
    work.infrastructureDependencyIndex * 20 +
    work.economicDependencyIndex * 20

  const collapsePenalty = work.collapseRiskIndex * 30

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    stabilityFactor +
    resilienceFactor -
    burnoutPenalty -
    loadPenalty -
    dependencyPenalty -
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
      resilienceFactor,
      burnoutPenalty,
      loadPenalty,
      dependencyPenalty,
      collapsePenalty,
    },
  }
}