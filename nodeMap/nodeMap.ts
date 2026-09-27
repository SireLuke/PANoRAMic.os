// nodeMap/nodeMap.ts

import { NodeProfile } from "../pillars/nodes/NodeProfile"
import { defaultNodeState } from "../pillars/nodes/NODES_STATE"
import { nodeSignalKeys } from "../pillars/nodes/NODES_SIGNALS"
import { computeNode } from "../engine/nodes/nodesEngine"
import { auditNode } from "../rams/nodes/nodesAudit"

export interface NodeMap {
  nodes: Record<string, NodeProfile>
}

/**
 * Create a unified node map from default node state
 */
export function createNodeMap(): NodeMap {
  const map: NodeMap = { nodes: {} }

  for (const id in defaultNodeState) {
    map.nodes[id] = {
      ...defaultNodeState[id],
      connections: [],
    }
  }

  return map
}

/**
 * Connect two nodes bidirectionally
 */
export function connectNodes(map: NodeMap, a: string, b: string) {
  if (!map.nodes[a] || !map.nodes[b]) return

  map.nodes[a].connections.push(b)
  map.nodes[b].connections.push(a)
}

/**
 * Update all nodes using the nodesEngine
 */
export function updateNodes(map: NodeMap) {
  for (const id in map.nodes) {
    const node = map.nodes[id]
    const updated = computeNode(node)
    map.nodes[id] = updated
  }
}

/**
 * Emit signals for all nodes
 */
export function emitNodeMapSignals(map: NodeMap) {
  const signals: Record<string, any> = {}

  for (const id in map.nodes) {
    const node = map.nodes[id]
    signals[id] = {
      health: node[nodeSignalKeys.health],
      autonomy: node[nodeSignalKeys.autonomy],
      connectivity: node[nodeSignalKeys.connectivity],
      storage: node[nodeSignalKeys.storage],
      aiPresence: node[nodeSignalKeys.aiPresence],
    }
  }

  return signals
}

/**
 * Run RAMS audits on all nodes
 */
export function auditNodeMap(map: NodeMap) {
  const audits: Record<string, any> = {}

  for (const id in map.nodes) {
    audits[id] = auditNode(map.nodes[id])
  }

  return audits
}
