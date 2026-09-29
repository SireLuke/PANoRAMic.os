// core/worldstate/globalSignalsEngine.ts

import { WorldState } from "./WorldState"
import { NodeState } from "../pillars/nodes/NODES_STATE"

export function computeGlobalSignals(world: WorldState): WorldState {
  const nodes = Object.values(world.nodes || {})

  if (nodes.length === 0) {
    return {
      ...world,
      globalSignals: {
        stability: 0,
        risk: 0,
        synthesis: 0,
        collapsePressure: 0,
        recoveryStrength: 0,
      },
    }
  }

  const avg = (values: number[]) =>
    values.length === 0
      ? 0
      : values.reduce((a, b) => a + b, 0) / values.length

  const stability = avg(nodes.map((n: NodeState) => n.stability ?? 0))
  const risk = avg(nodes.map((n: NodeState) => n.risk ?? 0))
  const load = avg(nodes.map((n: NodeState) => n.load ?? 0))
  const resilience = avg(nodes.map((n: NodeState) => n.resilience ?? 0))
  const collapseRisk = avg(nodes.map((n: NodeState) => n.collapseRisk ?? 0))

  const synthesis = stability - risk - load + resilience
  const collapsePressure = collapseRisk + risk + load - resilience
  const recoveryStrength = resilience - collapseRisk

  return {
    ...world,
    globalSignals: {
      stability,
      risk,
      synthesis,
      collapsePressure,
      recoveryStrength,
    },
  }
}
