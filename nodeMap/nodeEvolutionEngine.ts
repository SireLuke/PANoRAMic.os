// nodeMap/nodeEvolutionEngine.ts

import { NodeMap } from "./nodeMap"
import { NodeProfile } from "./nodeProfile"
import { propagateStress } from "./nodeConnections"
import { auditNode } from "../rams/nodes/nodesAudit"
import { computeNode } from "../engine/nodes/nodesEngine"

/**
 * Node evolution rules:
 * - Stress reduces health
 * - High autonomy increases resilience
 * - High connectivity accelerates recovery
 * - Nodes can shift type under extreme conditions (rare)
 * - RAMS audits influence long-term evolution
 */

export function evolveNode(node: NodeProfile): NodeProfile {
  let updated = { ...node }

  // Health decays under stress
  updated.healthIndex = Math.max(
    0,
    updated.healthIndex - updated.stressIndex * 0.05
  )

  // Autonomy helps resist stress
  updated.healthIndex = Math.min(
    1,
    updated.healthIndex + updated.autonomyIndex * 0.02
  )

  // Connectivity helps recovery
  updated.healthIndex = Math.min(
    1,
    updated.healthIndex + updated.connectivityIndex * 0.01
  )

  // Rare type evolution under extreme stress
  if (updated.stressIndex > 0.9 && updated.healthIndex < 0.2) {
    updated.type = "collapse"
  }

  // Rare positive evolution under high stability
  if (updated.healthIndex > 0.95 && updated.autonomyIndex > 0.8) {
    updated.type = "governance"
  }

  return updated
}

/**
 * Evolve all nodes in the map
 */
export function evolveNodeMap(map: NodeMap) {
  // Step 1: propagate stress across connections
  propagateStress(map)

  // Step 2: evolve each node individually
  for (const id in map.nodes) {
    const node = map.nodes[id]
    map.nodes[id] = evolveNode(node)
  }

  // Step 3: run RAMS audits to adjust long-term evolution
  for (const id in map.nodes) {
    const audit = auditNode(map.nodes[id])

    // RAMS audit influences node stability
    map.nodes[id].healthIndex = Math.min(
      1,
      map.nodes[id].healthIndex + audit.integrityScore * 0.02
    )

    // RAMS audit reduces stress if integrity is high
    map.nodes[id].stressIndex = Math.max(
      0,
      map.nodes[id].stressIndex - audit.integrityScore * 0.03
    )
  }

  // Step 4: compute final node state using node engine
  for (const id in map.nodes) {
    map.nodes[id] = computeNode(map.nodes[id])
  }
}
