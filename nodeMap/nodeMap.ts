// nodeMap/nodeMap.ts

import { NodeProfile } from "../nodes/NodeProfile"
import { NODES_STATE } from "../nodes/NODES_STATE"

export interface NodeMap {
  nodes: Record<string, NodeProfile>
}

/**
 * Create a new node map from NODES_STATE
 */
export function createNodeMap(): NodeMap {
  const map: NodeMap = { nodes: {} }

  for (const id in NODES_STATE) {
    map.nodes[id] = { ...NODES_STATE[id] }
  }

  return map
}

/**
 * Connect two nodes
 */
export function connectNodes(map: NodeMap, a: string, b: string) {
  if (!map.nodes[a] || !map.nodes[b]) return

  map.nodes[a].connections.push(b)
  map.nodes[b].connections.push(a)
}

/**
 * Update node health based on stress
 */
export function updateNodeHealth(map: NodeMap) {
  for (const id in map.nodes) {
    const node = map.nodes[id]
    node.healthIndex = Math.max(0, node.healthIndex - node.stressIndex * 0.1)
  }
}
