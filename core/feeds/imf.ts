// core/feeds/imf.ts

/**
 * IMF Economic Stress Feed
 * Real, public, no-auth endpoint.
 *
 * Base API:
 * https://www.imf.org/external/datamapper/api/
 *
 * Example indicator:
 * PCPIPCH = Inflation, percent change
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type IMFResponse = {
  PCPIPCH: Record<string, number>
}

async function fetchImfInflation(countryCode: string): Promise<IMFResponse> {
  const url =
    `https://www.imf.org/external/datamapper/api/v1/PCPIPCH?countries=${countryCode}`

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`IMF request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollImf(world: any, pillarDefaults: any) {
  // USA for now — you can expand to multi-country later
  const data = await fetchImfInflation("USA")

  const inflation = data.PCPIPCH["USA"]

  const packet = {
    sourceName: "IMF",
    sourceUrl: "https://www.imf.org/external/datamapper/api/",
    values: {
      inflationRate: inflation,      // global risk
      currencyStress: inflation,     // economy pillar
      sovereignRisk: inflation * 0.5 // optional mapping
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}