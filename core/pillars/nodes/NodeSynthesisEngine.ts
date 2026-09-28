// engine/nodes/NodeSynthesisEngine.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE.ts"

// Synthesis parameters
const STABILITY_WEIGHT = 0.25
const RESILIENCE_WEIGHT = 0.20
const FLOW_WEIGHT = 0.15
const RECOVERY_WEIGHT = 0.15

const RISK_PENALTY = 0.20
const LOAD_PENALTY = 0.15
const COLLAPSE_PENALTY = 0.30

const NEIGHBOR_INFLUENCE = 0.05

export function computeNodeSynthesis(node: NodeState, neighbors: NodeState[]): NodeState {
  let next = { ...node }

  // Positive contributions
  let synthesis =
    node.stability * STABILITY_WEIGHT +
    node.resilience * RESILIENCE_WEIGHT +
    node.flow * FLOW_WEIGHT +
    node.recovery * RECOVERY_WEIGHT

  // Negative contributions
  synthesis -= node.risk * RISK_PENALTY
  synthesis -= node.load * LOAD_PENALTY
  synthesis -= node.collapse * COLLAPSE_PENALTY

  // Network influence
  for (const neighbor of neighbors) {
    synthesis += neighbor.stability * NEIGHBOR_INFLUENCE
    synthesis -= neighbor.collapse * NEIGHBOR_INFLUENCE
  }

  // Clamp to 0–1
  next.synthesis = Math.max(0, Math.min(synthesis, 1))

  return next
}

// Apply synthesis engine to all nodes in the map
export function computeSynthesisMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    const node = nodes[id]

    // Gather neighbors based on connections
    const neighbors = node.connections
      .map(connId => nodes[connId])
      .filter(Boolean)

    updated[id] = computeNodeSynthesis(node, neighbors)
  }

  return updated
}
