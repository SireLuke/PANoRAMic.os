// engine/system/systemEngine.ts
import { SystemState } from "../../core/SystemState"
import { computeWorkforceRotation } from "../workforce/workforceRotationEngine"
import { computeMicroAi } from "../microAI/microAiEngine"
import { computeMarkets } from "../markets/marketsEngine"
import { computeModes } from "../modes/modesEngine"

export function computeSystem(state: SystemState): SystemState {
  const workforceRotation = computeWorkforceRotation(state.workforceRotation)
  const microAi = computeMicroAi(state.microAi)
  const markets = computeMarkets(state.markets)
  const modes = computeModes(state.modes)

  // simple example interactions:
  const par = {
    ...state.par,
    parVelocity:
      workforceRotation.skillGainRate +
      markets.cooperativeMarketShare +
      microAi.microAiCoverageIndex,
  }

  const nodes = state.nodes.map(node => ({
    ...node,
    nodeHealthIndex:
      node.nodeHealthIndex +
      state.ecology.regenerationIndex +
      state.infrastructure.resilienceIndex,
  }))

  return {
    ...state,
    workforceRotation,
    microAi,
    markets,
    modes,
    par,
    nodes,
  }
}
