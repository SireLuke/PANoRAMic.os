// pillars/trafficking/traffickingEngine.ts
//
// HOLD ENGINE. No dynamics are defined for the Trafficking pillar yet.
// It returns the pillar's declared default state with the current state merged over it,
// and rejects non-finite numbers. It exists so core/tick/tickLoop.ts can run end to end;
// replace the body only when a stated, tested model for this pillar exists.

import { WorldState } from "../../core/worldstate/WorldState"
import { Trafficking_STATE } from "./STATE"
import { holdPillar } from "../holdPillar"

export function updateTrafficking(world: WorldState) {
  return holdPillar(Trafficking_STATE, world.trafficking, "Trafficking")
}
