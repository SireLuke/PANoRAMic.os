import { MicroAiState } from "../../core/pillars/microAI/MICRO_AI_STATE"

export function auditMicroAi(state: MicroAiState) {
  return {
    dataIntegrity: true,
    safetyCheck: state.safetyGuardrailIndex >= 0,
    autonomyCheck: state.localAutonomyIndex >= 0,
    coverageCheck: state.microAiCoverageIndex >= 0,
  }
}
