// core/feeds/nasaPower.ts

/**
 * NASA POWER feed:
 * Uses the real public API (no auth) to pull climate/meteorological data.
 *
 * Docs:
 * - https://power.larc.nasa.gov/api/pages/
 * - Example endpoint: /api/temporal/daily/point
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type NasaPowerResponse = {
  properties: {
    parameter: Record<string, Record<string, number>>
  }
}

async function fetchNasaDailyPoint(lat: number, lon: number): Promise<NasaPowerResponse> {
  const start = "20260101"
  const end = "20260102"

  const url =
    `https://power.larc.nasa.gov/api/temporal/daily/point` +
    `?parameters=T2M,ALLSKY_SFC_SW_DWN` +
    `&community=RE` +
    `&longitude=${lon}` +
    `&latitude=${lat}` +
    `&start=${start}` +
    `&end=${end}` +
    `&format=JSON`

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`NASA POWER request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollNasaPower(world: any, pillarDefaults: any) {
  // Joplin-ish coords as an example; you can parameterize this later
  const lat = 37.0
  const lon = -94.5

  const data = await fetchNasaDailyPoint(lat, lon)

  const t2mSeries = data.properties.parameter["T2M"]
  const solarSeries = data.properties.parameter["ALLSKY_SFC_SW_DWN"]

  // Grab the first day in the series
  const firstKey = Object.keys(t2mSeries)[0]
  const temp = t2mSeries[firstKey]
  const solar = solarSeries[firstKey]

  const packet = {
    sourceName: "NASA POWER",
    sourceUrl: "https://power.larc.nasa.gov",
    values: {
      // Map to your UniversalMappingRules keys
      oceanTemp: temp,              // feeds into global risk/collapsePressure
      ALLSKY_SFC_SW_DWN: solar      // you can add a mapping rule for solar flux
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}