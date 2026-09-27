// engine/workforce/WorkforceRiskEngine.ts

import { WorkforceProfile } from "../../core/pillars/workforce/WorkforceProfile"

export function computeWorkforceRisk(work: WorkforceProfile) {
  // Risk factors
  const loadRisk = work.loadIndex * 35
  const stabilityRisk = (1 - work.stabilityIndex) * 35
  const resilienceRisk = (1 - work.resilienceIndex) * 30
  const burnoutRisk = work.burnoutIndex * 40

  const dependencyRisk =
    work.ecologicalDependencyIndex * 25 +
    work.infrastructureDependencyIndex * 25 +
    work.economicDependencyIndex * 25

  const collapseRisk = work.collapseRiskIndex * 40

  let riskScore =
    loadRisk +
    stabilityRisk +
    resilienceRisk +
    burnoutRisk +
    dependencyRisk +
    collapseRisk

  // Normalize
  riskScore = Math.max(0, Math.min(riskScore, 100))

  let riskMode = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    riskScore,
    riskMode,
    breakdown: {
      loadRisk,
      stabilityRisk,
      resilienceRisk,
      burnoutRisk,
      dependencyRisk,
      collapseRisk,
    },
  }
}