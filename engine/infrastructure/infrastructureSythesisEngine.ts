// engine/infrastructure/InfrastructureSynthesisEngine.ts

import { InfrastructureProfile } from "../../core/pillars/infrastructure/InfrastructureProfile"
import { computeInfrastructureRisk } from "./InfrastructureRiskEngine"
import { computeInfrastructureStability } from "./InfrastructureStabilityEngine"

export function computeInfrastructureSynthesis(infra: InfrastructureProfile) {
  const risk = computeInfrastructureRisk(infra)
  const stability = computeInfrastructureStability(infra)

  // Additional synthesis indicators
  const resilienceFactor = infra.resilienceIndex * 30
  const redundancyFactor = infra.redundancyIndex * 30
  const repairFactor = infra.repairRate * 30

  const loadPenalty = infra.loadIndex * 25
  const degradationPenalty = infra.degradationRate * 25
  const failurePressurePenalty = infra.failurePressureIndex * 30
  const humanDependencyPenalty = infra.humanDependencyIndex * 20
  const ecologicalDependencyPenalty = infra.ecologicalDependencyIndex * 20

  // Synthesis score combines:
  // - stability
  // - inverse risk
  // - resilience
  // - redundancy
  // - repair
  // - penalties for load, degradation, failure pressure, dependencies

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    resilienceFactor +
    redundancyFactor +
    repairFactor -
    loadPenalty -
    degradationPenalty -
    failurePressurePenalty -
    humanDependencyPenalty -
    ecologicalDependencyPenalty

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
      resilienceFactor,
      redundancyFactor,
      repairFactor,
      loadPenalty,
      degradationPenalty,
      failurePressurePenalty,
      humanDependencyPenalty,
      ecologicalDependencyPenalty,
    },
  }
}