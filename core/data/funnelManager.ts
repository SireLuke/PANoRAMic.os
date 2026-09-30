// core/data/funnelManager.ts

import { normalizeWorld } from "./normalize"
import { validateWorld } from "./validate"
import { computeTrustScore, checkStructuralIntegrity } from "./trustEngine"
import { HistoryStore, computeHistoricalConsistency } from "./history"
import { SourceAgreementStore } from "./crossSource"
import { MicroAiBalancer } from "../microAI/microAiBalancer"

/**
 * FunnelManager:
 * Routes incoming datasets to the correct funnel adapter.
 * Applies validation + normalization to ensure safe ingestion.
 */

// Funnel types
export type FunnelType =
  | "population"
  | "resources"
  | "economy"
  | "governance"
  | "medical"
  | "humanitarian"
  | "markets"
  | "crime"
  | "education"
  | "migration"
  | "trafficking"
  | "transparency"
  | "corporatecapture"
  | "epistemic"
  | "repairability"
  | "quantum"
  | "nodes"
  | "global"
  | "libraryOfAlexandria"
  | "unknown"

// Step 33 — Historical store
const historyStore = new HistoryStore(200)

// Step 34 — Cross-source agreement store
const agreementStore = new SourceAgreementStore(100)

// Step 41 — Micro-AI load balancer
// CPU/memory monitors (replace with real monitors later)
const balancer = new MicroAiBalancer(
  () => Math.random() * 0.5,  // simulated CPU load
  () => Math.random() * 0.5   // simulated memory load
)

// Funnel adapter registry
const adapters: Record<string, (data: any, world: any) => any> = {}

export function registerFunnel(type: FunnelType, handler: (data: any, world: any) => any) {
  adapters[type] = handler
}

// Detect funnel type from incoming data
export function detectFunnelType(data: any): FunnelType {
  if (!data || typeof data !== "object") return "unknown"

  if (data.nodes) return "nodes"
  if (data.globalSignals) return "global"
  if (data.library) return "libraryOfAlexandria"

  const pillarKeys = [
    "population","resources","economy","governance","medical","humanitarian",
    "markets","crime","education","migration","trafficking","transparency",
    "corporatecapture","epistemic","repairability","quantum"
  ]

  for (const key of pillarKeys) {
    if (data[key]) return key as FunnelType
  }

  return "unknown"
}

// Main ingestion pipeline
export function processFunnelData(world: any, incomingData: any, pillarDefaults: any): any {

  // ⭐ Step 41 — Micro-AI load balancing
  if (!balancer.canProcess()) {
    console.warn("Micro-AI: Ingestion skipped due to load balancing.")
    return world
  }

  const type = detectFunnelType(incomingData)
  const adapter = adapters[type]

  if (!adapter) {
    console.warn(`No adapter registered for funnel type: ${type}`)
    return world
  }

  // Step 34 — Add incoming to cross-source store
  const sourceName = incomingData.sourceName || "Unknown"
  agreementStore.add(sourceName, incomingData)

  const crossSourceAgreement = agreementStore.computeAgreement(incomingData)

  // Step 32 + 33 + 34 — Trust scoring with historical + cross-source
  const trustScore = computeTrustScore({
    sourceReputation: incomingData.sourceReputation ?? 0.5,
    structuralIntegrity: checkStructuralIntegrity(incomingData),
    historicalConsistency: computeHistoricalConsistency(historyStore.getAll(), incomingData),
    recency: incomingData.timestamp ? 1 : 0.5,
    crossSourceAgreement
  })

  if (trustScore < 0.2) {
    console.warn("Incoming dataset rejected due to low trust score.")
    return world
  }

  incomingData._trustWeight = trustScore

  // Adapter transforms incoming data → partial world update
  const updatedWorld = adapter(incomingData, world)

  // Validate + normalize world state
  const validated = validateWorld(updatedWorld, pillarDefaults)
  const normalized = normalizeWorld(validated)

  // Step 33 — Add to historical store
  historyStore.add(incomingData)

  return normalized
}