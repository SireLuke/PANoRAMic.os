// Pulls in the core/events structure
import { events as coreEvents } from "../core/events/src/index";

export function processEvents(world) {
    // Initialize event structure from core
    const evt = coreEvents();

    // Placeholder: future API will populate evt.feed + evt.categories
    const feed = evt.feed;
    const categories = evt.categories;

    // Engine-level behavior:
    // For now, we simply attach the event structure to the world state.
    // Later, this will include:
    // - event scoring
    // - category routing
    // - volatility triggers
    // - catastrophe escalation
    // - stability impacts
    // - synthesis merging

    world.events = {
        feed,
        categories,
        lastProcessed: Date.now()
    };

    return world;
}
