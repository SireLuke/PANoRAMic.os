import { NodeState } from "../../core/pillars/nodes/NODES_STATE"
import { emitNodeSignals } from "../../signals/nodes/nodesSignals"

export function showNode(state: NodeState) {
  const signals = emitNodeSignals(state)

  console.log("Node Status")
  console.log("-----------")
  console.log("Node ID:", state.nodeId)
  console.log("Health:", signals.health)
  console.log("Autonomy:", signals.autonomy)
  console.log("Connectivity:", signals.connectivity)
  console.log("Storage Capacity:", signals.storage)
  console.log("AI Presence:", signals.aiPresence)
}
