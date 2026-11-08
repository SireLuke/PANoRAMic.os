// pillars/repairability/repairabilityEngine.ts
//
// HOLD ENGINE. No dynamics are defined for the Repairability pillar yet.
// It returns the pillar's declared default state with the current state merged over it,
// and rejects non-finite numbers. It exists so core/tick/tickLoop.ts can run end to end;
// replace the body only when a stated, tested model for this pillar exists.

import { WorldState } from "../../core/worldstate/WorldState"
import { Repairability_STATE } from "./STATE"
import { holdPillar } from "../holdPillar"

export function updateRepairability(world: WorldState) {
  return holdPillar(Repairability_STATE, world.repairability, "Repairability")
}
