// engine/world/worldAPI.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile.ts"
import { WorldState } from "./worldState.ts"
import { initWorld } from "./initWorld.ts"
import { tick } from "./tick.ts"
import { runSimulation } from "./bootstrap.ts"

// API: initialize world
export function createWorld(profiles: NodeProfile[]): WorldState {
  return initWorld(profiles)
}

// API: run one tick
export function step(world: WorldState) {
  return tick(world)
}

// API: run multiple ticks
export function stepMany(world: WorldState, count: number) {
  let current = world
  let last = null

  for (let i = 0; i < count; i++) {
    last = tick(current)
    current = last.world
  }

  return last
}

// API: run full simulation from profiles
export function simulate(profiles: NodeProfile[], ticks: number = 1) {
  return runSimulation(profiles, ticks)
}

// API: get signals
export function getSignals(world: WorldState) {
  return world.synthesis ?? {}
}

// API: get nodes
export function getNodes(world: WorldState) {
  return world.nodes
}

// API: get world slice
export function getWorldSlice(world: WorldState, key: keyof WorldState) {
  return world[key]
}
