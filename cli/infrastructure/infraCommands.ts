import { InfrastructureState } from "../../core/pillars/infrastructure/INFRA_STATE"
import { emitInfrastructureSignals } from "../../signals/infrastructure/infraSignals"

export function showInfrastructure(state: InfrastructureState) {
  const signals = emitInfrastructureSignals(state)

  console.log("Planetary Infrastructure Status")
  console.log("-------------------------------")
  console.log("Desalination Capacity:", signals.desalination)
  console.log("Solar Belt Output:", signals.solarBelt)
  console.log("Recycling Loop Efficiency:", signals.recyclingLoop)
  console.log("Waste-to-Energy Rate:", signals.wasteToEnergy)
  console.log("Cooperative Housing Units:", signals.housingUnits)
  console.log("Grid Stability:", signals.gridStability)
  console.log("Infrastructure Health:", signals.infraHealth)
}
