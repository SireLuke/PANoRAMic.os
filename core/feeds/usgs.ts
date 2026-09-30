// core/feeds/usgs.ts

/**
 * USGS Earthquake Feed
 * Real, public, no-auth endpoint.
 *
 * Example:
 * https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&orderby=time&limit=1
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type USGSEarthquakeResponse = {
  features: Array<{
    properties: {
      mag: number
      place: string
      time: number
    }
    geometry: {
      coordinates: [number, number, number] // lon, lat, depth
    }
  }>
}

async function fetchLatestEarthquake(): Promise<USGSEarthquakeResponse> {
  const url =
    "https://earthquake.usgs.gov/fdsnws/event/1/query" +
    "?format=geojson&orderby=time&limit=1"

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`USGS request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollUsgs(world: any, pillarDefaults: any) {
  const data = await fetchLatestEarthquake()

  const quake = data.features[0]
  if (!quake) return world

  const magnitude = quake.properties.mag
  const depth = quake.geometry.coordinates[2]
  const place = quake.properties.place

  const packet = {
    sourceName: "USGS",
    sourceUrl: "https://earthquake.usgs.gov",
    values: {
      earthquakeMagnitude: magnitude,
      earthquakeDepth: depth
    },
    nodeTargets: {
      location: place
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}