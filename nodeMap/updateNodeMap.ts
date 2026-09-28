// nodeMap/updateNodeMap.ts
import { NodeProfile } from "../core/pillars/nodes/NodeProfile"
import { NodeState } from "../core/pillars/nodes/NODES_STATE"
import { stateToProfile, profileToState } from "./nodeAdapters"

import { propagateStress } from "./nodeConnections"
import { auditNode } from "../rams/nodes/nodesAudit"
import { computeNode } from "../engine/nodes/nodesEngine"

import { computeNodeRisk } from "../engine/nodes/NodeRiskEngine"
import { computeNodeStability } from "../engine/nodes/NodeStabilityEngine"
import { computeNodeFlow } from "../engine/nodes/NodeFlowEngine"
import { applyNodeRecovery } from "../engine/nodes/NodeRecoveryEngine"
import { applyNodeCollapse } from "../engine/nodes/NodeCollapseEngine"
import { computeNodeSynthesis } from "../engine/nodes/NodeSynthesisEngine"
import { computeNodeHealth } from "../core/pillars/nodes/NODES_STATE"

// nodes: Record<string, NodeState>
export function updateNodeMap(nodes: Record<string, NodeState>): Record<string, NodeState> {
  // 1) propagate stress across connections (works on NodeState)
  propagateStress(nodes)

  const updated: Record<string, NodeState> = {}

  for (const id in nodes) {
    const prevState = nodes[id]

    // 2) adapt state -> profile for engines that expect profile
    let profile: NodeProfile = stateToProfile(prevState)

    // 3) run engine pipeline (risk, stability, flow, recovery, collapse, synthesis)
    const riskResult = computeNodeRisk(profile)
    profile.riskIndex = (riskResult?.riskScore ?? 0) / 100

    const stabilityResult = computeNodeStability(profile)
    profile.stabilityIndex = (stabilityResult?.stabilityScore ?? 0) / 100

    const flowResult = computeNodeFlow(profile)
    profile = flowResult?.updatedNode ?? profile

    const recoveryResult = applyNodeRecovery(profile)
    profile = recoveryResult?.updatedNode ?? profile

    const collapseResult = applyNodeCollapse(profile)
    profile = collapseResult?.updatedNode ?? profile

    const synthesisResult = computeNodeSynthesis(profile)
    profile.stabilityIndex = (synthesisResult?.synthesisScore ?? 0) / 100

    // 4) RAMS audit influences long-term evolution (your existing logic)
    const audit = auditNode(profile)
    profile.healthIndex = Math.min(1, (profile.healthIndex ?? 0) + (audit?.integrityScore ?? 0) * 0.02)
    profile.stressIndex = Math.max(0, (profile.stressIndex ?? 0) - (audit?.integrityScore ?? 0) * 0.03)

    // 5) final domain compute (your computeNode)
    profile = computeNode(profile) ?? profile

    // 6) convert profile back to NodeState and finalize health
    let nodeState = profileToState(profile, prevState)
    nodeState = computeNodeHealth(nodeState)

    updated[id] = nodeState
  }

  return updated
}
