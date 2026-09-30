// core/server/worldApi.ts

import http from "http"
import { getWorldSnapshot, getWorldDiff, getGlobalAlerts, getForecastHistory, getEventLog } from "../data/worldExports"

/**
 * World API:
 * Exposes PAN-OS state over simple HTTP endpoints.
 */

const PORT = 3000

export function startWorldApiServer() {
  const server = http.createServer((req, res) => {
    res.setHeader("Content-Type", "application/json")
    res.setHeader("Access-Control-Allow-Origin", "*")

    if (req.url === "/snapshot") {
      res.end(JSON.stringify(getWorldSnapshot() ?? {}))
      return
    }

    if (req.url === "/diff") {
      res.end(JSON.stringify(getWorldDiff() ?? {}))
      return
    }

    if (req.url === "/alerts") {
      res.end(JSON.stringify(getGlobalAlerts() ?? []))
      return
    }

    if (req.url === "/forecast") {
      res.end(JSON.stringify(getForecastHistory() ?? []))
      return
    }

    if (req.url === "/events") {
      res.end(JSON.stringify(getEventLog() ?? []))
      return
    }

    res.statusCode = 404
    res.end(JSON.stringify({ error: "Not found" }))
  })

  server.listen(PORT, () => {
    console.log(`PAN-OS World API listening on port ${PORT}`)
  })
}