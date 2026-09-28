// nodeMap/nodeMap.ts

import { NodeProfile } from "../core/pillars/nodes/NodeProfile.ts"
import { NodeState, createNodeState } from "../core/pillars/nodes/NODES_STATE.ts"

import { evolveNodes } from "../engine/nodes/NodeEvolutionEngine.ts"
import { computeNodeRisk } from "../engine/nodes/NodeRiskEngine.ts"
import { computeNodeStability } from "../engine/nodes/NodeStabilityEngine.ts"
import { computeNodeFlow } from "../engine/nodes/NodeFlowEngine.ts"
import { computeNodeSynthesis } from "../engine/nodes/NodeSynthesisEngine.ts"

// Build initial node map from profiles
export function createNodeMap(profiles: NodeProfile[]): Record<string, NodeState> {
  const map: Record<string, NodeState> = {}

  for (const profile of profiles) {
    map[profile.id] = createNodeState(profile)
  }

  return map
}

// Run all node engines in correct order
export function updateNodeMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    const node = nodes[id]

    // Gather neighbors (not used by engines yet, but kept for future logic)
    const neighbors = node.connections
      .map(connId => nodes[connId])
      .filter(Boolean)

    // Engine pipeline
    let next = evolveNodes(node)
    next = computeNodeRisk(next)
    next = computeNodeStability(next)
    next = computeNodeFlow(next)
    next = computeNodeSynthesis(next)

    updated[id] = next
  }

  return updated
}

// Utility: get neighbors for a node
export function getNodeNeighbors(id: string, nodes: Record<string, NodeState>): NodeState[] {
  const node = nodes[id]
  if (!node) return []

  return node.connections
    .map(connId => nodes[connId])
    .filter(Boolean)
}

