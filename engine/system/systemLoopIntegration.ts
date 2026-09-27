// engine/system/systemLoopIntegration.ts

import { initGlobalLoopIntegration, runGlobalLoopIntegration } from "../global/globalLoopIntegration"
import { systemEngine } from "./systemEngine"
import { systemAudit } from "../../rams/system/systemAudit"
import { dashboardEngine } from "../dashboard/dashboardEngine"
import { globalSignals } from "../../signals/globalSignals"

export interface SystemLoopIntegration {
  tick: number
  global: ReturnType<typeof initGlobalLoopIntegration>
}

/**
 * Initialize the system loop integration layer
 */
export function initSystemLoopIntegration(): SystemLoopIntegration {
  return {
    tick: 0,
    global: initGlobalLoopIntegration(),
  }
}

/**
 * Run one full system integration tick
 */
export function runSystemLoopIntegration(state: SystemLoopIntegration) {
  state.tick++

  // 1. Run global loop integration (nodes + pillars + modes + audits)
  runGlobalLoopIntegration(state.global)

  // 2. Run system engine (planet-level synthesis)
  const systemState = systemEngine(globalSignals)

  // 3. Run system-level RAMS audits
  const audits = systemAudit(globalSignals)

  // 4. Update dashboard with system-level data
  dashboardEngine.update({
    tick: state.tick,
    systemState,
    audits,
    globalState: state.global,
  })

  return state
}
