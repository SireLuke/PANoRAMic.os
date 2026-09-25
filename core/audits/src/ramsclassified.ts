import { WorldState } from "../../../engine/worldState";

export function auditClassified(input: { world: WorldState }) {
    const count = input.world.classified.records.length;

    return {
        ok: count === 0,
        reason: count > 0 ? "Dangerous knowledge quarantined" : null,
        count
    };
}
