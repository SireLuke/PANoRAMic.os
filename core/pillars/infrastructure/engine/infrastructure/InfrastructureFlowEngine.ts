// engine/infrastructure/InfrastructureFlowEngine.ts

import { InfrastructureProfile } from "../../core/pillars/infrastructure/InfrastructureProfile"

export function computeInfrastructureFlow(infra: InfrastructureProfile) {
  const actions: string[] = []

  let {
    resilienceIndex,
    loadIndex,
    redundancyIndex,
    degradationRate,
    repairRate,
    failurePressureIndex,
    humanDependencyIndex,
    ecologicalDependencyIndex,
  } = infra

  // Load effects
  if (loadIndex > 0.7) {
    actions.push("High load — increasing degradation and failure pressure.")
    degradationRate *= 1.15
    failurePressureIndex *= 1.2
  }

  // Resilience boost
  if (resilienceIndex > 0.7) {
    actions.push("High resilience — reducing degradation and failure pressure.")
    degradationRate *= 0.9
    failurePressureIndex *= 0.85
  }

  // Redundancy boost
  if (redundancyIndex > 0.6) {
    actions.push("High redundancy — boosting repair rate.")
    repairRate *= 1.15
  }

  // Human dependency penalty
  if (humanDependencyIndex > 0.6) {
    actions.push("High human dependency — increasing failure pressure.")
    failurePressureIndex *= 1.1
  }

  // Ecological dependency penalty
  if (ecologicalDependencyIndex > 0.6) {
    actions.push("High ecological dependency — increasing degradation.")
    degradationRate *= 1.1
  }

  // Collapse triggers
  const collapseRisk =
    failurePressureIndex * 0.4 +
    degradationRate * 0.3 +
    loadIndex * 0.3

  if (collapseRisk > 0.7) {
    actions.push("Infrastructure collapse risk — boosting repair and reducing degradation.")
    repairRate *= 1.2
    degradationRate *= 0.85
  }

  // Normalize
  resilienceIndex = Math.max(0, Math.min(resilienceIndex, 1))
  loadIndex = Math.max(0, Math.min(loadIndex, 1))
  redundancyIndex = Math.max(0, Math.min(redundancyIndex, 1))
  degradationRate = Math.max(0, Math.min(degradationRate, 1))
  repairRate = Math.max(0, Math.min(repairRate, 1))
  failurePressureIndex = Math.max(0, Math.min(failurePressureIndex, 1))
  humanDependencyIndex = Math.max(0, Math.min(humanDependencyIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))

  // Update infra
  infra.resilienceIndex = resilienceIndex
  infra.loadIndex = loadIndex
  infra.redundancyIndex = redundancyIndex
  infra.degradationRate = degradationRate
  infra.repairRate = repairRate
  infra.failurePressureIndex = failurePressureIndex
  infra.humanDependencyIndex = humanDependencyIndex
  infra.ecologicalDependencyIndex = ecologicalDependencyIndex

  return {
    actions,
    updatedInfrastructure: infra,
    resilienceIndex,
    loadIndex,
    redundancyIndex,
    degradationRate,
    repairRate,
    failurePressureIndex,
    humanDependencyIndex,
    ecologicalDependencyIndex,
    collapseRisk,
  }
}