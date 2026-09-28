// api/server.ts
import { initWorld } from "../engine/world/initWorld.ts"
import { tick } from "../engine/world/tick.ts"
import { buildDashboard } from "../engine/world/dashboard.ts"
import { createServer } from "http"
import { Server } from "socket.io"

const world = initWorld([])

const httpServer = createServer()
const io = new Server(httpServer, {
  cors: { origin: "*" }
})

io.on("connection", socket => {
  console.log("client connected")
})

setInterval(() => {
  const result = tick(world)
  const packet = buildDashboard({
    world: result.world,
    signals: result.signals,
    tick: result.tick
  })

  io.emit("planet_update", packet)
}, 1000)

httpServer.listen(3000, () => {
  console.log("PANoRAMic.os live stream running on ws://localhost:3000")
})
