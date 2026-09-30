// core/server/worldApi.ts

import http from "http"
import {
  getWorldSnapshot,
  getWorldDiff,
  getGlobalAlerts,
  getForecastHistory,
  getEventLog
} from "../data/worldExports"

/**
 * World API:
 * Exposes PAN-OS state over simple HTTP endpoints.
 */

const PORT = 3000

export function startWorldApiServer() {
  const server = http.createServer((req, res) => {
    res.setHeader("Content-Type", "application/json")
    res.setHeader("Access-Control-Allow-Origin", "*")

    switch (req.url) {
      case "/snapshot":
        res.end(JSON.stringify(getWorldSnapshot() ?? {}))
        return

      case "/diff":
        res.end(JSON.stringify(getWorldDiff() ?? {}))
        return

      case "/alerts":
        res.end(JSON.stringify(getGlobalAlerts() ?? []))
        return

      case "/forecast":
        res.end(JSON.stringify(getForecastHistory() ?? []))
        return

      case "/events":
        res.end(JSON.stringify(getEventLog() ?? []))
        return

      default:
        res.statusCode = 404
        res.end(JSON.stringify({ error: "Not found" }))
        return
    }
  })

  server.listen(PORT, () => {
    console.log(`PAN-OS World API listening on port ${PORT}`)
  })
}