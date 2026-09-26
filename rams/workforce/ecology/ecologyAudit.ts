import { EcologyState } from "../../core/pillars/ecology/ECOLOGY_STATE"

export function auditEcology(state: EcologyState) {
  return {
    dataIntegrity: true,
    carryingCapacityCheck: state.carryingCapacityIndex >= 0,
    pollutionLoadCheck: state.pollutionLoadIndex >= 0,
    waterSecurityCheck: state.waterSecurityIndex >= 0,
    energyRenewabilityCheck: state.energyRenewabilityIndex >= 0,
  }
}
