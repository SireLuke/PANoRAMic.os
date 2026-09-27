// engine/system/systemEngine.ts
// engine/system/systemEngine.ts

import { SystemState } from "../../core/SystemState.js"

import { computeWorkforceRotation } from "../workforce/workforceRotationEngine.js"
import { computeMicroAi } from "../microAI/microAiEngine.js"
import { computeMarkets } from "../markets/marketsEngine.js"

import { computeModes } from "../modes/modesEngine.js"
import { computeModeTriggers } from "../modes/modeTriggersEngine.js"

import { computePar } from "../par/parEngine.js"

import { evolveNodes } from "../nodes/nodeEvolutionEngine.js"
import { computeDashboard } from "../dashboard/dashboardEngine.js"

import { auditSystem } from "../../rams/system/systemAudit.js"

export function computeSystem(state: SystemState): SystemState {

  // 1. Subsystem updates
  const workforceRotation = computeWorkforceRotation(state.workforceRotation)
  const microAi = computeMicroAi(state.microAi)
  const markets = computeMarkets(state.markets)

  // 2. Mode triggers (immune system reflexes)
  const modesTriggered = computeModeTriggers({
    modes: state.modes,
    ecology: state.ecology,
    infrastructure: state.infrastructure,
    markets,
    par: state.par,
  })

  const modes = computeModes(modesTriggered)

  // 3. Node evolution (planetary nervous system)
  const nodes = evolveNodes({
    nodes: state.nodes,
    ecology: state.ecology,
    infrastructure: state.infrastructure,
    microAi,
  })

  // 4. PAR economy (cap → salary → enforcement)
  const par = computePar({
    par: state.par,
    workforceRotation,
    modes,
    nodes,
    markets,
    ecology: state.ecology,
    infrastructure: state.infrastructure,
  })

  // 5. Build new state
  const newState: SystemState = {
    ...state,
    workforceRotation,
    microAi,
    markets,
    modes,
    nodes,
    par,
  }

  // 6. Global dashboard (planetary immune system)
  const dashboard = computeDashboard(newState)

  // 7. Global audit (RAMS)
  const audit = auditSystem(newState)

  return {
    ...newState,
    dashboard,
    audit,
  }
}

