import { CultureState } from "../../core/pillars/culture/CULTURE_STATE"

export function auditCulture(state: CultureState) {
  return {
    dataIntegrity: true,
    cohesionCheck: state.culturalCohesionIndex >= 0,
    heritageCheck: state.heritagePreservationIndex >= 0,
    narrativeCheck: state.narrativeHealthIndex >= 0,
  }
}
