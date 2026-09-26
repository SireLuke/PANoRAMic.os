import { RightsState } from "../../core/pillars/rights/RIGHTS_STATE"

export function emitRightsSignals(state: RightsState) {
  return {
    genderEquality: state.genderEqualityIndex,
    identityInclusion: state.identityInclusionScore,
    bodilyAutonomy: state.bodilyAutonomyAccessIndex,
    antiDiscrimination: state.antiDiscriminationSignal,
    violenceRisk: state.violenceRiskIndex,
    rightsProtection: state.rightsProtectionIndex,
  }
}
