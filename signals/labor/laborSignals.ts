import { LaborState } from "../../core/pillars/labor/LABOR_STATE"

export function emitLaborSignals(state: LaborState) {
  return {
    dignity: state.laborDignityIndex,
    compensation: state.fairCompensationIndex,
    safety: state.laborSafetyIndex,
    mobility: state.skillMobilityIndex,
    stability: state.laborStabilityIndex,
    cooperativeRate: state.cooperativeLaborRate,
  }
}
