// core/pillars/nodes/NodeState.ts

import { NodeProfile } from "./NodeProfile.ts"

// Dynamic state for each node in PANoRAMic.OS.
// Engines mutate this every tick.

export interface NodeState {
  id: string
  name: string
  nodeType: NodeProfile["nodeType"]

  // Dynamic metrics (0–1)
  stability: number
  risk: number
  load: number
  resilience: number

  // Dependencies (0–1)
  ecologicalDependency: number
  infrastructureDependency: number
  economicDependency: number

  // Collapse risk (0–1)
  collapseRisk: number

  // Node graph connections
  connections: string[]

  // Engine outputs
  flow: number
  synthesis: number
  recovery: number
  collapse: number

  // Health score (0–100)
  healthScore: number
  mode: "stable" | "unstable" | "critical"
}

// Create a NodeState from a NodeProfile
export function createNodeState(profile: NodeProfile): NodeState {
  return {
    id: profile.id,
    name: profile.name,
    nodeType: profile.nodeType,

    stability: profile.stabilityIndex,
    risk: profile.riskIndex,
    load: profile.loadIndex,
    resilience: profile.resilienceIndex,

    ecologicalDependency: profile.ecologicalDependencyIndex,
    infrastructureDependency: profile.infrastructureDependencyIndex,
    economicDependency: profile.economicDependencyIndex,

    collapseRisk: profile.collapseRiskIndex,

    connections: [...profile.connections],

    flow: 0,
    synthesis: 0,
    recovery: 0,
    collapse: 0,

    healthScore: 100,
    mode: "stable",
  }
}

// Update health score based on dynamic state
export function computeNodeHealth(state: NodeState): NodeState {
  let score =
    state.stability * 40 +
    state.resilience * 30 -
    state.load * 25 -
    state.risk * 25

  score -= state.ecologicalDependency * 15
  score -= state.infrastructureDependency * 15
  score -= state.economicDependency * 15
  score -= state.collapseRisk * 30

  score = Math.max(0, Math.min(score, 100))

  let mode: NodeState["mode"] = "stable"
  if (score < 40) mode = "critical"
  else if (score < 70) mode = "unstable"

  return {
    ...state,
    healthScore: score,
    mode,
  }
}
