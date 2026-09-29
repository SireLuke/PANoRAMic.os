// core/simulation/router.ts

import { exportWorld } from "./exportWorld"
import { WorldState } from "../worldstate/WorldState"

/**
 * PAN‑OS Router:
 * Provides clean API endpoints for dashboards or external systems.
 * This is NOT a full server — just the routing logic.
 */

export function createRouter(world: WorldState) {
  return {
    getWorld: () => exportWorld(world),

    getNodes: () => {
      const exported = exportWorld(world)
      return exported.nodes
    },

    getSignals: () => {
      const exported = exportWorld(world)
      return exported.globalSignals
    },

    getPillars: () => {
      const exported = exportWorld(world)
      return exported.pillars
    }
  }
}
