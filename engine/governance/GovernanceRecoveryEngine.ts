Paste:

```ts
// engine/governance/GovernanceRecoveryEngine.ts

import { GovernanceProfile } from "../../core/pillars/governance/GovernanceProfile"

export function applyGovernanceRecovery(gov: GovernanceProfile) {
  const actions: string[] = []

  let {
    stabilityIndex,
    riskIndex,
    coordinationIndex,
    dignityIndex,
    consensusIndex,
    conflictIndex,
    responsivenessIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    workforceDependencyIndex,
    marketDependencyIndex,
    collapseRiskIndex,
  } = gov

  // Base recovery
  actions.push("Applying base governance recovery.")
  stabilityIndex *= 1.05
  coordinationIndex *= 1.05

  // Consensus boosts recovery
  if (consensusIndex > 0.6) {
    actions.push("Strong consensus — reducing conflict and collapse pressure.")
    conflictIndex *= 0.9
    collapseRiskIndex *= 0.9
  }

  // Dignity boosts stability
  if (dignityIndex > 0.7) {
    actions.push("High dignity compliance — stabilizing governance behavior.")
    stabilityIndex *= 1.1
    riskIndex *= 0.9
  }

  // Responsiveness boosts recovery
  if (responsivenessIndex > 0.7) {
    actions.push("High responsiveness — reducing collapse pressure.")
    collapseRiskIndex *= 0.9
  }

  // Dependency pressure recovery
  const dependencyPressure =
    ecologicalDependencyIndex * 0.25 +
    infrastructureDependencyIndex * 0.25 +
    workforceDependencyIndex * 0.25 +
    marketDependencyIndex * 0.25

  if (dependencyPressure < 0.5) {
    actions.push("Low dependency pressure — boosting stability.")
    stabilityIndex *= 1.1
  }

  // Recovery trigger
  const recoveryTrigger =
    (1 - collapseRiskIndex) * 0.4 +
    stabilityIndex * 0.3 +
    dignityIndex * 0.3

  if (recoveryTrigger > 0.7) {
    actions.push("Recovery trigger — significantly reducing risk.")
    riskIndex *= 0.85
    collapseRiskIndex *= 0.85
  }

  // Normalize
  stabilityIndex = Math.max(0, Math.min(stabilityIndex, 1))
  riskIndex = Math.max(0, Math.min(riskIndex, 1))
  coordinationIndex = Math.max(0, Math.min(coordinationIndex, 1))
  dignityIndex = Math.max(0, Math.min(dignityIndex, 1))
  consensusIndex = Math.max(0, Math.min(consensusIndex, 1))
  conflictIndex = Math.max(0, Math.min(conflictIndex, 1))
  responsivenessIndex = Math.max(0, Math.min(responsivenessIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))
  infrastructureDependencyIndex = Math.max(0, Math.min(infrastructureDependencyIndex, 1))
  workforceDependencyIndex = Math.max(0, Math.min(workforceDependencyIndex, 1))
  marketDependencyIndex = Math.max(0, Math.min(marketDependencyIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  // Update gov
  gov.stabilityIndex = stabilityIndex
  gov.riskIndex = riskIndex
  gov.coordinationIndex = coordinationIndex
  gov.dignityIndex = dignityIndex
  gov.consensusIndex = consensusIndex
  gov.conflictIndex = conflictIndex
  gov.responsivenessIndex = responsivenessIndex
  gov.ecologicalDependencyIndex = ecologicalDependencyIndex
  gov.infrastructureDependencyIndex = infrastructureDependencyIndex
  gov.workforceDependencyIndex = workforceDependencyIndex
  gov.marketDependencyIndex = marketDependencyIndex
  gov.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedGovernance: gov,
    stabilityIndex,
    riskIndex,
    coordinationIndex,
    dignityIndex,
    consensusIndex,
    conflictIndex,
    responsivenessIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    workforceDependencyIndex,
    marketDependencyIndex,
    collapseRiskIndex,
    recoveryTrigger,
  }
}