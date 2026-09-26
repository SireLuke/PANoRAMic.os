import { LaborState } from "../../core/pillars/labor/LABOR_STATE"

export function auditLabor(state: LaborState) {
  return {
    dataIntegrity: true,
    dignityCheck: state.laborDignityIndex >= 0,
    compensationCheck: state.fairCompensationIndex >= 0,
    safetyCheck: state.laborSafetyIndex >= 0,
    stabilityCheck: state.laborStabilityIndex >= 0,
  }
}
