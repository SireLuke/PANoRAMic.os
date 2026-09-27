// engine/par/PARRecoveryEngine.ts

import { PARProfile } from "../../core/pillars/par/PARProfile"

export function applyPARRecovery(par: PARProfile) {
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

  // Base recovery
  actions.push("Applying base PAR recovery.")
  stabilityIndex *= 1.05
  parValueIndex *= 1.05

  // Liquidity boosts recovery
  if (liquidityIndex > 0.6) {
    actions.push("High liquidity — reducing volatility and collapse pressure.")
    volatilityIndex *= 0.9
    collapseRiskIndex *= 0.9
  }

  // Dignity boosts stability
  if (dignityIndex > 0.7) {
    actions.push("High dignity compliance — stabilizing PAR behavior.")
    stabilityIndex *= 1.1
    riskIndex *= 0.9
  }

  // Strong backing boosts recovery
  const backingStrength =
    ecologicalBackingIndex * 0.25 +
    infrastructureBackingIndex * 0.25 +
    workforceBackingIndex * 0.25 +
    marketBackingIndex * 0.25

  if (backingStrength > 0.6) {
    actions.push("Strong renewable backing — boosting PAR stability.")
    stabilityIndex *= 1.1
    parValueIndex *= 1.05
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
    recoveryTrigger,
  }
}