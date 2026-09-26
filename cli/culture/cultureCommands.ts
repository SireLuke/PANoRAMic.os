import { CultureState } from "../../core/pillars/culture/CULTURE_STATE"
import { emitCultureSignals } from "../../signals/culture/cultureSignals"

export function showCulture(state: CultureState) {
  const signals = emitCultureSignals(state)

  console.log("Culture & Identity Status")
  console.log("-------------------------")
  console.log("Cultural Cohesion:", signals.cohesion)
  console.log("Identity Expression:", signals.expression)
  console.log("Heritage Preservation:", signals.heritage)
  console.log("Narrative Health:", signals.narrative)
  console.log("Cultural Access:", signals.access)
  console.log("Cultural Vitality:", signals.vitality)
}
