// api/index.ts

import express from "express"
import { initialSystemState } from "../core/SystemInitialState"
import { attachPlanetRouter } from "./routes/planetRouter"

const app = express()
const PORT = process.env.PORT || 3000

// Attach all planetary API routes
app.use("/api", attachPlanetRouter(initialSystemState))

// Root endpoint
app.get("/", (req, res) => {
  res.json({
    status: "PANoRAMic.os API is running",
    endpoints: [
      "/api/planet",
      "/api/par",
      "/api/nodes",
      "/api/ecology",
      "/api/infrastructure",
      "/api/markets",
      "/api/modes",
      "/api/health",
      "/api/risk",
      "/api/synthesis",
    ],
  })
})

app.listen(PORT, () => {
  console.log(`PANoRAMic.os API live at http://localhost:${PORT}`)
})
