// engine/nodes/NodeRiskEngine.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE.ts"

// Risk parameters
const BASE_RISK = 0.01
const LOAD_RISK = 0.04
const STABILITY_RISK = 0.05
const RESILIENCE_BUFFER = 0.03
const DEPENDENCY_RISK = 0.035
const COLLAPSE_PRESSURE = 0.06
const CONNECTION_RISK = 0.004

export function computeNodeRisk(node: NodeState): NodeState {
  let next = { ...node }

  // Base risk
  next.risk += BASE_RISK

  // Load increases risk
  next.risk += next.load * LOAD_RISK

  // Low stability increases risk
  next.risk += (1 - next.stability) * STABILITY_RISK

  // Resilience reduces risk
  next.risk -= next.resilience * RESILIENCE_BUFFER

  // Dependencies increase risk
  next.risk += next.ecologicalDependency * DEPENDENCY_RISK
  next.risk += next.infrastructureDependency * DEPENDENCY_RISK
  next.risk += next.economicDependency * DEPENDENCY_RISK

  // Collapse pressure increases risk sharply
  next.risk += next.collapseRisk * COLLAPSE_PRESSURE

  // More connections = more systemic exposure
  next.risk += next.connections.length * CONNECTION_RISK

  // Clamp to 0–1
  next.risk = Math.max(0, Math.min(next.risk, 1))

  return next
}

// Apply risk engine to all nodes
export function computeRiskMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    updated[id] = computeNodeRisk(nodes[id])
  }

  return updated
}
