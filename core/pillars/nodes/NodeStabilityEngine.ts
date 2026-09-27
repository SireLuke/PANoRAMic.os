// engine/nodes/NodeStabilityEngine.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE.ts"

// Stability parameters
const BASE_STABILITY_GAIN = 0.02
const RESILIENCE_BOOST = 0.04
const LOAD_PENALTY = 0.05
const RISK_PENALTY = 0.06
const DEPENDENCY_PENALTY = 0.03
const COLLAPSE_PRESSURE = 0.08
const CONNECTION_STABILITY_SHARE = 0.01

export function computeNodeStability(node: NodeState, neighbors: NodeState[]): NodeState {
  let next = { ...node }

  // Base stability gain
  next.stability += BASE_STABILITY_GAIN

  // Resilience increases stability
  next.stability += next.resilience * RESILIENCE_BOOST

  // Load reduces stability
  next.stability -= next.load * LOAD_PENALTY

  // Risk reduces stability
  next.stability -= next.risk * RISK_PENALTY

  // Dependencies reduce stability
  next.stability -= next.ecologicalDependency * DEPENDENCY_PENALTY
  next.stability -= next.infrastructureDependency * DEPENDENCY_PENALTY
  next.stability -= next.economicDependency * DEPENDENCY_PENALTY

  // Collapse pressure sharply reduces stability
  next.stability -= next.collapseRisk * COLLAPSE_PRESSURE

  // Stability sharing from neighbors (network effect)
  for (const neighbor of neighbors) {
    next.stability += neighbor.stability * CONNECTION_STABILITY_SHARE
  }

  // Clamp to 0–1
  next.stability = Math.max(0, Math.min(next.stability, 1))

  return next
}

// Apply stability engine to all nodes in the map
export function computeStabilityMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    const node = nodes[id]

    // Gather neighbors based on connections
    const neighbors = node.connections
      .map(connId => nodes[connId])
      .filter(Boolean)

    updated[id] = computeNodeStability(node, neighbors)
  }

  return updated
}
