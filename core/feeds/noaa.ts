// core/feeds/noaa.ts

/**
 * NOAA Weather API Feed
 * Real, public, no-auth endpoint.
 *
 * Example:
 * https://api.weather.gov/gridpoints/SGF/63,34/forecast
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type NOAAForecastResponse = {
  properties: {
    periods: Array<{
      name: string
      temperature: number
      windSpeed: string
      shortForecast: string
    }>
  }
}

async function fetchNoaaForecast(): Promise<NOAAForecastResponse> {
  const url = "https://api.weather.gov/gridpoints/SGF/63,34/forecast"

  const res = await fetch(url, {
    headers: {
      "User-Agent": "PAN-OS/1.0 (youremail@example.com)"
    }
  })

  if (!res.ok) {
    throw new Error(`NOAA request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollNoaa(world: any, pillarDefaults: any) {
  const data = await fetchNoaaForecast()

  const firstPeriod = data.properties.periods[0]

  const packet = {
    sourceName: "NOAA",
    sourceUrl: "https://api.weather.gov",
    values: {
      // Map to your UniversalMappingRules keys
      localStormSeverity:
        firstPeriod.shortForecast.includes("storm") ||
        firstPeriod.shortForecast.includes("thunder")
          ? 1
          : 0,

      temperature: firstPeriod.temperature,
      windSpeed: parseInt(firstPeriod.windSpeed)
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}