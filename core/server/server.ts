// core/server/server.ts

import express from "express"
import { createWorld } from "../worldstate/createWorld"
import { tick } from "../tick/tickLoop"
import { createRouter } from "../simulation/router"

const app = express()
const port = 3000

// Build initial world
let world = createWorld()

// Create router bound to world
let router = createRouter(world)

// Optional: auto‑tick every second
setInterval(() => {
  world = tick(world)
  router = createRouter(world)
}, 1000)

// Routes
app.get("/world", (req, res) => {
  res.json(router.getWorld())
})

app.get("/nodes", (req, res) => {
  res.json(router.getNodes())
})

app.get("/signals", (req, res) => {
  res.json(router.getSignals())
})

app.get("/pillars", (req, res) => {
  res.json(router.getPillars())
})

app.listen(port, () => {
  console.log(`PAN‑OS server running at http://localhost:${port}`)
})
