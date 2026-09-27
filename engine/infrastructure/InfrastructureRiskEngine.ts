// engine/infrastructure/InfrastructureRiskEngine.ts

import { InfrastructureProfile } from "../../core/pillars/infrastructure/InfrastructureProfile"

export function computeInfrastructureRisk(infra: InfrastructureProfile) {
  // Risk factors
  const loadRisk = infra.loadIndex * 35
  const degradationRisk = infra.degradationRate * 35
  const failurePressureRisk = infra.failurePressureIndex * 40
  const lowResilienceRisk = (1 - infra.resilienceIndex) * 35
  const lowRedundancyRisk = (1 - infra.redundancyIndex) * 30
  const humanDependencyRisk = infra.humanDependencyIndex * 25
  const ecologicalDependencyRisk = infra.ecologicalDependencyIndex * 25

  // Collapse risk synthesis
  const collapseRisk =
    failurePressureRisk * 0.3 +
    degradationRisk * 0.25 +
    loadRisk * 0.2 +
    lowResilienceRisk * 0.15 +
    lowRedundancyRisk * 0.1

  let riskScore =
    loadRisk +
    degradationRisk +
    failurePressureRisk +
    lowResilienceRisk +
    lowRedundancyRisk +
    humanDependencyRisk +
    ecologicalDependencyRisk

  // Normalize
  riskScore = Math.max(0, Math.min(riskScore, 100))

  let riskMode = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    riskScore,
    riskMode,
    collapseRisk,
    breakdown: {
      loadRisk,
      degradationRisk,
      failurePressureRisk,
      lowResilienceRisk,
      lowRedundancyRisk,
      humanDependencyRisk,
      ecologicalDependencyRisk,
    },
  }
}