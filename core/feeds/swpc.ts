// core/feeds/swpc.ts

/**
 * NASA / NOAA SWPC Solar Weather Feed
 * Real, public, no-auth endpoint.
 *
 * Example:
 * https://services.swpc.noaa.gov/json/goes/primary/xray.json
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type SWPCResponse = Array<{
  time_tag: string
  flux: number
}>

async function fetchSwpcXray(): Promise<SWPCResponse> {
  const url = "https://services.swpc.noaa.gov/json/goes/primary/xray.json"

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`SWPC request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollSwpc(world: any, pillarDefaults: any) {
  const data = await fetchSwpcXray()

  const latest = data[data.length - 1]
  const flux = latest.flux

  const packet = {
    sourceName: "SWPC",
    sourceUrl: "https://services.swpc.noaa.gov",
    values: {
      solarFlareIntensity: flux,
      geomagneticStress: flux * 0.1
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}