// engine/world/world.ts

import { WorldState } from "./worldState.ts"
import { worldReducer } from "./worldReducer.ts"
import { runGlobalLoop } from "../global/globalLoopIntegration.ts"

// Main world runner
export function runWorldTick(prev: WorldState, tick: number = 0) {
  // Run global loop
  const frame = runGlobalLoop(prev, tick)

  // Reduce world state
  const result = worldReducer(prev, frame)

  return result
}
