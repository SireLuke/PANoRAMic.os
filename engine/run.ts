// engine/run.ts
//
// Compatibility facade for the canonical world lifecycle.
// The previous file mixed two unrelated initializers, referenced removed
// travel/incentive modules, and contained malformed object/function boundaries.
// Keep this entry point small and delegate state construction and advancement
// to the canonical engine/world implementation.

import { initWorld } from "./world/initWorld.ts";
import { tick } from "./world/tick.ts";
import type { WorldState } from "./world/worldState.ts";

/**
 * Advance the canonical PAN world by one deterministic engine tick.
 *
 * `subsystems` is retained as an optional compatibility argument for older
 * callers. Subsystem orchestration is owned by the canonical world tick path.
 * The returned value is the new WorldState; the input state is not mutated here.
 */
export function run(
  world: WorldState,
  _subsystems?: unknown,
): WorldState {
  return tick(world).world;
}

/**
 * Construct the canonical initial world state with no preloaded node profiles.
 * Call initWorld(profiles) directly when a caller has node profiles to seed.
 */
export function createInitialWorldState(): WorldState {
  return initWorld([]);
}
