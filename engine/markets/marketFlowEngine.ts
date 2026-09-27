// engine/markets/marketFlowEngine.ts

import { MarketProfile } from "../../core/pillars/markets/MarketProfile"

export function computeMarketFlow(market: MarketProfile) {
  const flowActions: string[] = []

  let { liquidity, velocity } = market

  // Flow collapse triggers
  const liquidityCollapse = liquidity < 0.4
  const velocityCollapse = velocity < 0.4

  // Flow overheating triggers
  const liquidityOverheat = liquidity > 1.5
  const velocityOverheat = velocity > 1.5

  // Extraction dampening
  if (market.extractivePressureIndex > 0.7) {
    flowActions.push("High extraction pressure — dampening flow.")
    liquidity *= 0.9
    velocity *= 0.9
  }

  // Dignity boost
  if (market.dignityComplianceIndex > 0.8) {
    flowActions.push("High dignity compliance — boosting flow.")
    liquidity *= 1.1
    velocity *= 1.1
  }

  // Corruption penalty
  if (market.corruptionIndex > 0.5) {
    flowActions.push("High corruption — reducing flow.")
    liquidity *= 0.85
    velocity *= 0.85
  }

  // Ecological penalty
  if (market.ecologicalImpactIndex > 0.6) {
    flowActions.push("High ecological impact — reducing flow.")
    liquidity *= 0.9
    velocity *= 0.9
  }

  // Infrastructure penalty
  if (market.infrastructureDependencyIndex > 0.7) {
    flowActions.push("High infrastructure dependency — reducing flow.")
    liquidity *= 0.9
    velocity *= 0.9
  }

  // Flow collapse recovery
  if (liquidityCollapse) {
    flowActions.push("Liquidity collapse — boosting liquidity.")
    liquidity *= 1.25
  }

  if (velocityCollapse) {
    flowActions.push("Velocity collapse — boosting velocity.")
    velocity *= 1.25
  }

  // Overheat dampening
  if (liquidityOverheat) {
    flowActions.push("Liquidity overheating — dampening liquidity.")
    liquidity *= 0.85
  }

  if (velocityOverheat) {
    flowActions.push("Velocity overheating — dampening velocity.")
    velocity *= 0.85
  }

  // Normalize
  liquidity = Math.max(0, Math.min(liquidity, 2))
  velocity = Math.max(0, Math.min(velocity, 2))

  // Update market
  market.liquidity = liquidity
  market.velocity = velocity

  return {
    flowActions,
    updatedMarket: market,
    liquidity,
    velocity,
  }
}