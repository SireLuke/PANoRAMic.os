// nodeMap/nodeAdapters.ts
import { NodeProfile } from "../core/pillars/nodes/NodeProfile"
import { NodeState } from "../core/pillars/nodes/NODES_STATE"

// Convert NodeState -> NodeProfile
export function stateToProfile(state: NodeState): NodeProfile {
  return {
    id: state.id,
    name: state.name,
    // adapt field names to match your existing profile schema
    type: state.nodeType ?? (state.type as any) ?? "city",
    latitude: state.latitude ?? 0,
    longitude: state.longitude ?? 0,
    populationCapacity: state.populationCapacity ?? 0,
    resourceCapacity: state.resourceCapacity ?? 0,

    // legacy/engine fields your evolveNode expects
    healthIndex: state.healthIndex ?? 0,
    stressIndex: state.stressIndex ?? 0,
    autonomyIndex: state.autonomyIndex ?? 0,
    connectivityIndex: state.connectivityIndex ?? 0,

    // dependency / indices used by other engines
    stabilityIndex: state.stability ?? 0,
    riskIndex: state.risk ?? 0,
    loadIndex: state.load ?? 0,
    resilienceIndex: state.resilience ?? 0,
    ecologicalDependencyIndex: state.ecologicalDependency ?? 0,
    infrastructureDependencyIndex: state.infrastructureDependency ?? 0,
    economicDependencyIndex: state.economicDependency ?? 0,
    collapseRiskIndex: state.collapseRisk ?? 0,

    connections: state.connections ?? []
  } as unknown as NodeProfile
}

// Convert NodeProfile -> NodeState (merge into previous state)
export function profileToState(profile: NodeProfile, prev: NodeState): NodeState {
  return {
    ...prev,
    id: profile.id,
    name: profile.name,
    nodeType: (profile.type as any) ?? prev.nodeType,
    latitude: profile.latitude ?? prev.latitude,
    longitude: profile.longitude ?? prev.longitude,
    populationCapacity: profile.populationCapacity ?? prev.populationCapacity,
    resourceCapacity: profile.resourceCapacity ?? prev.resourceCapacity,

    // legacy fields
    healthIndex: profile.healthIndex ?? prev.healthIndex,
    stressIndex: profile.stressIndex ?? prev.stressIndex,
    autonomyIndex: profile.autonomyIndex ?? prev.autonomyIndex,
    connectivityIndex: profile.connectivityIndex ?? prev.connectivityIndex,

    // normalized indices
    stability: profile.stabilityIndex ?? prev.stability,
    risk: profile.riskIndex ?? prev.risk,
    load: profile.loadIndex ?? prev.load,
    resilience: profile.resilienceIndex ?? prev.resilience,
    ecologicalDependency: profile.ecologicalDependencyIndex ?? prev.ecologicalDependency,
    infrastructureDependency: profile.infrastructureDependencyIndex ?? prev.infrastructureDependency,
    economicDependency: profile.economicDependencyIndex ?? prev.economicDependency,
    collapseRisk: profile.collapseRiskIndex ?? prev.collapseRisk,

    connections: profile.connections ?? prev.connections
  }
}
