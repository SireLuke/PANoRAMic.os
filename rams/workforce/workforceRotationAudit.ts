import { WorkforceRotationState } from "../../core/pillars/workforce/WORKFORCE_ROTATION_STATE"

export function auditWorkforceRotation(state: WorkforceRotationState) {
  return {
    dataIntegrity: true,
    rotationCheck: state.rotationLengthHours === 4,
    disciplineCheck: state.disciplinesPerCycle >= 2,
    burnoutCheck: state.burnoutReductionIndex >= 0,
  }
}
