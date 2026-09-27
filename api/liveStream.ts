// api/liveStream.ts

import { Server } from "socket.io"
import { initialSystemState } from "../core/SystemInitialState"
import { computeSystem } from "../engine/system/systemEngine"
import { buildPlanetDashboard } from "../engine/dashboard/planetDashboard"

export function attachLiveStream(httpServer: any) {
  const io = new Server(httpServer, {
    cors: {
      origin: "*",
    },
  })

  let state = initialSystemState

  // Broadcast every tick (you can adjust interval)
  setInterval(() => {
    state = computeSystem(state)
    const dashboard = buildPlanetDashboard(state)

    io.emit("planet_update", dashboard)
  }, 1000) // 1 second per tick

  io.on("connection", socket => {
    console.log("Client connected to PAN live stream")

    // Send immediate snapshot on connect
    const dashboard = buildPlanetDashboard(state)
    socket.emit("planet_update", dashboard)
  })

  return io
}
