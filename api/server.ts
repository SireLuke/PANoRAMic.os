// api/server.ts

import express from "express"
import { initialSystemState } from "../core/SystemInitialState"
import { computeSystem } from "../engine/system/systemEngine"
import { buildPlanetDashboard } from "../engine/dashboard/planetDashboard"

const app = express()
const PORT = process.env.PORT || 3000

let state = initialSystemState

// advance PAN one tick each request (you can later move this to a timer/loop)
app.get("/planet", (req, res) => {
  state = computeSystem(state)
  const dashboard = buildPlanetDashboard(state)
  res.json(dashboard)
})

app.listen(PORT, () => {
  console.log(`PANoRAMic.os API running on http://localhost:${PORT}`)
})
