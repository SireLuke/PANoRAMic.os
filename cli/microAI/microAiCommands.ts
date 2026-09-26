import { MicroAiState } from "../../core/pillars/microAI/MICRO_AI_STATE"
import { emitMicroAiSignals } from "../../signals/microAI/microAiSignals"

export function showMicroAi(state: MicroAiState) {
  const signals = emitMicroAiSignals(state)

  console.log("Micro-AI & Node Intelligence Status")
  console.log("-----------------------------------")
  console.log("Node Intelligence:", signals.nodeIntelligence)
  console.log("Retrieval Quality:", signals.retrievalQuality)
  console.log("Cooperative Agents:", signals.cooperativeAgents)
  console.log("Local Autonomy:", signals.localAutonomy)
  console.log("Safety Guardrails:", signals.safetyGuardrails)
  console.log("Coverage:", signals.coverage)
}
