// engine/world/worldStatus.ts

import { WorldState } from "./worldState.ts"
import { GlobalFrame } from "../global/globalLoopIntegration.ts"

export interface WorldStatus {
  tick: number
  overallHealth: number
  collapseRisk: number
  recoveryStrength: number
  coherence: number

  nodesHealthy: number
  nodesUnstable: number
  nodesCritical: number

  subsystem: {
    population: number
    resources: number
    governance: number
    ecology: number
    economy: number
    humanitarian: number
    infrastructure: number
    migration: number
    trafficking: number
    harmindex: number
    icc: number
  }

  signals: any
}

export function computeWorldStatus(frame: GlobalFrame): WorldStatus {
  const { world, signals, tick } = frame

  const nodes = Object.values(world.nodes)
  const total = nodes.length || 1

  const nodesHealthy = nodes.filter(n => n.stability > 0.6 && n.collapse < 0.3).length
  const nodesUnstable = nodes.filter(n => n.stability <= 0.6 && n.collapse < 0.7).length
  const nodesCritical = nodes.filter(n => n.collapse >= 0.7).length

  const overallHealth =
    (signals.stability +
      signals.resilience +
      signals.recovery +
      (1 - signals.collapsePressure)) / 4

  return {
    tick,
    overallHealth,
    collapseRisk: signals.collapsePressure,
    recoveryStrength: signals.recovery,
    coherence: signals.coherence,

    nodesHealthy,
    nodesUnstable,
    nodesCritical,

    subsystem: {
      population: world.population.total ?? 0,
      resources: world.resources.resourceScore ?? 0,
      governance: world.governance.panitarianScore ?? 0,
      ecology: world.ecology.healthScore ?? 0,
      economy: world.economy.parSupply ?? 0,
      humanitarian: world.humanitarian.needScore ?? 0,
      infrastructure: world.infrastructure.integrityScore ?? 0,
      migration: world.migration.migrationScore ?? 0,
      trafficking: world.trafficking.traffickingScore ?? 0,
      harmindex: world.harmindex.harmScore ?? 0,
      icc: world.icc.score ?? 0,
    },

    signals,
  }
}
