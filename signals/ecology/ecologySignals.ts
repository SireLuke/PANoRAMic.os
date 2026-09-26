import { EcologyState } from "../../core/pillars/ecology/ECOLOGY_STATE"

export function emitEcologySignals(state: EcologyState) {
  return {
    carryingCapacity: state.carryingCapacityIndex,
    regenerationVelocity: state.regenerationVelocity,
    ecologicalDebt: state.ecologicalDebt,
    biodiversity: state.biodiversityScore,
    pollutionLoad: state.pollutionLoadIndex,
    waterSecurity: state.waterSecurityIndex,
    energyRenewability: state.energyRenewabilityIndex,
  }
}
