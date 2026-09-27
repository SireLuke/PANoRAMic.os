// engine/nodes/NodeFlowEngine.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE.ts"

// Flow parameters
const BASE_FLOW = 0.02
const STABILITY_FLOW = 0.03
const RISK_FLOW = 0.04
const LOAD_FLOW = 0.025
const RESILIENCE_FLOW = 0.02
const CONNECTION_FLOW_SHARE = 0.015
const COLLAPSE_FLOW_PRESSURE = 0.05

export function computeNodeFlow(node: NodeState, neighbors: NodeState[]): NodeState {
  let next = { ...node }

  // Base flow
  next.flow = BASE_FLOW

  // Stability contributes positive flow
  next.flow += node.stability * STABILITY_FLOW

  // Risk contributes negative flow
  next.flow -= node.risk * RISK_FLOW

  // Load contributes negative flow
  next.flow -= node.load * LOAD_FLOW

  // Resilience contributes positive flow
  next.flow += node.resilience * RESILIENCE_FLOW

  // Collapse pressure sharply reduces flow
  next.flow -= node.collapseRisk * COLLAPSE_FLOW_PRESSURE

  // Network flow sharing
  for (const neighbor of neighbors) {
    next.flow += neighbor.stability * CONNECTION_FLOW_SHARE
    next.flow -= neighbor.risk * CONNECTION_FLOW_SHARE
  }

  // Clamp flow to 0–1
  next.flow = Math.max(0, Math.min(next.flow, 1))

  return next
}

// Apply flow engine to all nodes in the map
export function computeFlowMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    const node = nodes[id]

    // Gather neighbors based on connections
    const neighbors = node.connections
      .map(connId => nodes[connId])
      .filter(Boolean)

    updated[id] = computeNodeFlow(node, neighbors)
  }

  return updated
}
