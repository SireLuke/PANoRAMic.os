import { CultureState } from "../../core/pillars/culture/CULTURE_STATE"

export function emitCultureSignals(state: CultureState) {
  return {
    cohesion: state.culturalCohesionIndex,
    expression: state.identityExpressionIndex,
    heritage: state.heritagePreservationIndex,
    narrative: state.narrativeHealthIndex,
    access: state.culturalAccessIndex,
    vitality: state.culturalVitalityIndex,
  }
}
