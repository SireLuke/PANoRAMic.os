import { RightsState } from "../../core/pillars/rights/RIGHTS_STATE"
import { emitRightsSignals } from "../../signals/rights/rightsSignals"

export function showRights(state: RightsState) {
  const signals = emitRightsSignals(state)

  console.log("Universal Human Rights Status")
  console.log("-----------------------------")
  console.log("Gender Equality:", signals.genderEquality)
  console.log("Identity Inclusion:", signals.identityInclusion)
  console.log("Bodily Autonomy:", signals.bodilyAutonomy)
  console.log("Anti-Discrimination:", signals.antiDiscrimination)
  console.log("Violence Risk:", signals.violenceRisk)
  console.log("Rights Protection:", signals.rightsProtection)
}
