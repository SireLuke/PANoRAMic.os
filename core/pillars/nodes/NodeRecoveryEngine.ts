// engine/nodes/NodeRecoveryEngine.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE.ts"

// Recovery parameters
const BASE_RECOVERY = 0.03
const RESILIENCE_RECOVERY = 0.05
const STABILITY_RECOVERY = 0.04
const LOAD_RECOVERY_PENALTY = 0.03
const RISK_RECOVERY_PENALTY = 0.04
const DEPENDENCY_RECOVERY_PENALTY = 0.025
const COLLAPSE_RECOVERY_PENALTY = 0.06
const NEIGHBOR_SUPPORT = 0.02

export function computeNodeRecovery(node: NodeState, neighbors: NodeState[]): NodeState {
  let next = { ...node }

  // Base recovery
  next.recovery = BASE_RECOVERY

  // Resilience boosts recovery
  next.recovery += node.resilience * RESILIENCE_RECOVERY

  // Stability boosts recovery
  next.recovery += node.stability * STABILITY_RECOVERY

  // Load reduces recovery
  next.recovery -= node.load * LOAD_RECOVERY_PENALTY

  // Risk reduces recovery
  next.recovery -= node.risk * RISK_RECOVERY_PENALTY

  // Dependencies reduce recovery
  next.recovery -= node.ecologicalDependency * DEPENDENCY_RECOVERY_PENALTY
  next.recovery -= node.infrastructureDependency * DEPENDENCY_RECOVERY_PENALTY
  next.recovery -= node.economicDependency * DEPENDENCY_RECOVERY_PENALTY

  // Collapse pressure sharply reduces recovery
  next.recovery -= node.collapseRisk * COLLAPSE_RECOVERY_PENALTY

  // Neighbor support (network healing)
  for (const neighbor of neighbors) {
    next.recovery += neighbor.resilience * NEIGHBOR_SUPPORT
    next.recovery += neighbor.stability * NEIGHBOR_SUPPORT
  }

  // Clamp to 0–1
  next.recovery = Math.max(0, Math.min(next.recovery, 1))

  return next
}

// Apply recovery engine to all nodes in the map
export function computeRecoveryMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    const node = nodes[id]

    // Gather neighbors based on connections
    const neighbors = node.connections
      .map(connId => nodes[connId])
      .filter(Boolean)

    updated[id] = computeNodeRecovery(node, neighbors)
  }

  return updated
}
