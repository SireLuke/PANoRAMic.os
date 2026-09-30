// core/feeds/epa.ts

/**
 * EPA Air Quality Feed (AirNow API)
 * Real endpoint, requires free API key.
 *
 * Docs:
 * https://docs.airnowapi.org/
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type EPAResponse = Array<{
  AQI: number
  Category: { Number: number; Name: string }
  ParameterName: string
  Latitude: number
  Longitude: number
}>

const EPA_API_KEY = process.env.EPA_API_KEY || "" // put your key in .env

async function fetchEpaAirQuality(lat: number, lon: number): Promise<EPAResponse> {
  const url =
    `https://www.airnowapi.org/aq/observation/latLong/current/` +
    `?format=application/json` +
    `&latitude=${lat}` +
    `&longitude=${lon}` +
    `&distance=25` +
    `&API_KEY=${EPA_API_KEY}`

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`EPA request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollEpa(world: any, pillarDefaults: any) {
  // Joplin coordinates — you can expand later
  const lat = 37.0
  const lon = -94.5

  const data = await fetchEpaAirQuality(lat, lon)
  if (!data || data.length === 0) return world

  // Pick PM2.5 or AQI as primary signal
  const pm25 = data.find(d => d.ParameterName === "PM2.5")
  const aqi = data[0]

  const packet = {
    sourceName: "EPA",
    sourceUrl: "https://www.airnowapi.org",
    values: {
      airQualityIndex: aqi.AQI,
      pollutionLevel: pm25 ? pm25.AQI : aqi.AQI,
      pollutionCategory: aqi.Category.Number
    },
    nodeTargets: {
      location: "Joplin-MO",
      lat,
      lon
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}