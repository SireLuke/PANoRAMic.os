import { ModesState } from "../../core/pillars/modes/MODES_STATE"

export function auditModes(state: ModesState) {
  return {
    dataIntegrity: true,
    stabilityCheck: state.stabilityIndex >= 0,
    safetyCheck: state.safetyLevel >= 0,
    autonomyCheck: state.autonomyLevel >= 0,
  }
}
