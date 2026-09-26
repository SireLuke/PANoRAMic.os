import { WorkforceRotationState } from "../../core/pillars/workforce/WORKFORCE_ROTATION_STATE"

export function computeWorkforceRotation(state: WorkforceRotationState): WorkforceRotationState {
  return {
    ...state,
    skillGainRate: state.disciplinesPerCycle * 0.05,
    burnoutReductionIndex: 1 - (state.rotationLengthHours / 12),
    workforceSatisfactionIndex: (state.skillGainRate + state.burnoutReductionIndex) / 2,
  }
}
