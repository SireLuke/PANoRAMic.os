// api/integration/apiBootstrap.ts

import { server } from "../server.js"
import { bindAPIRoutes } from "./apiIntegration.js"
import { bindPillarRoutes } from "./pillarRoutesIntegration.js"
import { liveStream } from "../liveStream.js"
import { planetRouter } from "../routes/planetRouter.js"
import { initAPIIntegration } from "./apiIntegration.js"
import { initLiveStreamIntegration, startLiveStream } from "./liveStreamIntegration.js"

/**
 * API Bootstrap
 *
 * This file ties together:
 * - REST API
 * - WebSocket live stream
 * - pillar routes
 * - planetary engine integration
 */

export async function bootstrapAPI() {
  console.log("API: Initializing planetary API...")

  // 1. Initialize API integration
  const api = initAPIIntegration()

  // 2. Bind REST routes
  bindAPIRoutes(api)
  bindPillarRoutes()

  // 3. Start REST server
  server.listen(3000, () => {
    console.log("API: REST server running on port 3000")
  })

  // 4. Start WebSocket live stream
  const live = initLiveStreamIntegration(1000)
  startLiveStream(live)
}
