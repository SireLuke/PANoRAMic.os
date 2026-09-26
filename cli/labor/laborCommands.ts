import { LaborState } from "../../core/pillars/labor/LABOR_STATE"
import { emitLaborSignals } from "../../signals/labor/laborSignals"

export function showLabor(state: LaborState) {
  const signals = emitLaborSignals(state)

  console.log("Labor & Cooperative Work Status")
  console.log("-------------------------------")
  console.log("Labor Dignity:", signals.dignity)
  console.log("Fair Compensation:", signals.compensation)
  console.log("Labor Safety:", signals.safety)
  console.log("Skill Mobility:", signals.mobility)
  console.log("Labor Stability:", signals.stability)
  console.log("Cooperative Labor Rate:", signals.cooperativeRate)
}
