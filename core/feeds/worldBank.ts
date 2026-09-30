// core/feeds/worldBank.ts

/**
 * World Bank Global Indicators Feed
 * Real, public, no-auth endpoint.
 *
 * Example indicator:
 * SP.POP.TOTL = Total population
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type WorldBankResponse = [
  any,
  Array<{
    country: { id: string }
    date: string
    value: number
  }>
]

async function fetchWorldBankIndicator(
  countryCode: string,
  indicator: string
): Promise<WorldBankResponse> {
  const url =
    `https://api.worldbank.org/v2/country/${countryCode}/indicator/${indicator}?format=json`

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`World Bank request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollWorldBank(world: any, pillarDefaults: any) {
  // Example: USA population indicator
  const data = await fetchWorldBankIndicator("USA", "SP.POP.TOTL")

  const latest = data[1][0]
  const population = latest.value

  const packet = {
    sourceName: "World Bank",
    sourceUrl: "https://api.worldbank.org",
    values: {
      // Map into your UniversalMappingRules
      globalPopulation: population,
      resourceStress: population * 0.0000001 // optional mapping
    },
    nodeTargets: {
      location: latest.country.id
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}