import { CommonsState } from "../../core/pillars/commons/COMMONS_STATE"
import { emitCommonsSignals } from "../../signals/commons/commonsSignals"

export function showCommons(state: CommonsState) {
  const signals = emitCommonsSignals(state)

  console.log("Commons & Shared Resources Status")
  console.log("---------------------------------")
  console.log("Access:", signals.access)
  console.log("Public Goods Health:", signals.publicGoods)
  console.log("Stewardship Participation:", signals.stewardship)
  console.log("Sustainability:", signals.sustainability)
  console.log("Cooperative Use Rate:", signals.cooperativeUse)
  console.log("Equity:", signals.equity)
}
