import { ModesState } from "../../core/pillars/modes/MODES_STATE"
import { emitModesSignals } from "../../signals/modes/modesSignals"

export function showModes(state: ModesState) {
  const signals = emitModesSignals(state)

  console.log("System Modes Status")
  console.log("-------------------")
  console.log("Active Mode:", signals.active)
  console.log("Stability:", signals.stability)
  console.log("Responsiveness:", signals.responsiveness)
  console.log("Autonomy Level:", signals.autonomy)
  console.log("Safety Level:", signals.safety)
  console.log("Transition Rate:", signals.transitionRate)
}
