import { WorkforceRotationState } from "../../core/pillars/workforce/WORKFORCE_ROTATION_STATE"

export function emitWorkforceRotationSignals(state: WorkforceRotationState) {
  return {
    rotationLength: state.rotationLengthHours,
    disciplinesPerCycle: state.disciplinesPerCycle,
    skillGainRate: state.skillGainRate,
    burnoutReduction: state.burnoutReductionIndex,
    satisfaction: state.workforceSatisfactionIndex,
  }
}
