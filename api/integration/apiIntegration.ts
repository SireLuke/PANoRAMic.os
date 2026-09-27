// api/integration/apiIntegration.ts

import { initRunIntegration, runOneTick } from "../../engine/system/runIntegration.js"
import { dashboardEngine } from "../../engine/dashboard/dashboardEngine.js"
import { globalSignals } from "../../signals/globalSignals.js"
import { server } from "../server.js"
import { liveStream } from "../liveStream.js"
import { planetRouter } from "../routes/planetRouter.js"


export interface APIIntegration {
  run: ReturnType<typeof initRunIntegration>
}

/**
 * Initialize API integration layer
 */
export function initAPIIntegration(): APIIntegration {
  return {
    run: initRunIntegration(),
  }
}

/**
 * Broadcast full planetary state over WebSocket
 */
function broadcastState(integration: APIIntegration) {
  const state = {
    tick: integration.run.tick,
    global: integration.run.systemTick.system.global,
    signals: globalSignals,
    dashboard: dashboardEngine.getState(),
  }

  liveStream.broadcast(state)
}

/**
 * Run one tick and broadcast via API
 */
export function apiTick(integration: APIIntegration) {
  runOneTick(integration.run)
  broadcastState(integration)
}

/**
 * Start continuous planetary broadcast
 */
export async function apiRun(integration: APIIntegration, intervalMs = 1000) {
  console.log("API: Starting continuous planetary broadcast...")

  while (true) {
    apiTick(integration)
    await new Promise((resolve) => setTimeout(resolve, intervalMs))
  }
}

/**
 * Bind API routes to planetary state
 */
export function bindAPIRoutes(integration: APIIntegration) {
  server.get("/state", (req, res) => {
    res.json({
      tick: integration.run.tick,
      global: integration.run.systemTick.system.global,
      signals: globalSignals,
      dashboard: dashboardEngine.getState(),
    })
  })

  server.get("/nodes", (req, res) => {
    res.json(integration.run.systemTick.system.global.nodeMap)
  })

  server.get("/signals", (req, res) => {
    res.json(globalSignals)
  })

  server.get("/dashboard", (req, res) => {
    res.json(dashboardEngine.getState())
  })
}
