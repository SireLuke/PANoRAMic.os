// engine/world/bootstrap.ts

import { initWorld } from "./initWorld.ts"
import { tick } from "./tick.ts"
import { NodeProfile } from "../../core/pillars/nodes/NodeProfile.ts"
import { WorldState } from "./worldState.ts"

// Bootstrap result
export interface BootstrapResult {
  world: WorldState
  tick: number
  signals: any
}

// Initialize world and run first tick
export function bootstrap(profiles: NodeProfile[]): BootstrapResult {
  // 1. Build initial world
  const world = initWorld(profiles)

  // 2. Run first tick
  const result = tick(world)

  return result
}

// Run continuous simulation
export function runSimulation(
  profiles: NodeProfile[],
  ticks: number = 1
): BootstrapResult {
  let result = bootstrap(profiles)

  for (let i = 1; i < ticks; i++) {
    result = tick(result.world)
  }

  return result
}
