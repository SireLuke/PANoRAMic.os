import { ParState } from "../../core/pillars/par/PAR_STATE"

export function auditPar(state: ParState) {
  return {
    dataIntegrity: true,
    supplyCheck: state.totalParSupply >= 0,
    capCheck: state.parCap >= 0,
    circulationCheck: state.parInCirculation >= 0,
    stewardshipCheck: state.stewardshipFund >= 0,
    humanitarianCheck: state.humanitarianPool >= 0,
    velocityCheck: state.parVelocity >= 0,
  }
}
