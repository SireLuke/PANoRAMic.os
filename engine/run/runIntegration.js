// engine/run/runIntegration.ts

import { initSystemTickIntegration, runSystemTick } from "../system/systemTickIntegration.js"
import { dashboardEngine } from "../dashboard/dashboardEngine.js"
import { globalSignals } from "../../signals/globalSignals.js"


export interface RunIntegration {
  tick: number
  systemTick: ReturnType<typeof initSystemTickIntegration>
  running: boolean
}

export function initRunIntegration(): RunIntegration {
  return {
    tick: 0,
    systemTick: initSystemTickIntegration(),
    running: false,
  }
}

export function runOneTick(integration: RunIntegration) {
  integration.tick++

  // Run system tick (nodes + pillars + modes + audits)
  runSystemTick(integration.systemTick)

  // Update dashboard with global signals + global state
  dashboardEngine.update({
    tick: integration.tick,
    signals: globalSignals,
    globalState: integration.systemTick.system.global,
  })

  return integration
}

export async function runContinuous(integration: RunIntegration, intervalMs = 1000) {
  integration.running = true

  while (integration.running) {
    runOneTick(integration)
    await new Promise((resolve) => setTimeout(resolve, intervalMs))
  }

  return integration
}

export function stopRun(integration: RunIntegration) {
  integration.running = false
}
