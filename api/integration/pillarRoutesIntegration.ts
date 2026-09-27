// api/integration/pillarRoutesIntegration.ts

import { server } from "../server"
import { dashboardEngine } from "../../engine/dashboard/dashboardEngine"
import { globalSignals } from "../../signals/globalSignals"

/**
 * Bind pillar-specific API routes
 */
export function bindPillarRoutes() {
  const dashboard = () => dashboardEngine.getState()

  server.get("/par", (req, res) => {
    res.json(dashboard().par)
  })

  server.get("/rights", (req, res) => {
    res.json(dashboard().rights)
  })

  server.get("/ecology", (req, res) => {
    res.json(dashboard().ecology)
  })

  server.get("/infrastructure", (req, res) => {
    res.json(dashboard().infrastructure)
  })

  server.get("/commons", (req, res) => {
    res.json(dashboard().commons)
  })

  server.get("/governance", (req, res) => {
    res.json(dashboard().governance)
  })

  server.get("/labor", (req, res) => {
    res.json(dashboard().labor)
  })

  server.get("/markets", (req, res) => {
    res.json(dashboard().markets)
  })

  server.get("/population", (req, res) => {
    res.json(dashboard().population)
  })

  server.get("/workforce", (req, res) => {
    res.json(dashboard().workforce)
  })

  server.get("/modes", (req, res) => {
    res.json(globalSignals.modes)
  })
}
