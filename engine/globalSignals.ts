// engine/globalSignals.ts

import { WorldState } from "./worldState";

export type GlobalSignals = {
    risk: number;
    resilience: number;
    volatility: number;
    energy: number;
    renewables: number;
    parSupply: number;
    parCap: number;
    stewardship: number;
    humanitarianPool: number;
    taxLoad: number;
    knowledge: number;
    access: number;
    equity: number;
    quality: number;
    governance: number;
    humanitarianNeed: number;
    humanitarianRelief: number;
    migration: number;
    trafficking: number;
    harm: number;
    coherence: number;
    icc: number;
};

export function aggregateSignals(world: WorldState): GlobalSignals {
    return {
        risk: world.catastrophe.impactScore ?? 0,
        resilience: world.stability.dampeningScore ?? 0,
        volatility: world.stability.volatilityScore ?? 0,
        energy: world.metabolism.parPool ?? 0,
        renewables: world.metabolism.renewables ?? 0,
        parSupply: world.economy.parSupply ?? 0,
        parCap: world.economy.parCap ?? 0,
        stewardship: world.economy.stewardshipFund ?? 0,
        humanitarianPool: world.economy.humanitarianPool ?? 0,
        taxLoad: world.economy.taxLoad ?? 0,
        knowledge: world.education.qualityScore ?? 0,
        access: world.education.accessScore ?? 0,
        equity: world.education.equityScore ?? 0,
        quality: world.education.qualityScore ?? 0,
        governance: world.governance.panitarianScore ?? 0,
        humanitarianNeed: world.humanitarian.needScore ?? 0,
        humanitarianRelief: world.humanitarian.reliefScore ?? 0,
        migration: world.migration.migrationScore ?? 0,
        trafficking: world.trafficking.traffickingScore ?? 0,
        harm: world.harmindex.harmScore ?? 0,
        coherence: world.synthesis.weights ?? 0,
        icc: world.icc.score ?? 0
    };
}

