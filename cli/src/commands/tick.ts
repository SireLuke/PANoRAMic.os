// cli/src/commands/tick.ts

import { reduceWorld } from "../../engine/worldReducer";
import { initialWorld } from "../../engine/worldState";

export async function tickCommand() {
    const next = await reduceWorld(initialWorld);
    console.log("World tick complete.");
    console.log(JSON.stringify(next, null, 2));
}
