// api/integration/pillarRoutesIntegration.ts

import { server } from "../server.js"
import { dashboardEngine } from "../../engine/dashboard/dashboardEngine.js"
import { globalSignals } from "../../signals/globalSignals.js"

export function bindPillarRoutes() {
  const dashboard = () => dashboardEngine.getState()

  // Core
  server.get("/tick", (req, res) => res.json({ tick: dashboard().tick }))
  server.get("/system", (req, res) => res.json(dashboard().systemState))
  server.get("/global", (req, res) => res.json(dashboard().globalState))
  server.get("/audits", (req, res) => res.json(dashboard().systemAudits))

  // NodeMap
  server.get("/nodeMap/signals", (req, res) => res.json(dashboard().nodeSignals))
  server.get("/nodeMap/audits", (req, res) => res.json(dashboard().nodeAudits))

  // Pillars
  server.get("/par", (req, res) => res.json(dashboard().par))
  server.get("/rights", (req, res) => res.json(dashboard().rights))
  server.get("/ecology", (req, res) => res.json(dashboard().ecology))
  server.get("/infrastructure", (req, res) => res.json(dashboard().infrastructure))
  server.get("/commons", (req, res) => res.json(dashboard().commons))
  server.get("/governance", (req, res) => res.json(dashboard().governance))
  server.get("/labor", (req, res) => res.json(dashboard().labor))
  server.get("/markets", (req, res) => res.json(dashboard().markets))
  server.get("/population", (req, res) => res.json(dashboard().population))
  server.get("/workforce", (req, res) => res.json(dashboard().workforce))

  // Modes
  server.get("/modes", (req, res) => res.json(globalSignals.modes))
}

}
