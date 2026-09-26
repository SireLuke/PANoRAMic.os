import { WorkforceRotationState } from "../../core/pillars/workforce/WORKFORCE_ROTATION_STATE"
import { emitWorkforceRotationSignals } from "../../signals/workforce/workforceRotationSignals"

export function showWorkforceRotation(state: WorkforceRotationState) {
  const signals = emitWorkforceRotationSignals(state)

  console.log("Workforce Rotation Status")
  console.log("-------------------------")
  console.log("Rotation Length:", signals.rotationLength)
  console.log("Disciplines Per Cycle:", signals.disciplinesPerCycle)
  console.log("Skill Gain Rate:", signals.skillGainRate)
  console.log("Burnout Reduction:", signals.burnoutReduction)
  console.log("Workforce Satisfaction:", signals.satisfaction)
}
