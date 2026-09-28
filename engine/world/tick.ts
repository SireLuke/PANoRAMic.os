// engine/world/tick.ts

import { WorldState } from "./worldState.ts"
import { runWorldTick } from "./world.ts"

// Tick result
export interface TickResult {
  world: WorldState
  tick: number
  signals: any
}

// Main tick runner
export function tick(world: WorldState): TickResult {
  const result = runWorldTick(world, world.tick)

  return {
    world: result.world,
    tick: result.tick,
    signals: result.signals,
  }
}
