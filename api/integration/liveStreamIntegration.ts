// api/integration/liveStreamIntegration.ts

import { initAPIIntegration, apiTick } from "./apiIntegration"
import { liveStream } from "../liveStream"
import { dashboardEngine } from "../../engine/dashboard/dashboardEngine"
import { globalSignals } from "../../signals/globalSignals"

/**
 * LiveStreamIntegration
 *
 * Connects:
 * - apiIntegration
 * - WebSocket live stream
 * - dashboard
 * - global signals
 * - nodeMap
 * - pillar states
 */

export interface LiveStreamIntegration {
  api: ReturnType<typeof initAPIIntegration>
  intervalMs: number
}

/**
 * Initialize live stream integration
 */
export function initLiveStreamIntegration(intervalMs = 1000): LiveStreamIntegration {
  return {
    api: initAPIIntegration(),
    intervalMs,
  }
}

/**
 * Broadcast full planetary state
 */
function broadcast(integration: LiveStreamIntegration) {
  const state = {
    tick: integration.api.run.tick,
    global: integration.api.run.systemTick.system.global,
    signals: globalSignals,
    dashboard: dashboardEngine.getState(),
  }

  liveStream.broadcast(state)
}

/**
 * Run one tick and broadcast
 */
export function liveStreamTick(integration: LiveStreamIntegration) {
  apiTick(integration.api)
  broadcast(integration)
}

/**
 * Start continuous broadcast
 */
export async function startLiveStream(integration: LiveStreamIntegration) {
  console.log("LiveStream: Broadcasting planetary state...")

  while (true) {
    liveStreamTick(integration)
    await new Promise((resolve) => setTimeout(resolve, integration.intervalMs))
  }
}
