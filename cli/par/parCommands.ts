import { ParState } from "../../core/pillars/par/PAR_STATE"
import { emitParSignals } from "../../signals/par/parSignals"

export function showPar(state: ParState) {
  const signals = emitParSignals(state)

  console.log("PAR Economy Status")
  console.log("------------------")
  console.log("Total Supply:", signals.supply)
  console.log("Cap:", signals.cap)
  console.log("Circulation:", signals.circulation)
  console.log("Stewardship Fund:", signals.stewardshipFund)
  console.log("Humanitarian Pool:", signals.humanitarianPool)
  console.log("Velocity:", signals.velocity)
  console.log("Burn Rate:", signals.burnRate)
  console.log("Mint Rate:", signals.mintRate)
}
