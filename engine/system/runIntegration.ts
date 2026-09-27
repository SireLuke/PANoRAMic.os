// engine/system/runIntegration.ts

import { initSystemTickIntegration, runSystemTick } from "./systemTickIntegration"
import { dashboardEngine } from "../dashboard/dashboardEngine"
import { globalSignals } from "../../signals/globalSignals"

/**
 * runIntegration
 *
 * This module connects:
 * - systemTickIntegration
 * - run.ts
 * - CLI
 * - API
 * - dashboard
 *
 * It runs PAN continuously or step-by-step.
 */

export interface RunIntegration {
  tick: number
  systemTick: ReturnType<typeof initSystemTickIntegration>
  running: boolean
}

/**
 * Initialize run integration
 */
export function initRunIntegration(): RunIntegration {
  return {
    tick: 0,
    systemTick: initSystemTickIntegration(),
    running: false,
  }
}

/**
 * Run one tick of the entire planetary OS
 */
export function runOneTick(integration: RunIntegration) {
  integration.tick++

  // 1. Run system tick (nodes + pillars + modes + audits)
  runSystemTick(integration.systemTick)

  // 2. Update dashboard with global signals
  dashboardEngine.update({
    tick: integration.tick,
    signals: globalSignals,
    globalState: integration.systemTick.system.global,
  })

  return integration
}

/**
 * Run PAN continuously (loop)
 */
export async function runContinuous(integration: RunIntegration, intervalMs = 1000) {
  integration.running = true

  while (integration.running) {
    runOneTick(integration)
    await new Promise((resolve) => setTimeout(resolve, intervalMs))
  }

  return integration
}

/**
 * Stop continuous run
 */
export function stopRun(integration: RunIntegration) {
  integration.running = false
}
