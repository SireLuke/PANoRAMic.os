// engine/tick.ts
export function tick(world) {
    // placeholder tick cycle
    return {
        ...world,
        ticked: true
    };import { WorldState } from "./worldState";

export function tick(world: WorldState): WorldState {
    const next: WorldState = {
        ...world,
        time: world.time + 1
    };

    // later: call catastrophe, dampening, metabolism, stability, synthesis, etc.
    // e.g. next = applyMetabolism(next);
    //      next = applyStability(next);
    //      next = applySynthesis(next);

    return next;
}

}
