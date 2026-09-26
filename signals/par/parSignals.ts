import { ParState } from "../../core/pillars/par/PAR_STATE"

export function emitParSignals(state: ParState) {
  return {
    supply: state.totalParSupply,
    cap: state.parCap,
    circulation: state.parInCirculation,
    stewardshipFund: state.stewardshipFund,
    humanitarianPool: state.humanitarianPool,
    velocity: state.parVelocity,
    burnRate: state.parBurnRate,
    mintRate: state.parMintRate,
  }
}
