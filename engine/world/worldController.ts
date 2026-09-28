// engine/world/worldController.ts

import { NodeProfile } from "../../core/pillars/nodes/NodeProfile.ts"
import { WorldState } from "./worldState.ts"
import { createWorld, step, stepMany, simulate } from "./worldAPI.ts"

export interface WorldController {
  world: WorldState

  init(profiles: NodeProfile[]): void
  tick(): void
  ticks(count: number): void
  run(profiles: NodeProfile[], count: number): void

  getWorld(): WorldState
  getNodes(): Record<string, any>
  getSignals(): any
}

export function createWorldController(): WorldController {
  let world: WorldState | null = null

  return {
    world: world as WorldState,

    init(profiles: NodeProfile[]) {
      world = createWorld(profiles)
      this.world = world
    },

    tick() {
      if (!world) throw new Error("World not initialized")
      const result = step(world)
      world = result.world
      this.world = world
    },

    ticks(count: number) {
      if (!world) throw new Error("World not initialized")
      const result = stepMany(world, count)
      world = result.world
      this.world = world
    },

    run(profiles: NodeProfile[], count: number) {
      const result = simulate(profiles, count)
      world = result.world
      this.world = world
    },

    getWorld() {
      if (!world) throw new Error("World not initialized")
      return world
    },

    getNodes() {
      if (!world) throw new Error("World not initialized")
      return world.nodes
    },

    getSignals() {
      if (!world) throw new Error("World not initialized")
      return world.synthesis
    },
  }
}
