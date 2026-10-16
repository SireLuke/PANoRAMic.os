// engine/worldState.ts
// Compatibility re-export. Canonical type lives in engine/world/worldState.ts.

export type { WorldState } from "./world/worldState";
import { initWorld } from "./world/initWorld";

export const initialWorld = initWorld([]);
