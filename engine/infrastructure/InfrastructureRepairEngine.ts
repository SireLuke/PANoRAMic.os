// engine/infrastructure/InfrastructureRepairEngine.ts

import { InfrastructureProfile } from "../../core/pillars/infrastructure/InfrastructureProfile"

export function applyInfrastructureRepair(infra: InfrastructureProfile) {
  const actions: string[] = []

  let {
    repairRate,
    degradationRate,
    resilienceIndex,
    redundancyIndex,
    failurePressureIndex,
    loadIndex,
  } = infra

  // Base repair
  actions.push("Applying base infrastructure repair.")
  repairRate *= 1.05

  // High redundancy boosts repair
  if (redundancyIndex > 0.6) {
    actions.push("High redundancy — boosting repair efficiency.")
    repairRate *= 1.15
  }

  // High resilience boosts repair
  if (resilienceIndex > 0.7) {
    actions.push("High resilience — reducing degradation and failure pressure.")
    degradationRate *= 0.9
    failurePressureIndex *= 0.9
  }

  // Load penalty
  if (loadIndex > 0.7) {
    actions.push("High load — reducing repair effectiveness.")
    repairRate *= 0.9
  }

  // Failure pressure penalty
  if (failurePressureIndex > 0.6) {
    actions.push("High failure pressure — increasing degradation.")
    degradationRate *= 1.1
  }

  // Emergency repair trigger
  const emergencyTrigger =
    failurePressureIndex * 0.4 +
    degradationRate * 0.3 +
    (1 - resilienceIndex) * 0.2 +
    (1 - redundancyIndex) * 0.1

  if (emergencyTrigger > 0.75) {
    actions.push("Emergency repair triggered — boosting repair and dampening degradation.")
    repairRate *= 1.25
    degradationRate *= 0.85
  }

  // Normalize
  repairRate = Math.max(0, Math.min(repairRate, 1))
  degradationRate = Math.max(0, Math.min(degradationRate, 1))
  resilienceIndex = Math.max(0, Math.min(resilienceIndex, 1))
  redundancyIndex = Math.max(0, Math.min(redundancyIndex, 1))
  failurePressureIndex = Math.max(0, Math.min(failurePressureIndex, 1))
  loadIndex = Math.max(0, Math.min(loadIndex, 1))

  // Update infra
  infra.repairRate = repairRate
  infra.degradationRate = degradationRate
  infra.resilienceIndex = resilienceIndex
  infra.redundancyIndex = redundancyIndex
  infra.failurePressureIndex = failurePressureIndex
  infra.loadIndex = loadIndex

  return {
    actions,
    updatedInfrastructure: infra,
    repairRate,
    degradationRate,
    resilienceIndex,
    redundancyIndex,
    failurePressureIndex,
    loadIndex,
    emergencyTrigger,
  }
}