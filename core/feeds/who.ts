// core/feeds/who.ts

/**
 * WHO Outbreak Feed
 * Real, public, no-auth endpoint.
 *
 * Base API:
 * https://ghoapi.azureedge.net/api/
 *
 * Example indicator:
 * WHOSIS_000001 = Number of cases
 */

import { pushExternalFeedToPanOs } from "./feedBridge"

type WHOResponse = {
  value: Array<{
    SpatialDim: string
    TimeDim: string
    NumericValue: number
  }>
}

async function fetchWhoCases(): Promise<WHOResponse> {
  const url = "https://ghoapi.azureedge.net/api/WHOSIS_000001"

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`WHO request failed: ${res.status}`)
  }

  return res.json()
}

export async function pollWho(world: any, pillarDefaults: any) {
  const data = await fetchWhoCases()

  if (!data.value || data.value.length === 0) return world

  // Take the most recent entry
  const latest = data.value[0]

  const packet = {
    sourceName: "WHO",
    sourceUrl: "https://ghoapi.azureedge.net/api/",
    values: {
      globalInfectionRate: latest.NumericValue, // maps to global risk
      infectionRate: latest.NumericValue        // maps to medical pillar
    },
    nodeTargets: {
      location: latest.SpatialDim
    }
  }

  const updated = pushExternalFeedToPanOs(world, packet, pillarDefaults)
  return updated
}