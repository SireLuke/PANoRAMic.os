// core/data/funnels/iccUniversal.ts

import { registerFunnel } from "../../data/funnelManager"
import { mapIncomingToPillar, applyPillarUpdates } from "../../data/pillarMapping"
import { mapIncomingToGlobal, applyGlobalUpdates } from "../../data/globalMapping"
import { ProvenanceTracker, hashData } from "../../data/provenance"

const provenance = new ProvenanceTracker()

/**
 * ICC-Universal Funnel:
 * Handles WHO, UN, IMF, World Bank, WTO, NGO, regulatory, climate, energy,
 * humanitarian, migration, crime, trafficking, corporate transparency,
 * epistemic integrity, and planetary health feeds.
 *
 * This is the broadest adapter in PAN-OS.
 */

registerFunnel("epistemic", (incoming, world) => {
  const updatedWorld = { ...world }
  const weight = incoming._trustWeight ?? 1

  // UNIVERSAL PILLAR UPDATES
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

  // UNIVERSAL GLOBAL UPDATES
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
    funnelType: "iccUniversal",
    sourceName: incoming.sourceName || "Unknown",
    sourceUrl: incoming.sourceUrl,
    affectedPillars: incoming.pillarData ? Object.keys(incoming.pillarData) : [],
    affectedGlobals: incoming.globalData ? Object.keys(incoming.globalData.values) : [],
    trustScore: weight,
    rawDataHash: hashData(incoming)
  })

  return updatedWorld
})

export function getIccUniversalProvenance() {
  return provenance.getHistory()
}