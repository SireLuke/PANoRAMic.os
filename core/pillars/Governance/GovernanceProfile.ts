// core/pillars/governance/GovernanceProfile.ts

export interface GovernanceProfile {
  name: string

  // Core governance metrics
  stabilityIndex: number            // 0–1
  riskIndex: number                 // 0–1
  coordinationIndex: number         // 0–1
  dignityIndex: number              // 0–1

  // Decision-making metrics
  consensusIndex: number            // 0–1
  conflictIndex: number             // 0–1
  responsivenessIndex: number       // 0–1

  // Systemic dependencies
  ecologicalDependencyIndex: number // 0–1
  infrastructureDependencyIndex: number // 0–1
  workforceDependencyIndex: number  // 0–1
  marketDependencyIndex: number     // 0–1

  // Collapse metrics
  collapseRiskIndex: number         // 0–1
}

export function evaluateGovernanceHealth(gov: GovernanceProfile) {
  let healthScore =
    gov.stabilityIndex * 35 +
    gov.coordinationIndex * 30 +
    gov.consensusIndex * 25 +
    gov.responsivenessIndex * 25 +
    gov.dignityIndex * 25

  healthScore -= gov.riskIndex * 25
  healthScore -= gov.conflictIndex * 25
  healthScore -= gov.collapseRiskIndex * 30

  healthScore -= gov.ecologicalDependencyIndex * 15
  healthScore -= gov.infrastructureDependencyIndex * 15
  healthScore -= gov.workforceDependencyIndex * 15
  healthScore -= gov.marketDependencyIndex * 15

  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}