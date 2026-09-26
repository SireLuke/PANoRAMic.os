// cli/src/commands/rams.ts

import { initialWorld } from "../../engine/worldState";
import { runRamsTick } from "../../engine/ramsTick";

export function ramsCommand() {
    const report = runRamsTick(initialWorld);

    console.log("PANoRAMic.os RAMS Report");
    console.log("------------------------");

    for (const [key, value] of Object.entries(report)) {
        console.log(`\n${key.toUpperCase()}:`);
        console.log(`  OK: ${value.ok ? "Yes" : "No"}`);
        console.log(`  Reason: ${value.reason ?? "None"}`);
    }
}
