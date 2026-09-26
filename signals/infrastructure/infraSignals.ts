import { InfrastructureState } from "../../core/pillars/infrastructure/INFRA_STATE"

export function emitInfrastructureSignals(state: InfrastructureState) {
  return {
    desalination: state.desalinationCapacity,
    solarBelt: state.solarBeltOutput,
    recyclingLoop: state.recyclingLoopEfficiency,
    wasteToEnergy: state.wasteToEnergyRate,
    housingUnits: state.cooperativeHousingUnits,
    gridStability: state.gridStabilityIndex,
    infraHealth: state.infrastructureHealthIndex,
  }
}
