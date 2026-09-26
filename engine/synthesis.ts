// engine/synthesis.ts

import { WorldState } from "./worldState";
import { computeSynthesis } from "../core/synthesis/src";

export function applySynthesis(world: WorldState): WorldState {
    const input = {
        risk: world.catastrophe.impactScore ?? 0,
        resilience: world.stability.dampeningScore ?? 0,
        volatility: world.stability.volatilityScore ?? 0,
        parSupply: world.economy.parSupply ?? 0,
        governance: world.governance.panitarianScore ?? 0,
        humanitarianNeed: world.humanitarian.needScore ?? 0,
        humanitarianRelief: world.humanitarian.reliefScore ?? 0,
        migration: world.migration.migrationScore ?? 0,
        trafficking: world.trafficking.traffickingScore ?? 0,
        harm: world.harmindex.harmScore ?? 0,
        population: world.population.total ?? 0,
        resources: world.resources.resourceScore ?? 0,
        scarcity: world.resources.scarcityScore ?? 0,
        sustainability: world.resources.sustainabilityScore ?? 0,
        knowledge: world.education.qualityScore ?? 0,
        access: world.education.accessScore ?? 0,
        equity: world.education.equityScore ?? 0,
        icc: world.icc.score ?? 0
    };

    const result = computeSynthesis(input);

    return {
        ...world,
        synthesis: {
            coherenceScore: result.coherenceScore,
            vector: result.synthesisVector,
            weights: result.synthesisWeights
        }
    };
}
