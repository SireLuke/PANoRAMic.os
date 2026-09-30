// core/data/funnels/icc.ts

import { registerFunnel } from "../../data/funnelManager"
import { mapIncomingToPillar, applyPillarUpdates } from "../../data/pillarMapping"
import { mapIncomingToGlobal, applyGlobalUpdates } from "../../data/globalMapping"
import { ProvenanceTracker, hashData } from "../../data/provenance"

const provenance = new ProvenanceTracker()

/**
 * ICC Funnel:
 * Inter-Civilizational Conduit for WHO, UN, NGO, and global humanitarian feeds.
 *
 * Expected incoming shape:
 * {
 *   sourceName: string
 *   sourceUrl?: string
 *   pillarData?: {
 *     medical?: { mappingRules, values }
 *     humanitarian?: { mappingRules, values }
 *     governance?: { mappingRules, values }
 *   }
 *   globalData?: {
 *     mappingRules: any
 *     values: Record<string, number>
 *   }
 * }
 */

registerFunnel("epistemic", (incoming, world) => {
  const updatedWorld = { ...world }
  const weight = incoming._trustWeight ?? 1

  // PILLAR UPDATES (medical, humanitarian, governance, etc.)
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

  // GLOBAL UPDATES (planetary health, humanitarian pressure, governance stability)
  if (incoming.globalData) {
    const mapped = mapIncomingToGlobal(incoming.globalData.values, incoming.globalData.mappingRules)

    const weightedMapped: any = {}
    for (const key in mapped) {
      weightedMapped[key] = mapped[key] * weight
    }

    Object.assign(updatedWorld, applyGlobalUpdates(updatedWorld, weightedMapped))
  }

  // PROVENANCE
  provenance.addRecord({
    timestamp: Date.now(),
    funnelType: "icc",
    sourceName: incoming.sourceName || "Unknown",
    sourceUrl: incoming.sourceUrl,
    affectedPillars: incoming.pillarData ? Object.keys(incoming.pillarData) : [],
    affectedGlobals: incoming.globalData ? Object.keys(incoming.globalData.values) : [],
    trustScore: weight,
    rawDataHash: hashData(incoming)
  })

  return updatedWorld
})

export function getIccProvenance() {
  return provenance.getHistory()
}