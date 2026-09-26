// engine/trafficking.ts

import { WorldState } from "./worldState";

/**
 * Trafficking Tick Engine
 *
 * Computes trafficking pressure, trafficking flow, and trafficking score
 * based on humanitarian need, migration, and governance.
 */

export function applyTrafficking(world: WorldState): WorldState {
    const need = world.humanitarian.needScore ?? 0;
    const relief = world.humanitarian.reliefScore ?? 0;
    const migrationScore = world.migration.migrationScore ?? 0;
    const governanceScore = world.governance.panitarianScore ?? 0;

    // Trafficking pressure: unmet need + migration vulnerability
    const pressure = Math.max(0, (need - relief) + migrationScore);

    // Trafficking flow: pressure reduced by governance
    const flow = Math.max(0, pressure * (1 - governanceScore));

    // Trafficking score: normalized indicator
    const score = Math.min(1, flow);

    return {
        ...world,
        trafficking: {
            traffickingPressure: pressure,
            traffickingFlow: flow,
            traffickingScore: score
        }
    };
}

