// engine/tick.ts

import { WorldState } from "./worldState";
import { reduceWorld } from "./worldReducer";
import { aggregateSignals } from "./globalSignals";
import { runRamsTick } from "./ramsTick";

export async function tick(world: WorldState): Promise<WorldState> {
    const updated = await reduceWorld(world);
    const signals = aggregateSignals(updated);
    const rams = runRamsTick(updated);                    const newResult = runGlobalLoop(state)
setResult(newResult)

// Track PAR adoption over time
setParHistory((prev) => [...prev, state.par.adoptionIndex])

    return {
        ...updated,
        time: updated.time + 1,
        globalSignals: signals,
        ramsReport: rams
    };
}


