// engine/humanitarian.ts

import { WorldState } from "./worldState";

/**
 * Humanitarian Tick Engine
 *
 * Computes humanitarian need, relief, and human rights harm.
 * Based on:
 * - population
 * - economy
 * - governance
 * - trafficking
 * - migration
 * - stability
 */

export function applyHumanitarian(world: WorldState): WorldState {
    const population = world.population.total ?? 0;
    const parSupply = world.economy.parSupply ?? 0;
    const governance = world.governance.panitarianScore ?? 0;
    const trafficking = world.trafficking.traffickingScore ?? 0;
    const migration = world.migration.migrationScore ?? 0;
    const stability = world.stability.stabilityScore ?? 0;

    // Humanitarian need: population strain + trafficking + migration
    const need =
        (population / (parSupply + 1)) +
        trafficking * 10 +
        migration * 5;

    // Relief: governance + stability + stewardship
    const relief =
        governance * 10 +
        stability * 5 +
        (world.economy.stewardshipFund ?? 0) / 100;

    // Human rights harm: unmet need
    const humanRights = Math.max(0, need - relief);

    return {
        ...world,
        humanitarian: {
            needScore: need,
            reliefScore: relief,
            humanRights
        }
    };
}
