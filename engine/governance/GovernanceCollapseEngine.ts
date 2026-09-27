// engine/governance/GovernanceCollapseEngine.ts

import { GovernanceProfile } from "../../core/pillars/governance/GovernanceProfile"

export function applyGovernanceCollapse(gov: GovernanceProfile) {
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

  // Natural collapse pressure
  actions.push("Applying natural governance collapse pressure.")
  collapseRiskIndex *= 1.05

  // High conflict increases collapse
  if (conflictIndex > 0.6) {
    actions.push("High conflict — increasing collapse risk and reducing stability.")
    collapseRiskIndex *= 1.15
    stabilityIndex *= 0.9
  }

  // Low coordination penalty
  if (coordinationIndex < 0.4) {
    actions.push("Low coordination — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
  }

  // Low dignity penalty
  if (dignityIndex < 0.5) {
    actions.push("Low dignity compliance — increasing collapse risk.")
    collapseRiskIndex *= 1.1
    stabilityIndex *= 0.9
  }

  // Weak consensus penalty
  if (consensusIndex < 0.4) {
    actions.push("Weak consensus — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
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

  // Collapse event trigger
  const collapseEventTrigger =
    collapseRiskIndex * 0.4 +
    conflictIndex * 0.3 +
    (1 - stabilityIndex) * 0.2 +
    (1 - dignityIndex) * 0.1

  if (collapseEventTrigger > 0.8) {
    actions.push("Governance collapse event triggered — forcing critical mode.")
    stabilityIndex *= 0.7
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
    collapseEventTrigger,
  }
, consensus strengthening, dignity reinforcement.

Create: