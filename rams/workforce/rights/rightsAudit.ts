import { RightsState } from "../../core/pillars/rights/RIGHTS_STATE"

export function auditRights(state: RightsState) {
  return {
    dataIntegrity: true,
    rightsProtectionCheck: state.rightsProtectionIndex >= 0,
    violenceRiskCheck: state.violenceRiskIndex >= 0,
  }
}
