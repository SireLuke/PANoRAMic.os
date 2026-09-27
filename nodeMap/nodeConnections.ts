// nodeMap/nodeConnections.ts

import { NodeMap } from "./nodeMap"
import { NodeProfile } from "./nodeProfile"

/**
 * Validate that a connection between two nodes is allowed
 */
export function validateConnection(a: NodeProfile, b: NodeProfile): boolean {
  // Nodes cannot connect to themselves
  if (a.id === b.id) return false

  // Basic rule: nodes can connect across any pillar
  // but certain high‑risk nodes should not directly connect
  const forbiddenPairs = [
    ["trafficking", "rights"],
    ["catastrophe", "population"],
    ["collapse", "infrastructure"],
  ]

  for (const [x, y] of forbiddenPairs) {
    if (a.type === x && b.type === y) return false
    if (a.type === y && b.type === x) return false
  }

  return true
}

/**
 * Connect two nodes if valid
 */
export function safeConnect(map: NodeMap, aId: string, bId: string) {
  const a = map.nodes[aId]
  const b = map.nodes[bId]

  if (!a || !b) return false
  if (!validateConnection(a, b)) return false

  a.connections.push(bId)
  b.connections.push(aId)

  return true
}

/**
 * Compute connection strength between two nodes
 */
export function connectionStrength(a: NodeProfile, b: NodeProfile): number {
  // Stronger if both nodes have high autonomy + connectivity
  const base =
    (a.autonomyIndex + b.autonomyIndex) * 0.4 +
    (a.connectivityIndex + b.connectivityIndex) * 0.6

  return Math.min(1, base / 2)
}

/**
 * Propagate stress across connected nodes
 */
export function propagateStress(map: NodeMap) {
  for (const id in map.nodes) {
    const node = map.nodes[id]

    for (const targetId of node.connections) {
      const target = map.nodes[targetId]
      if (!target) continue

      const strength = connectionStrength(node, target)

      // Stress spreads proportionally to connection strength
      target.stressIndex = Math.min(
        1,
        target.stressIndex + node.stressIndex * strength * 0.1
      )
    }
  }
}
