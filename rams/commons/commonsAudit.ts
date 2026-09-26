import { CommonsState } from "../../core/pillars/commons/COMMONS_STATE"

export function auditCommons(state: CommonsState) {
  return {
    dataIntegrity: true,
    accessCheck: state.sharedResourceAccessIndex >= 0,
    publicGoodsCheck: state.publicGoodsHealthIndex >= 0,
    sustainabilityCheck: state.commonsSustainabilityIndex >= 0,
    equityCheck: state.commonsEquityIndex >= 0,
  }
}
