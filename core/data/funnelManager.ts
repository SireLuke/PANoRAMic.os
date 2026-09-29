// core/data/funnelManager.ts

import { normalizeWorld } from "./normalize"
import { validateWorld } from "./validate"

/**
 * FunnelManager:
 * Routes incoming datasets to the correct funnel adapter.
 * Applies validation + normalization to ensure safe ingestion.
 */

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

/**
 * Funnel adapters will be added in Step 24.
 * For now, we create a placeholder registry.
 */

const adapters: Record<string, (data: any) => any> = {}

/**
 * registerFunnel:
 * Allows adapters to register themselves.
 */
export function registerFunnel(type: FunnelType, handler: (data: any) => any) {
  adapters[type] = handler
}

/**
 * detectFunnelType:
 * Determines which funnel should handle the incoming dataset.
 * Step 24 will expand this logic.
 */
export function detectFunnelType(data: any): FunnelType {
  if (!data || typeof data !== "object") return "unknown"

  if (data.nodes) return "nodes"
  if (data.globalSignals) return "global"
  if (data.library) return "libraryOfAlexandria"

  // Pillar detection
  const pillarKeys = [
    "population",
    "resources",
    "economy",
    "governance",
    "medical",
    "humanitarian",
    "markets",
    "crime",
    "education",
    "migration",
    "trafficking",
    "transparency",
    "corporatecapture",
    "epistemic",
    "repairability",
    "quantum"
  ]

  for (const key of pillarKeys) {
    if (data[key]) return key as FunnelType
  }

  return "unknown"
}

/**
 * processFunnelData:
 * Main entry point for ingesting external datasets.
 * Applies:
 *  - funnel detection
 *  - adapter routing
 *  - validation
 *  - normalization
 */
export function processFunnelData(world: any, incomingData: any, pillarDefaults: any): any {
  const type = detectFunnelType(incomingData)

  const adapter = adapters[type]
  if (!adapter) {
    console.warn(`No adapter registered for funnel type: ${type}`)
    return world
  }

  // Adapter transforms incoming data → partial world update
  const updatedWorld = adapter(incomingData, world)

  // Validate structure
  const validated = validateWorld(updatedWorld, pillarDefaults)

  // Normalize values
  const normalized = normalizeWorld(validated)

  return normalized
}
