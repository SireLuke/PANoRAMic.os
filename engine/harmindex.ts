// engine/harmindex.ts

import { WorldState } from "./worldState";

/**
 * HarmIndex Tick Engine
 *
 * Computes global harm based on:
 * - environmental harm
 * - human rights harm
 * - trafficking harm
 * - migration harm
 * - governance harm
 * - supply chain harm
 */

export function applyHarmIndex(world: WorldState): WorldState {
    const env = world.environment?.harm ?? 0;
    const rights = world.humanitarian.humanRights ?? 0;
    const trafficking = world.trafficking.traffickingScore ?? 0;
    const migration = world.migration.migrationScore ?? 0;
    const governance = world.governance.panitarianScore ?? 0;
    const supply = world.economy.taxLoad ?? 0;

    // Total harm score
    const total =
        env +
        rights +
        trafficking +
        migration +
        (1 - governance) +
        supply;

    // Normalize
    const normalized = Math.min(1, total / 100);

    // Risk flags
    const severe = total > 70;
    const moderate = total > 40 && total <= 70;
    const low = total <= 40;

    return {
        ...world,
        harmindex: {
            harmScore: total,
            normalized,
            severe,
            moderate,
            low
        }
    };
}
