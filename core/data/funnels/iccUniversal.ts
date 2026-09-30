// core/data/funnels/iccUniversal.ts

import { registerFunnel } from "../../data/funnelManager"
import { mapIncomingToPillar, applyPillarUpdates } from "../../data/pillarMapping"
import { mapIncomingToGlobal, applyGlobalUpdates } from "../../data/globalMapping"
import { UniversalMappingRules, applyMappingRules } from "../mappingRules"
import { ProvenanceTracker, hashData } from "../../data/provenance"

const provenance = new ProvenanceTracker()

registerFunnel("epistemic", (incoming, world) => {
  const updatedWorld = { ...world }
  const weight = incoming._trustWeight ?? 1

  const values = incoming.values || {}
  const rules = UniversalMappingRules

  // PILLAR UPDATES (medical, humanitarian, resources, economy, governance, markets, crime, quantum...)
  if (rules.pillarRules) {
    for (const pillarName in rules.pillarRules) {
      const pillarRuleSet = rules.pillarRules[pillarName]
      const mapped = applyMappingRules(values, pillarRuleSet)

      const weightedMapped: any = {}
      for (const key in mapped) {
        weightedMapped[key] = mapped[key] * weight
      }

      Object.assign(updatedWorld, applyPillarUpdates(updatedWorld, pillarName, weightedMapped))
    }
  }

  // GLOBAL UPDATES (risk, stability, collapsePressure, etc.)
  if (rules.globalRules) {
    const mappedGlobals = applyMappingRules(values, rules.globalRules)

    const weightedGlobals: any = {}
    for (const key in mappedGlobals) {
      weightedGlobals[key] = mappedGlobals[key] * weight
    }

    Object.assign(updatedWorld, applyGlobalUpdates(updatedWorld, weightedGlobals))
  }

  // NODE UPDATES (local stress signals)
  if (rules.nodeRules && incoming.nodeTargets) {
    const mappedNode = applyMappingRules(values, rules.nodeRules)

    const weightedNode: any = {}
    for (const key in mappedNode) {
      weightedNode[key] = mappedNode[key] * weight
    }

    // you can plug this into your existing nodeMapping.applyNodeUpdates
    // when you’re ready to route by location / ids
  }

  provenance.addRecord({
    timestamp: Date.now(),
    funnelType: "iccUniversal",
    sourceName: incoming.sourceName || "Unknown",
    sourceUrl: incoming.sourceUrl,
    affectedPillars: rules.pillarRules ? Object.keys(rules.pillarRules) : [],
    affectedGlobals: rules.globalRules ? rules.globalRules.map(r => r.targetKey) : [],
    trustScore: weight,
    rawDataHash: hashData(incoming)
  })

  return updatedWorld
})

export function getIccUniversalProvenance() {
  return provenance.getHistory()
}