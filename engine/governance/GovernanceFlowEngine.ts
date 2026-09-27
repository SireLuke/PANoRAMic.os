// engine/governance/GovernanceFlowEngine.ts

import { GovernanceProfile } from "../../core/pillars/governance/GovernanceProfile"

export function computeGovernanceFlow(gov: GovernanceProfile) {
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

  // Coordination boosts flow
  if (coordinationIndex > 0.7) {
    actions.push("High coordination — improving stability and reducing risk.")
    stabilityIndex *= 1.05
    riskIndex *= 0.9
  }

  // Consensus boosts dignity and stability
  if (consensusIndex > 0.6) {
    actions.push("Strong consensus — boosting dignity and stability.")
    dignityIndex *= 1.05
    stabilityIndex *= 1.05
  }

  // Conflict penalty
  if (conflictIndex > 0.5) {
    actions.push("High conflict — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
    stabilityIndex *= 0.9
  }

  // Responsiveness boosts recovery
  if (responsivenessIndex > 0.7) {
    actions.push("High responsiveness — reducing collapse pressure.")
    collapseRiskIndex *= 0.9
  }

  // Dependency pressure
  const dependencyPressure =
    ecologicalDependencyIndex * 0.25 +
    infrastructureDependencyIndex * 0.25 +
    workforceDependencyIndex * 0.25 +
    marketDependencyIndex * 0.25

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing governance collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Collapse trigger
  const collapseTrigger =
    collapseRiskIndex * 0.4 +
    conflictIndex * 0.3 +
    (1 - stabilityIndex) * 0.2 +
    (1 - dignityIndex) * 0.1

  if (collapseTrigger > 0.75) {
    actions.push("Governance collapse risk — forcing critical mode.")
    stabilityIndex *= 0.8
    coordinationIndex *= 0.85
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
    collapseTrigger,
  }
}