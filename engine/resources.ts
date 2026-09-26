// engine/resources.ts

import { WorldState } from "./worldState";
import { computeResourceScores } from "../core/resources/src";

export function applyResources(world: WorldState): WorldState {
    const resources = world.resources ?? {
        water: 500,
        food: 500,
        minerals: 500,
        energy: 500,
        renewables: 500
    };

    const scores = computeResourceScores(resources);

    return {
        ...world,
        resources: {
            ...resources,
            ...scores
        }
    };
}
