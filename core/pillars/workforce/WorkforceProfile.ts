// core/pillars/workforce/WorkforceProfile.ts

export interface WorkforceProfile {
  name: string
  workforceType:
    | "general"
    | "technical"
    | "medical"
    | "infrastructure"
    | "ecological"
    | "logistics"
    | "education"
    | "emergency"
    | "governance"

  // Core metrics
  stabilityIndex: number            // 0–1
  riskIndex: number                 // 0–1
  loadIndex: number                 // 0–1
  resilienceIndex: number           // 0–1
  burnoutIndex: number              // 0–1

  // Dependency metrics
  ecologicalDependencyIndex: number // 0–1
  infrastructureDependencyIndex: number // 0–1
  economicDependencyIndex: number   // 0–1

  // Collapse metrics
  collapseRiskIndex: number         // 0–1
}

export function evaluateWorkforceHealth(work: WorkforceProfile) {
  let healthScore =
    work.stabilityIndex * 40 +
    work.resilienceIndex * 30 -
    work.loadIndex * 25 -
    work.riskIndex * 25 -
    work.burnoutIndex * 25

  healthScore -= work.ecologicalDependencyIndex * 15
  healthScore -= work.infrastructureDependencyIndex * 15
  healthScore -= work.economicDependencyIndex * 15
  healthScore -= work.collapseRiskIndex * 30

  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}