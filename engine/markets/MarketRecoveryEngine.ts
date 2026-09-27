// engine/markets/MarketRecoveryEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"

export function applyMarketRecovery(market: MarketProfile) {
  const actions: string[] = []

  let {
    stabilityIndex,
    riskIndex,
    loadIndex,
    resilienceIndex,
    volatilityIndex,
    liquidityIndex,
    dignityComplianceIndex,
    predatoryPressureIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    workforceDependencyIndex,
    collapseRiskIndex,
  } = market

  // Base recovery
  actions.push("Applying base market recovery.")
  stabilityIndex *= 1.05
  resilienceIndex *= 1.05

  // Liquidity boosts recovery
  if (liquidityIndex > 0.6) {
    actions.push("High liquidity — reducing volatility and collapse pressure.")
    volatilityIndex *= 0.9
    collapseRiskIndex *= 0.9
  }

  // Dignity compliance boosts recovery
  if (dignityComplianceIndex > 0.7) {
    actions.push("High dignity compliance — stabilizing market behavior.")
    stabilityIndex *= 1.1
    predatoryPressureIndex *= 0.9
  }

  // Manageable load supports recovery
  if (loadIndex < 0.6) {
    actions.push("Moderate market load — supporting recovery.")
    stabilityIndex *= 1.1
  } else {
    actions.push("High market load — limiting recovery effectiveness.")
    stabilityIndex *= 0.95
  }

  // Volatility recovery
  if (volatilityIndex > 0.5) {
    actions.push("High volatility — applying volatility dampening.")
    volatilityIndex *= 0.9
  }

  // Dependency pressure recovery
  const dependencyPressure =
    ecologicalDependencyIndex * 0.3 +
    infrastructureDependencyIndex * 0.3 +
    workforceDependencyIndex * 0.3

  if (dependencyPressure < 0.5) {
    actions.push("Low dependency pressure — boosting stability.")
    stabilityIndex *= 1.1
  }

  // Recovery trigger
  const recoveryTrigger =
    (1 - collapseRiskIndex) * 0.4 +
    resilienceIndex * 0.3 +
    stabilityIndex * 0.3

  if (recoveryTrigger > 0.7) {
    actions.push("Recovery trigger — significantly reducing risk.")
    riskIndex *= 0.85
    collapseRiskIndex *= 0.85
  }

  // Normalize
  stabilityIndex = Math.max(0, Math.min(stabilityIndex, 1))
  riskIndex = Math.max(0, Math.min(riskIndex, 1))
  loadIndex = Math.max(0, Math.min(loadIndex, 1))
  resilienceIndex = Math.max(0, Math.min(resilienceIndex, 1))
  volatilityIndex = Math.max(0, Math.min(volatilityIndex, 1))
  liquidityIndex = Math.max(0, Math.min(liquidityIndex, 1))
  dignityComplianceIndex = Math.max(0, Math.min(dignityComplianceIndex, 1))
  predatoryPressureIndex = Math.max(0, Math.min(predatoryPressureIndex, 1))
  ecologicalDependencyIndex = Math.max(0, Math.min(ecologicalDependencyIndex, 1))
  infrastructureDependencyIndex = Math.max(0, Math.min(infrastructureDependencyIndex, 1))
  workforceDependencyIndex = Math.max(0, Math.min(workforceDependencyIndex, 1))
  collapseRiskIndex = Math.max(0, Math.min(collapseRiskIndex, 1))

  // Update market
  market.stabilityIndex = stabilityIndex
  market.riskIndex = riskIndex
  market.loadIndex = loadIndex
  market.resilienceIndex = resilienceIndex
  market.volatilityIndex = volatilityIndex
  market.liquidityIndex = liquidityIndex
  market.dignityComplianceIndex = dignityComplianceIndex
  market.predatoryPressureIndex = predatoryPressureIndex
  market.ecologicalDependencyIndex = ecologicalDependencyIndex
  market.infrastructureDependencyIndex = infrastructureDependencyIndex
  market.workforceDependencyIndex = workforceDependencyIndex
  market.collapseRiskIndex = collapseRiskIndex

  return {
    actions,
    updatedMarket: market,
    stabilityIndex,
    riskIndex,
    loadIndex,
    resilienceIndex,
    volatilityIndex,
    liquidityIndex,
    dignityComplianceIndex,
    predatoryPressureIndex,
    ecologicalDependencyIndex,
    infrastructureDependencyIndex,
    workforceDependencyIndex,
    collapseRiskIndex,
    recoveryTrigger,
  }
}