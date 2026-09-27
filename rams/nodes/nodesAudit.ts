import { NodeState } from "../../core/pillars/nodes/NODES_STATE"

export function auditNode(state: NodeState) {
  return {
    dataIntegrity: true,
    healthCheck: state.nodeHealthIndex >= 0,
    autonomyCheck: state.nodeAutonomyIndex >= 0,
    connectivityCheck: state.nodeConnectivityIndex >= 0,
  }
}
