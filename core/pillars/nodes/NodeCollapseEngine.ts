// engine/nodes/NodeCollapseEngine.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE.ts"

// Collapse parameters
const BASE_COLLAPSE = 0.01
const RISK_COLLAPSE = 0.06
const LOAD_COLLAPSE = 0.05
const LOW_STABILITY_COLLAPSE = 0.07
const LOW_RESILIENCE_COLLAPSE = 0.05
const DEPENDENCY_COLLAPSE = 0.04
const NEIGHBOR_COLLAPSE_PRESSURE = 0.03
const CASCADE_THRESHOLD = 0.75

export function computeNodeCollapse(node: NodeState, neighbors: NodeState[]): NodeState {
  let next = { ...node }

  // Base collapse pressure
  next.collapse += BASE_COLLAPSE

  // High risk increases collapse
  next.collapse += node.risk * RISK_COLLAPSE

  // High load increases collapse
  next.collapse += node.load * LOAD_COLLAPSE

  // Low stability increases collapse
  next.collapse += (1 - node.stability) * LOW_STABILITY_COLLAPSE

  // Low resilience increases collapse
  next.collapse += (1 - node.resilience) * LOW_RESILIENCE_COLLAPSE

  // Dependencies increase collapse pressure
  next.collapse += node.ecologicalDependency * DEPENDENCY_COLLAPSE
  next.collapse += node.infrastructureDependency * DEPENDENCY_COLLAPSE
  next.collapse += node.economicDependency * DEPENDENCY_COLLAPSE

  // Collapse contagion from neighbors
  for (const neighbor of neighbors) {
    if (neighbor.collapse > CASCADE_THRESHOLD) {
      next.collapse += NEIGHBOR_COLLAPSE_PRESSURE
    }
  }

  // Clamp collapse to 0–1
  next.collapse = Math.max(0, Math.min(next.collapse, 1))

  return next
}

// Apply collapse engine to all nodes in the map
export function computeCollapseMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    const node = nodes[id]

    // Gather neighbors based on connections
    const neighbors = node.connections
      .map(connId => nodes[connId])
      .filter(Boolean)

    updated[id] = computeNodeCollapse(node, neighbors)
  }

  return updated
}
