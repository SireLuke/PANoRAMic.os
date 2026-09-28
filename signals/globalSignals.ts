// signals/globalSignals.ts

import { NodeState } from "../core/pillars/nodes/NODES_STATE.ts"
import { WorldState } from "../engine/world/worldState.ts"

// Global signal shape
export interface GlobalSignals {
  // Planetary stability
  stability: number
  risk: number
  collapsePressure: number

  // Planetary flow & synthesis
  flow: number
  synthesis: number

  // Planetary resilience & recovery
  resilience: number
  recovery: number

  // Population & resources
  population: number
  resources: number
  scarcity: number
  sustainability: number

  // Governance & rights
  governance: number
  rights: number
  equity: number

  // Economy & PAR
  parSupply: number
  parCap: number
  stewardship: number
  humanitarianPool: number
  taxLoad: number

  // Ecology
  ecology: number
  renewables: number

  // Infrastructure
  infrastructure: number

  // Humanitarian
  humanitarianNeed: number
  humanitarianRelief: number

  // Migration & trafficking
  migration: number
  trafficking: number

  // Harm index
  harm: number

  // ICC / justice
  icc: number

  // Planetary coherence
  coherence: number
}

// Aggregate node signals
function aggregateNodeSignals(nodes: Record<string, NodeState>) {
  const list = Object.values(nodes)
  const count = list.length || 1

  return {
    stability: list.reduce((a, n) => a + n.stability, 0) / count,
    risk: list.reduce((a, n) => a + n.risk, 0) / count,
    collapsePressure: list.reduce((a, n) => a + n.collapse, 0) / count,
    flow: list.reduce((a, n) => a + n.flow, 0) / count,
    synthesis: list.reduce((a, n) => a + n.synthesis, 0) / count,
    resilience: list.reduce((a, n) => a + n.resilience, 0) / count,
    recovery: list.reduce((a, n) => a + n.recovery, 0) / count,
  }
}

// Aggregate full global signals
export function computeGlobalSignals(world: WorldState): GlobalSignals {
  const nodeSignals = aggregateNodeSignals(world.nodes)

  return {
    // Node-derived signals
    stability: nodeSignals.stability,
    risk: nodeSignals.risk,
    collapsePressure: nodeSignals.collapsePressure,
    flow: nodeSignals.flow,
    synthesis: nodeSignals.synthesis,
    resilience: nodeSignals.resilience,
    recovery: nodeSignals.recovery,

    // Population & resources
    population: world.population.total ?? 0,
    resources: world.resources.resourceScore ?? 0,
    scarcity: world.resources.scarcityScore ?? 0,
    sustainability: world.resources.sustainabilityScore ?? 0,

    // Governance & rights
    governance: world.governance.panitarianScore ?? 0,
    rights: world.rights.accessScore ?? 0,
    equity: world.education.equityScore ?? 0,

    // Economy & PAR
    parSupply: world.economy.parSupply ?? 0,
    parCap: world.economy.parCap ?? 0,
    stewardship: world.economy.stewardshipFund ?? 0,
    humanitarianPool: world.economy.humanitarianPool ?? 0,
    taxLoad: world.economy.taxLoad ?? 0,

    // Ecology
    ecology: world.ecology.healthScore ?? 0,
    renewables: world.metabolism.renewables ?? 0,

    // Infrastructure
    infrastructure: world.infrastructure.integrityScore ?? 0,

    // Humanitarian
    humanitarianNeed: world.humanitarian.needScore ?? 0,
    humanitarianRelief: world.humanitarian.reliefScore ?? 0,

    // Migration & trafficking
    migration: world.migration.migrationScore ?? 0,
    trafficking: world.trafficking.traffickingScore ?? 0,

    // Harm index
    harm: world.harmindex.harmScore ?? 0,

    // ICC / justice
    icc: world.icc.score ?? 0,

    // Planetary coherence
    coherence: world.synthesis.weights ?? 0,
  }
}
