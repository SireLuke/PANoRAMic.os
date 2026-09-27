// engine/par/PARCollapseEngine.ts

import { PARProfile } from "../../core/pillars/par/PARProfile"

export function applyPARCollapse(par: PARProfile) {
  const actions: string[] = []

  let {
    parValueIndex,
    stabilityIndex,
    riskIndex,
    liquidityIndex,
    dignityIndex,
    ecologicalBackingIndex,
    infrastructureBackingIndex,
    workforceBackingIndex,
    marketBackingIndex,
    volatilityIndex,
    collapseRiskIndex,
  } = par

  // Natural collapse pressure
  actions.push("Applying natural PAR collapse pressure.")
  collapseRiskIndex *= 1.05

  // High volatility increases collapse
  if (volatilityIndex > 0.7) {
    actions.push("High volatility — increasing collapse risk and reducing stability.")
    collapseRiskIndex *= 1.15
    stabilityIndex *= 0.9
  }

  // Low liquidity penalty
  if (liquidityIndex < 0.4) {
    actions.push("Low liquidity — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
  }

  // Low dignity penalty
  if (dignityIndex < 0.5) {
    actions.push("Low dignity compliance — increasing collapse risk.")
    collapseRiskIndex *= 1.1
    stabilityIndex *= 0.9
  }

  // Weak backing penalty
  const backingStrength =
    ecologicalBackingIndex * 0.25 +
    infrastructureBackingIndex * 0.25 +
    workforceBackingIndex * 0.25 +
    marketBackingIndex * 0.25

  if (backingStrength < 0.5) {
    actions.push("Weak renewable backing — increasing collapse pressure.")
    collapseRiskIndex *= 1.15
  }

  // Collapse event trigger
  const collapseEventTrigger =
    collapseRiskIndex * 0.4 +
    volatilityIndex * 0.3 +
    (1 - stabilityIndex) * 0.2 +
    (1 - dignityIndex) * 0.1

  if (collapseEventTrigger > 0.8) {
    actions.push("PAR collapse event triggered — forcing critical mode.")
    stabilityIndex *= 0.7
    parValueIndex *= 0.85
  }

  // Normalize
  parValueIndex = Math.max(0, Math.min(parValueIndex, 1))
  stabilityIndex = Math.max(0, Math.min(stabilityIndex, 1))
  riskIndex = Math.max(0, Math.min(riskIndex, 1))
  liquidityIndex = Math.max(0, Math.min(liquidityIndex, 1))
  dignityIndex = Math.max(0, Math.min(dignityIndex, 1))
  ecologicalBackingIndex = Math.max(0, Math.min(ecologicalBackingIndex, 1))
  infrastructureBackingIndex = Math.max(0, Math.min(infrastructureBackingIndex, 1))
  workforceBackingIndex = Math.max(0, Math.min(workforceBackingIndex, 1))
  marketBackingIndex = Math.max(0, Math.min(marketBackingIndex, 1))
  volatilityIndex = Math.max(0, Math.min(volatilityIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  // Update par
  par.parValueIndex = parValueIndex
  par.stabilityIndex = stabilityIndex
  par.riskIndex = riskIndex
  par.liquidityIndex = liquidityIndex
  par.dignityIndex = dignityIndex
  par.ecologicalBackingIndex = ecologicalBackingIndex
  par.infrastructureBackingIndex = infrastructureBackingIndex
  par.workforceBackingIndex = workforceBackingIndex
  par.marketBackingIndex = marketBackingIndex
  par.volatilityIndex = volatilityIndex
  par.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedPAR: par,
    parValueIndex,
    stabilityIndex,
    riskIndex,
    liquidityIndex,
    dignityIndex,
    ecologicalBackingIndex,
    infrastructureBackingIndex,
    workforceBackingIndex,
    marketBackingIndex,
    volatilityIndex,
    collapseRiskIndex,
    collapseEventTrigger,
  }
}