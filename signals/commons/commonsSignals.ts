import { CommonsState } from "../../core/pillars/commons/COMMONS_STATE"

export function emitCommonsSignals(state: CommonsState) {
  return {
    access: state.sharedResourceAccessIndex,
    publicGoods: state.publicGoodsHealthIndex,
    stewardship: state.stewardshipParticipationRate,
    sustainability: state.commonsSustainabilityIndex,
    cooperativeUse: state.cooperativeUseRate,
    equity: state.commonsEquityIndex,
  }
}
