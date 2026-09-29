// core/simulation/runSimulation.ts

import { createWorld } from "../worldstate/createWorld"
import { tick } from "../tick/tickLoop"
import { WorldState } from "../worldstate/WorldState"

/**
 * runSimulation:
 * Runs PAN‑OS for a specified number of ticks.
 * Later you can expand this to stream results to a dashboard,
 * save snapshots, or run real-time updates.
 */

export function runSimulation(ticks: number = 10): WorldState {
  let world = createWorld()

  for (let i = 0; i < ticks; i++) {
    world = tick(world)
    world.tick = i + 1

    // Debug output (safe to remove later)
    console.log(`Tick ${world.tick}:`, world.globalSignals)
  }

  return world
}
