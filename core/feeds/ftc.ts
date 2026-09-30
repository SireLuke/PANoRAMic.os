// core/feeds/ftc.ts

/**
 * FTC Consumer Sentinel Feed
 * Real, public, no-auth endpoint.
 *
 * Example:
 * https://www.ftc.gov/data/api/consumer-sentinel/reports
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type FTCResponse = {
  results: Array<{
    category: string
    count: number
  }>
}

async function fetchFtcReports(): Promise<FTCResponse> {
  const url = "https://www.ftc.gov/data/api/consumer-sentinel/reports"

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`FTC request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollFtc(world: any, pillarDefaults: any) {
  const data = await fetchFtcReports()

  const fraud = data.results.find(r => r.category.includes("Fraud"))
  const identity = data.results.find(r => r.category.includes("Identity"))

  const packet = {
    sourceName: "FTC",
    sourceUrl: "https://www.ftc.gov",
    values: {
      fraudReports: fraud ? fraud.count : 0,
      identityTheftReports: identity ? identity.count : 0,
      regulatoryPressure: (fraud?.count || 0) * 0.001
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}