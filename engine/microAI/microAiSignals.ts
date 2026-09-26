import { MicroAiState } from "../../core/pillars/microAI/MICRO_AI_STATE"

export function emitMicroAiSignals(state: MicroAiState) {
  return {
    nodeIntelligence: state.nodeIntelligenceIndex,
    retrievalQuality: state.retrievalQualityIndex,
    cooperativeAgents: state.cooperativeAgentCount,
    localAutonomy: state.localAutonomyIndex,
    safetyGuardrails: state.safetyGuardrailIndex,
    coverage: state.microAiCoverageIndex,
  }
}
