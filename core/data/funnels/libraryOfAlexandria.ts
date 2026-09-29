// core/data/funnels/libraryOfAlexandria.ts

import { registerFunnel } from "../../data/funnelManager"
import { matchByLocation, matchByRadius, applyNodeUpdates } from "../../data/nodeMapping"
import { mapIncomingToPillar, applyPillarUpdates } from "../../data/pillarMapping"
import { mapIncomingToGlobal, applyGlobalUpdates } from "../../data/globalMapping"
import { ProvenanceTracker, hashData } from "../../data/provenance"

const provenance = new ProvenanceTracker()

/**
 * Library of Alexandria Funnel:
 * Ingests structured + unstructured knowledge and maps it into PAN‑OS.
 */

registerFunnel("libraryOfAlexandria", (incoming, world) => {
  const updatedWorld = { ...world }

  // 1. Node updates (geospatial or semantic)
  if (incoming.nodeData) {
    const { location, radiusKm, updates } = incoming.nodeData

    let matchedNodes: string[] = []

    if (location?.lat && location?.long && radiusKm) {
      matchedNodes = matchByRadius(world.nodes, location.lat, location.long, radiusKm)
    } else {
      matchedNodes = matchByLocation(world.nodes, incoming.nodeData)
    }

    updatedWorld = applyNodeUpdates(updatedWorld, matchedNodes, updates)
  }

  // 2. Pillar updates (semantic mapping)
  if (incoming.pillarData) {
    for (const pillarName in incoming.pillarData) {
      const { mappingRules, values } = incoming.pillarData[pillarName]

      const mapped = mapIncomingToPillar(values, pillarName, mappingRules)
      updatedWorld = applyPillarUpdates(updatedWorld, pillarName, mapped)
    }
  }

  // 3. Global signal updates
  if (incoming.globalData) {
    const mapped = mapIncomingToGlobal(incoming.globalData.values, incoming.globalData.mappingRules)
    updatedWorld = applyGlobalUpdates(updatedWorld, mapped)
  }

  // 4. Provenance tracking
  provenance.addRecord({
    timestamp: Date.now(),
    funnelType: "libraryOfAlexandria",
    sourceName: incoming.sourceName || "Unknown",
    sourceUrl: incoming.sourceUrl,
    affectedNodes: incoming.nodeData ? Object.keys(incoming.nodeData) : [],
    affectedPillars: incoming.pillarData ? Object.keys(incoming.pillarData) : [],
    affectedGlobals: incoming.globalData ? Object.keys(incoming.globalData.values) : [],
    trustScore: incoming.trustScore || 0.5,
    rawDataHash: hashData(incoming)
  })

  return updatedWorld
})

export function getLibraryProvenance() {
  return provenance.getHistory()
}