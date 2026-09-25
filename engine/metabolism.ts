// engine/metabolism.ts

import { metabolism as coreMetabolism } from "../core/metabolism/src/index";

export function processMetabolism(world) {
    // Initialize metabolism structure from core
    const meta = coreMetabolism();

    // Placeholder values from core (future API will populate these)
    const intake = meta.intake;
    const output = meta.output;

    // Engine-level behavior:
    // Later this will include:
    // - resource intake calculations
    // - renewable resource routing
    // - population metabolism modeling
    // - stability + incentive integration
    // - synthesis merging

    world.metabolism = {
        intake,
        output,
        lastProcessed: Date.now()
    };

    return world;
}
