import { EcologyState } from "../../core/pillars/ecology/ECOLOGY_STATE"
import { emitEcologySignals } from "../../signals/ecology/ecologySignals"

export function showEcology(state: EcologyState) {
  const signals = emitEcologySignals(state)

  console.log("Ecology & Planetary Stability")
  console.log("-----------------------------")
  console.log("Carrying Capacity:", signals.carryingCapacity)
  console.log("Regeneration Velocity:", signals.regenerationVelocity)
  console.log("Ecological Debt:", signals.ecologicalDebt)
  console.log("Biodiversity:", signals.biodiversity)
  console.log("Pollution Load:", signals.pollutionLoad)
  console.log("Water Security:", signals.waterSecurity)
  console.log("Energy Renewability:", signals.energyRenewability)
}
