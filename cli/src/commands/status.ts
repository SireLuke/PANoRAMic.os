// cli/src/commands/status.ts

import { initialWorld } from "../../engine/worldState";
import { aggregateSignals } from "../../engine/globalSignals";

export function statusCommand() {
    const signals = aggregateSignals(initialWorld);

    console.log("PANoRAMic.os Status");
    console.log("--------------------");
    console.log(`Population: ${signals.population}`);
    console.log(`Risk: ${signals.risk}`);
    console.log(`Resilience: ${signals.resilience}`);
    console.log(`Volatility: ${signals.volatility}`);
    console.log(`PAR Supply: ${signals.parSupply}`);
    console.log(`Governance: ${signals.governance}`);
    console.log(`Harm: ${signals.harm}`);
}
