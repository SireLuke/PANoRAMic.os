// core/simulation/exportWorld.ts

import { WorldState } from "../worldstate/WorldState"

/**
 * exportWorld:
 * Converts the entire world state into a JSON-safe object.
 * This is the data layer used by dashboards, CLIs, or external systems.
 */

export function exportWorld(world: WorldState): any {
  return {
    tick: world.tick,

    globalSignals: {
      stability: world.globalSignals.stability,
      risk: world.globalSignals.risk,
      synthesis: world.globalSignals.synthesis,
      collapsePressure: world.globalSignals.collapsePressure,
      recoveryStrength: world.globalSignals.recoveryStrength,
    },

    nodes: Object.fromEntries(
      Object.entries(world.nodes).map(([id, node]) => [
        id,
        {
          id: node.id,
          name: node.name,
          nodeType: node.nodeType,
          latitude: node.latitude,
          longitude: node.longitude,
          populationCapacity: node.populationCapacity,
          resourceCapacity: node.resourceCapacity,

          healthIndex: node.healthIndex,
          stressIndex: node.stressIndex,
          autonomyIndex: node.autonomyIndex,
          connectivityIndex: node.connectivityIndex,

          stability: node.stability,
          risk: node.risk,
          load: node.load,
          resilience: node.resilience,

          ecologicalDependency: node.ecologicalDependency,
          infrastructureDependency: node.infrastructureDependency,
          economicDependency: node.economicDependency,
          collapseRisk: node.collapseRisk,

          connections: node.connections,
        },
      ])
    ),

    pillars: {
      population: world.population,
      resources: world.resources,
      economy: world.economy,
      governance: world.governance,
      humanitarian: world.humanitarian,
      medical: world.medical,
      antigenocide: world.antigenocide,
      markets: world.markets,
      crime: world.crime,
      education: world.education,
      migration: world.migration,
      trafficking: world.trafficking,
      transparency: world.transparency,
      corporatecapture: world.corporatecapture,
      epistemic: world.epistemic,
      repairability: world.repairability,
      quantum: world.quantum,
    },
  }
}
