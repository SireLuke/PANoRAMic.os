import { NodeState } from "../../core/pillars/nodes/NODES_STATE"

export function emitNodeSignals(state: NodeState) {
  return {
    health: state.nodeHealthIndex,
    autonomy: state.nodeAutonomyIndex,
    connectivity: state.nodeConnectivityIndex,
    storage: state.nodeStorageCapacity,
    aiPresence: state.nodeAiPresenceIndex,
  }
}
