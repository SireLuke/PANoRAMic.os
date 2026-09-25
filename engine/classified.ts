import { WorldState } from "./worldState";
import { classifyDanger, addToClassified } from "../core/classified/src";

export function applyClassified(world: WorldState): WorldState {
    const text = world.education.original ?? "";

    const category = classifyDanger(text);

    if (!category) return world;

    addToClassified({
        id: crypto.randomUUID(),
        category,
        summary: "Dangerous knowledge detected and quarantined.",
        riskLevel: 1,
        timestamp: Date.now()
    });

    return {
        ...world,
        classified: {
            records: [...world.classified.records]
        }
    };
}
