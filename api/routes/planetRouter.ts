// api/routes/planetRouter.ts

import { Router } from "express"
import { SystemState } from "../../core/SystemState"
import { computeSystem } from "../../engine/system/systemEngine"
import { buildPlanetDashboard } from "../../engine/dashboard/planetDashboard"

const router = Router()

let state: SystemState | null = null

export function attachPlanetRouter(initialState: SystemState) {
  state = initialState

  // Global dashboard endpoint
  router.get("/planet", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })

    state = computeSystem(state)
    const dashboard = buildPlanetDashboard(state)
    res.json(dashboard)
  })

  // PAR endpoint
  router.get("/par", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    res.json(state.par)
  })

  // Nodes endpoint
  router.get("/nodes", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    res.json(state.nodes)
  })

  // Ecology endpoint
  router.get("/ecology", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    res.json(state.ecology)
  })

  // Infrastructure endpoint
  router.get("/infrastructure", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    res.json(state.infrastructure)
  })

  // Markets endpoint
  router.get("/markets", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    res.json(state.markets)
  })

  // Modes endpoint
  router.get("/modes", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    res.json(state.modes)
  })

  // Global health endpoint
  router.get("/health", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    const dashboard = buildPlanetDashboard(state)
    res.json({ globalHealth: dashboard.globalHealth })
  })

  // Global risk endpoint
  router.get("/risk", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    const dashboard = buildPlanetDashboard(state)
    res.json({ globalRisk: dashboard.globalRisk })
  })

  // Global synthesis endpoint
  router.get("/synthesis", (req, res) => {
    if (!state) return res.status(500).json({ error: "System not initialized" })
    state = computeSystem(state)
    const dashboard = buildPlanetDashboard(state)
    res.json({ globalSynthesis: dashboard.globalSynthesis })
  })

  return router
}
