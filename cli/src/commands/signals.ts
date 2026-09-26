// cli/src/commands/signals.ts

import { initialWorld } from "../../engine/worldState";
import { aggregateSignals } from "../../engine/globalSignals";

export function signalsCommand() {
    const signals = aggregateSignals(initialWorld);

    console.log("PANoRAMic.os Global Signals");
    console.log("---------------------------");

    for (const [key, value] of Object.entries(signals)) {
        console.log(`${key}: ${value}`);
    }
}

