// engine/markets/MarketFlowEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"

export function computeMarketFlow(market: MarketProfile) {
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

  // Volatility effects
  if (volatilityIndex > 0.6) {
    actions.push("High volatility — increasing risk and collapse pressure.")
    riskIndex *= 1.15
    collapseRiskIndex *= 1.1
  }

  // Liquidity boost
  if (liquidityIndex > 0.7) {
    actions.push("High liquidity — reducing risk and stabilizing flows.")
    riskIndex *= 0.9
    stabilityIndex *= 1.05
  }

  // Predatory pressure penalty
  if (predatoryPressureIndex > 0.5) {
    actions.push("Predatory pressure detected — reducing dignity compliance and stability.")
    dignityComplianceIndex *= 0.9
    stabilityIndex *= 0.9
  }

  // Dignity compliance boost
  if (dignityComplianceIndex > 0.7) {
    actions.push("High dignity compliance — reducing collapse pressure.")
    collapseRiskIndex *= 0.9
  }

  // Dependency penalties
  const dependencyPressure =
    ecologicalDependencyIndex * 0.3 +
    infrastructureDependencyIndex * 0.3 +
    workforceDependencyIndex * 0.3

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Load effects
  if (loadIndex > 0.7) {
    actions.push("High market load — increasing volatility and collapse pressure.")
    volatilityIndex *= 1.1
    collapseRiskIndex *= 1.15
  }

  // Collapse trigger
  const collapseTrigger =
    riskIndex * 0.3 +
    volatilityIndex * 0.3 +
    (1 - stabilityIndex) * 0.2 +
    predatoryPressureIndex * 0.2

  if (collapseTrigger > 0.75) {
    actions.push("Market collapse risk — boosting stability and reducing volatility.")
    stabilityIndex *= 1.1
    volatilityIndex *= 0.85
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
    collapseTrigger,
  }
}