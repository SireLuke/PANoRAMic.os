// engine/nodes/NodeEvolutionEngine.ts

import { NodeState, computeNodeHealth } from "../../core/pillars/nodes/NODES_STATE.ts"

// Evolution parameters for node behavior
const EVOLUTION_RATE = 0.02
const RISK_SENSITIVITY = 0.03
const LOAD_PRESSURE = 0.025
const RESILIENCE_GAIN = 0.015
const DEPENDENCY_DRAG = 0.02
const COLLAPSE_PRESSURE = 0.04

export function evolveNode(node: NodeState): NodeState {
  let next = { ...node }

  // Stability increases slowly unless risk or load is high
  next.stability += EVOLUTION_RATE
  next.stability -= next.risk * RISK_SENSITIVITY
  next.stability -= next.load * LOAD_PRESSURE

  // Risk increases with dependencies and collapse pressure
  next.risk += next.ecologicalDependency * DEPENDENCY_DRAG
  next.risk += next.infrastructureDependency * DEPENDENCY_DRAG
  next.risk += next.economicDependency * DEPENDENCY_DRAG
  next.risk += next.collapseRisk * COLLAPSE_PRESSURE

  // Resilience grows slowly unless collapse risk is high
  next.resilience += RESILIENCE_GAIN
  next.resilience -= next.collapseRisk * 0.02

  // Load increases with connections (more connections = more pressure)
  next.load += next.connections.length * 0.005

  // Clamp values to 0–1
  next.stability = Math.max(0, Math.min(next.stability, 1))
  next.risk = Math.max(0, Math.min(next.risk, 1))
  next.load = Math.max(0, Math.min(next.load, 1))
  next.resilience = Math.max(0, Math.min(next.resilience, 1))

  // Recompute health
  next = computeNodeHealth(next)

  return next
}

// Apply evolution to all nodes in the map
export function evolveNodeMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    updated[id] = evolveNode(nodes[id])
  }

  return updated
}
