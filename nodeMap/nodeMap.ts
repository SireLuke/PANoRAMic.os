// nodeMap/nodeMap.ts

import { NodeProfile } from "../core/pillars/nodes/NodeProfile.ts"
import { NodeState, createNodeState, computeNodeHealth } from "../core/pillars/nodes/NODES_STATE.ts"

import { computeNodeRisk } from "../engine/nodes/NodeRiskEngine.ts"
import { computeNodeStability } from "../engine/nodes/NodeStabilityEngine.ts"
import { computeNodeFlow } from "../engine/nodes/NodeFlowEngine.ts"
import { applyNodeRecovery } from "../engine/nodes/NodeRecoveryEngine.ts"
import { applyNodeCollapse } from "../engine/nodes/NodeCollapseEngine.ts"
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
    let node = nodes[id]

    // Convert NodeState back to NodeProfile for engine processing
    let profile: NodeProfile = {
      id: node.id,
      name: node.name,
      nodeType: node.nodeType,
      stabilityIndex: node.stability,
      riskIndex: node.risk,
      loadIndex: node.load,
      resilienceIndex: node.resilience,
      ecologicalDependencyIndex: node.ecologicalDependency,
      infrastructureDependencyIndex: node.infrastructureDependency,
      economicDependencyIndex: node.economicDependency,
      collapseRiskIndex: node.collapseRisk,
      connections: node.connections,
    }

    // Engine pipeline - each engine returns updated profile properties
    const riskResult = computeNodeRisk(profile)
    profile.riskIndex = riskResult.riskScore / 100 // Normalize back to 0-1
    
    const stabilityResult = computeNodeStability(profile)
    profile.stabilityIndex = stabilityResult.stabilityScore / 100
    
    const flowResult = computeNodeFlow(profile)
    profile = flowResult.updatedNode
    
    const recoveryResult = applyNodeRecovery(profile)
    profile = recoveryResult.updatedNode
    
    const collapseResult = applyNodeCollapse(profile)
    profile = collapseResult.updatedNode
    
    const synthesisResult = computeNodeSynthesis(profile)
    profile.stabilityIndex = synthesisResult.synthesisScore / 100

    // Convert back to NodeState
    node = {
      ...node,
      stability: profile.stabilityIndex,
      risk: profile.riskIndex,
      load: profile.loadIndex,
      resilience: profile.resilienceIndex,
      ecologicalDependency: profile.ecologicalDependencyIndex,
      infrastructureDependency: profile.infrastructureDependencyIndex,
      economicDependency: profile.economicDependencyIndex,
      collapseRisk: profile.collapseRiskIndex,
    }

    // Compute final health
    node = computeNodeHealth(node)
    updated[id] = node
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
