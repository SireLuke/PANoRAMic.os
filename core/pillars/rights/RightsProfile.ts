// core/pillars/rights/RightsProfile.ts

export interface RightsProfile {
  name: string

  // Core rights metrics
  dignityIndex: number              // 0–1
  autonomyIndex: number             // 0–1
  safetyIndex: number               // 0–1
  accessIndex: number               // 0–1
  fairnessIndex: number             // 0–1

  // Systemic pressures
  predatoryPressureIndex: number    // 0–1
  exclusionIndex: number            // 0–1
  exploitationIndex: number         // 0–1

  // Dependencies
  governanceDependencyIndex: number // 0–1
  marketDependencyIndex: number     // 0–1
  workforceDependencyIndex: number  // 0–1
  infrastructureDependencyIndex: number // 0–1
  ecologicalDependencyIndex: number // 0–1

  // Collapse metrics
  collapseRiskIndex: number         // 0–1
}

export function evaluateRightsHealth(rights: RightsProfile) {
  let healthScore =
    rights.dignityIndex * 35 +
    rights.autonomyIndex * 30 +
    rights.safetyIndex * 30 +
    rights.accessIndex * 25 +
    rights.fairnessIndex * 25

  healthScore -= rights.predatoryPressureIndex * 30
  healthScore -= rights.exclusionIndex * 25
  healthScore -= rights.exploitationIndex * 25
  healthScore -= rights.collapseRiskIndex * 30

  healthScore -= rights.governanceDependencyIndex * 15
  healthScore -= rights.marketDependencyIndex * 15
  healthScore -= rights.workforceDependencyIndex * 15
  healthScore -= rights.infrastructureDependencyIndex * 15
  healthScore -= rights.ecologicalDependencyIndex * 15

  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}