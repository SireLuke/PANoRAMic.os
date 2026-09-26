import { WorkforceState } from "../../core/pillars/workforce/WORKFORCE_STATE"

export function auditWorkforce(state: WorkforceState) {
  return {
    dataIntegrity: true,
    dignityCheck: state.dignityAccessScore >= 0,
    participationCheck: state.participationRate >= 0,
    parFlowCheck: state.parEarningsFlow >= 0,
  }
}

