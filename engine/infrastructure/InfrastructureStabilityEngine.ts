// engine/infrastructure/InfrastructureStabilityEngine.ts

import { InfrastructureProfile } from "../../core/pillars/infrastructure/InfrastructureProfile"
import { computeInfrastructureRisk } from "./InfrastructureRiskEngine"

export function computeInfrastructureStability(infra: InfrastructureProfile) {
  const risk = computeInfrastructureRisk(infra)

  // Stability factors
  const resilienceFactor = infra.resilienceIndex * 40
  const redundancyFactor = infra.redundancyIndex * 35
  const repairFactor = infra.repairRate * 30

  // Penalties
  const loadPenalty = infra.loadIndex * 30
  const degradationPenalty = infra.degradationRate * 30
  const failurePressurePenalty = infra.failurePressureIndex * 35
  const humanDependencyPenalty = infra.humanDependencyIndex * 20
  const ecologicalDependencyPenalty = infra.ecologicalDependencyIndex * 20

  let stabilityScore =
    resilienceFactor +
    redundancyFactor +
    repairFactor -
    loadPenalty -
    degradationPenalty -
    failurePressurePenalty -
    humanDependencyPenalty -
    ecologicalDependencyPenalty -
    risk.collapseRisk * 20

  // Normalize
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      resilienceFactor,
      redundancyFactor,
      repairFactor,
      loadPenalty,
      degradationPenalty,
      failurePressurePenalty,
      humanDependencyPenalty,
      ecologicalDependencyPenalty,
      collapseRisk: risk.collapseRisk,
    },
  }
}