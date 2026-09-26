// engine/migration.ts

import { WorldState } from "./worldState";

/**
 * Migration Tick Engine
 *
 * Computes migration pressure, migration flow, and migration score
 * based on population, humanitarian conditions, stability, and economy.
 */

export function applyMigration(world: WorldState): WorldState {
    const population = world.population.total ?? 0;
    const need = world.humanitarian.needScore ?? 0;
    const relief = world.humanitarian.reliefScore ?? 0;
    const stability = world.stability.stabilityScore ?? 0;
    const parSupply = world.economy.parSupply ?? 0;

    // Migration pressure: humanitarian need + economic strain
    const pressure = Math.max(0, need - relief + (population / (parSupply + 1)));

    // Migration flow: pressure dampened by stability
    const flow = Math.max(0, pressure * (1 - stability));

    // Migration score: normalized indicator
    const score = Math.min(1, flow / (population + 1));

    return {
        ...world,
        migration: {
            migrationPressure: pressure,
            migrationFlow: flow,
            migrationScore: score
        }
    };
}
