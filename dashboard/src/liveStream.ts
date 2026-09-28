// dashboard/src/liveStream.ts

import { io, Socket } from "socket.io-client"
import { DashboardPacket } from "../../engine/world/dashboard.ts"

export interface LiveStream {
  socket: Socket
  connect: () => void
  disconnect: () => void
  onPlanetUpdate: (cb: (packet: DashboardPacket) => void) => void
}

export function createLiveStream(url: string): LiveStream {
  const socket = io(url, {
    transports: ["websocket"],
    reconnection: true,
    reconnectionDelay: 500,
    reconnectionAttempts: Infinity,
  })

  return {
    socket,

    connect() {
      socket.connect()
    },

    disconnect() {
      socket.disconnect()
    },

    onPlanetUpdate(cb) {
      socket.on("planet_update", (dashboard: DashboardPacket) => {
        cb(dashboard)
      })
    },
  }
}
