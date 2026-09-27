// api/serverWithLive.ts

import express from "express"
import http from "http"

import { initialSystemState } from "../core/SystemInitialState"
import { attachPlanetRouter } from "./routes/planetRouter"
import { attachLiveStream } from "./liveStream"

export function startPanServer() {
  const app = express()
  const server = http.createServer(app)

  // Attach REST API
  app.use("/api", attachPlanetRouter(initialSystemState))

  // Attach WebSocket live stream
  attachLiveStream(server)

  const PORT = process.env.PORT || 3000

  server.listen(PORT, () => {
    console.log(`PANoRAMic.os LIVE server running at http://localhost:${PORT}`)
    console.log(`REST API: http://localhost:${PORT}/api/planet`)
    console.log(`WebSocket: ws://localhost:${PORT}`)
  })
}
