// engine/system/systemLoop.ts

import { SystemState } from "../../core/SystemState"
import { computeSystem } from "./systemEngine"

export function runSystemLoop(initialState: SystemState, cycles: number) {
  let state = initialState
  const history: SystemState[] = []

  for (let i = 0; i < cycles; i++) {
    state = computeSystem(state)
    history.push(state)
  }

  return {
    finalState: state,
    history,
  }
}
