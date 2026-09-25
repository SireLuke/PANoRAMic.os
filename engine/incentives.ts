// engine/incentive.ts

import { incentive as coreIncentive } from "../core/incentive/src/index";

export function processIncentive(world) {
    // Initialize incentive structure from core
    const inc = coreIncentive();

    // Placeholder values from core (future API will populate these)
    const rewards = inc.rewards;
    const penalties = inc.penalties;

    // Engine-level behavior:
    // Later this will include:
    // - reward scoring
    // - penalty routing
    // - population incentive modeling
    // - stability + metabolism integration
    // - synthesis merging

    world.incentive = {
        rewards,
        penalties,
        lastProcessed: Date.now()
    };

    return world;
}
