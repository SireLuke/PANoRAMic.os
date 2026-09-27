// core/pillars/infrastructure/InfrastructureProfile.ts

export interface InfrastructureProfile {
  name: string
  infrastructureType:
    | "power"
    | "water"
    | "transport"
    | "digital"
    | "supply_chain"
    | "structural"
    | "communication"
    | "medical"
    | "agricultural"

  // Core metrics
  resilienceIndex: number          // 0–1
  loadIndex: number                // 0–1
  redundancyIndex: number          // 0–1
  degradationRate: number          // 0–1
  repairRate: number               // 0–1

  // Human + ecological dependency
  humanDependencyIndex: number     // 0–1
  ecologicalDependencyIndex: number // 0–1

  // Failure pressure
  failurePressureIndex: number     // 0–1
  collapseRiskIndex: number        // 0–1
}

export function evaluateInfrastructureHealth(infra: InfrastructureProfile) {
  // Base health
  let healthScore =
    infra.resilienceIndex * 40 +
    infra.redundancyIndex * 30 +
    infra.repairRate * 30

  // Penalties
  healthScore -= infra.loadIndex * 25
  healthScore -= infra.degradationRate * 25
  healthScore -= infra.failurePressureIndex * 30
  healthScore -= infra.humanDependencyIndex * 15
  healthScore -= infra.ecologicalDependencyIndex * 15

  // Normalize
  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}