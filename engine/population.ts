// engine/population.ts

import { WorldState } from "./worldState";

/**
 * Population Tick Engine
 *
 * Computes population changes based on:
 * - birth rate
 * - death rate
 * - migration flow
 * - catastrophe impact
 */

export function applyPopulation(world: WorldState): WorldState {
    const total = world.population.total ?? 0;

    const birthRate = world.population.birthRate ?? 0.0176; // placeholder
    const deathRate = world.population.deathRate ?? 0.0077; // placeholder

    const migrationFlow = world.migration.migrationFlow ?? 0;
    const catastropheImpact = world.catastrophe.impactScore ?? 0;

    // Births and deaths per tick
    const births = total * birthRate;
    const deaths = total * deathRate;

    // Catastrophe mortality
    const catastropheLoss = total * (catastropheImpact / 100);

    // Migration effect
    const migrationChange = migrationFlow * 1000;

    const newTotal = Math.max(
        0,
        total + births - deaths - catastropheLoss + migrationChange
    );

    return {
        ...world,
        population: {
            ...world.population,
            total: newTotal,
            births,
            deaths,
            catastropheLoss,
            migrationChange
        }
    };
}
