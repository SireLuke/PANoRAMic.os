// engine/par/PARFlowEngine.ts

import { PARProfile } from "../../core/pillars/par/PARProfile"

export function computePARFlow(par: PARProfile) {
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

  // Liquidity boosts flow
  if (liquidityIndex > 0.7) {
    actions.push("High liquidity — strengthening PAR value and stability.")
    parValueIndex *= 1.05
    stabilityIndex *= 1.05
  }

  // Volatility penalty
  if (volatilityIndex > 0.6) {
    actions.push("High volatility — increasing risk and collapse pressure.")
    riskIndex *= 1.15
    collapseRiskIndex *= 1.1
  }

  // Dignity compliance boosts stability
  if (dignityIndex > 0.7) {
    actions.push("High dignity compliance — reducing collapse pressure.")
    collapseRiskIndex *= 0.9
  }

  // Backing pressure
  const backingStrength =
    ecologicalBackingIndex * 0.25 +
    infrastructureBackingIndex * 0.25 +
    workforceBackingIndex * 0.25 +
    marketBackingIndex * 0.25

  if (backingStrength > 0.6) {
    actions.push("Strong renewable backing — boosting PAR stability.")
    stabilityIndex *= 1.1
    parValueIndex *= 1.05
  } else {
    actions.push("Weak backing — increasing collapse pressure.")
    collapseRiskIndex *= 1.1
  }

  // Collapse trigger
  const collapseTrigger =
    riskIndex * 0.3 +
    volatilityIndex * 0.3 +
    (1 - stabilityIndex) * 0.2 +
    (1 - dignityIndex) * 0.2

  if (collapseTrigger > 0.75) {
    actions.push("PAR collapse risk — boosting stability and reducing volatility.")
    stabilityIndex *= 1.1
    volatilityIndex *= 0.85
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
    collapseTrigger,
  }
}