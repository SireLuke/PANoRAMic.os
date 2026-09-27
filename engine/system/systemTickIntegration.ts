// engine/system/systemTickIntegration.ts

import { initSystemLoopIntegration, runSystemLoopIntegration } from "./systemLoopIntegration"
import { globalSignals } from "../../signals/globalSignals"
import { dashboardEngine } from "../dashboard/dashboardEngine"

/**
 * SystemTickIntegration
 *
 * This module connects:
 * - systemLoopIntegration
 * - tick.ts
 * - run.ts
 *
 * It advances PAN one tick at a time.
 */

export interface SystemTickIntegration {
  system: ReturnType<typeof initSystemLoopIntegration>
}

/**
 * Initialize tick integration
 */
export function initSystemTickIntegration(): SystemTickIntegration {
  return {
    system: initSystemLoopIntegration(),
  }
}

/**
 * Run one tick of the entire planetary OS
 */
export function runSystemTick(integration: SystemTickIntegration) {
  // 1. Run system loop integration (nodes + pillars + modes + audits)
  runSystemLoopIntegration(integration.system)

  // 2. Push global signals into dashboard
  dashboardEngine.update({
    tick: integration.system.tick,
    signals: globalSignals,
    globalState: integration.system.global,
  })

  return integration
}
