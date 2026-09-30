// core/data/funnels/libraryOfAlexandria.ts

import { registerFunnel } from "../../data/funnelManager"
import { matchByLocation, matchByRadius, applyNodeUpdates } from "../../data/nodeMapping"
import { mapIncomingToPillar, applyPillarUpdates } from "../../data/pillarMapping"
import { mapIncomingToGlobal, applyGlobalUpdates } from "../../data/globalMapping"
import { smoothGlobalSignals } from "../../data/globalSmoothing"
import { AlertEngine } from "../../data/alertEngine"
import { ForecastEngine } from "../../data/forecastEngine"
import { generateSnapshot } from "../../data/stateSnapshot"
import { computeDiff } from "../../data/stateDiff"
import { ProvenanceTracker, hashData } from "../../data/provenance"

const provenance = new ProvenanceTracker()
const alertEngine = new AlertEngine()
const forecastEngine = new ForecastEngine()

let lastSnapshot: any = null
let lastDiff: any = null

registerFunnel("libraryOfAlexandria", (incoming, world) => {
  const updatedWorld = { ...world }
  const weight = incoming._trustWeight ?? 1

  // NODE UPDATES
  if (incoming.nodeData) {
    const { location, radiusKm, updates } = incoming.nodeData

    let matchedNodes: string[] = []

    if (location?.lat && location?.long && radiusKm) {
      matchedNodes = matchByRadius(world.nodes, location.lat, location.long, radiusKm)
    } else {
      matchedNodes = matchByLocation(world.nodes, incoming.nodeData)
    }

    const weightedUpdates: any = {}
    for (const key in updates) {
      weightedUpdates[key] = updates[key] * weight
    }

    Object.assign(updatedWorld, applyNodeUpdates(updatedWorld, matchedNodes, weightedUpdates))
  }

  // PILLAR UPDATES
  if (incoming.pillarData) {
    for (const pillarName in incoming.pillarData) {
      const { mappingRules, values } = incoming.pillarData[pillarName]

      const mapped = mapIncomingToPillar(values, pillarName, mappingRules)

      const weightedMapped: any = {}
      for (const key in mapped) {
        weightedMapped[key] = mapped[key] * weight
      }

      Object.assign(updatedWorld, applyPillarUpdates(updatedWorld, pillarName, weightedMapped))
    }
  }

  // GLOBAL UPDATES + SMOOTHING + ALERTS + FORECAST + SNAPSHOT + DIFF
  if (incoming.globalData) {
    const mapped = mapIncomingToGlobal(incoming.globalData.values, incoming.globalData.mappingRules)

    const weightedMapped: any = {}
    for (const key in mapped) {
      weightedMapped[key] = mapped[key] * weight
    }

    const smoothed = smoothGlobalSignals(
      updatedWorld.globalSignals,
      weightedMapped,
      incoming.globalData.alpha ?? 0.3
    )

    Object.assign(updatedWorld, applyGlobalUpdates(updatedWorld, smoothed))

    // Alerts
    alertEngine.evaluate(updatedWorld.globalSignals)

    // Forecast
    const forecast = forecastEngine.compute(updatedWorld.globalSignals)

    // Snapshot
    const newSnapshot = generateSnapshot(
      updatedWorld,
      alertEngine.getRecent(),
      forecastEngine.getRecent()
    )

    // Diff
    if (lastSnapshot) {
      lastDiff = computeDiff(lastSnapshot, newSnapshot)
    }

    lastSnapshot = newSnapshot
  }

  // PROVENANCE
  provenance.addRecord({
    timestamp: Date.now(),
    funnelType: "libraryOfAlexandria",
    sourceName: incoming.sourceName || "Unknown",
    sourceUrl: incoming.sourceUrl,
    affectedNodes: incoming.nodeData ? Object.keys(incoming.nodeData) : [],
    affectedPillars: incoming.pillarData ? Object.keys(incoming.pillarData) : [],
    affectedGlobals: incoming.globalData ? Object.keys(incoming.globalData.values) : [],
    trustScore: weight,
    rawDataHash: hashData(incoming)
  })

  return updatedWorld
})

export function getWorldSnapshot() {
  return lastSnapshot
}

export function getWorldDiff() {
  return lastDiff
}