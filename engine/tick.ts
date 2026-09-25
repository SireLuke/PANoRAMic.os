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

}import { reduceWorld } from "./worldReducer";

export function tick(world: WorldState): WorldState {
    const updated = reduceWorld(world);

    return {
        ...updated,
        time: updated.time + 1
    };
}import { aggregateSignals } from "./globalSignals";

export function tick(world: WorldState): WorldState {
    const updated = reduceWorld(world);
    const signals = aggregateSignals(updated);

    return {
        ...updated,
        time: updated.time + 1,
        globalSignals: signals
    };
}


