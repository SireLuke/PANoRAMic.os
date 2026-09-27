// engine/markets/MarketCollapseEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"

export function applyMarketCollapse(market: MarketProfile) {
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

  // Natural collapse pressure
  actions.push("Applying natural market collapse pressure.")
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

  // Predatory pressure penalty
  if (predatoryPressureIndex > 0.6) {
    actions.push("High predatory pressure — reducing dignity compliance and stability.")
    dignityComplianceIndex *= 0.85
    stabilityIndex *= 0.9
  }

  // Low dignity compliance penalty
  if (dignityComplianceIndex < 0.4) {
    actions.push("Low dignity compliance — increasing collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Dependency pressure
  const dependencyPressure =
    ecologicalDependencyIndex * 0.3 +
    infrastructureDependencyIndex * 0.3 +
    workforceDependencyIndex * 0.3

  if (dependencyPressure > 0.6) {
    actions.push("High dependency pressure — increasing collapse risk.")
    collapseRiskIndex *= 1.1
  }

  // Collapse event trigger
  const collapseEventTrigger =
    collapseRiskIndex * 0.4 +
    volatilityIndex * 0.3 +
    (1 - stabilityIndex) * 0.2 +
    predatoryPressureIndex * 0.1

  if (collapseEventTrigger > 0.8) {
    actions.push("Market collapse event triggered — forcing critical mode.")
    stabilityIndex *= 0.7
    resilienceIndex *= 0.8
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
    collapseEventTrigger,
  }
}