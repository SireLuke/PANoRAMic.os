import { SynthesisInput } from "./types";

export function computeSynthesis(input: SynthesisInput) {
    const {
        risk,
        resilience,
        volatility,
        parSupply,
        governance,
        humanitarianNeed,
        humanitarianRelief,
        migration,
        trafficking,
        harm,
        population,
        resources,
        scarcity,
        sustainability,
        knowledge,
        access,
        equity,
        icc
    } = input;

    const stabilityFactor = resilience - volatility;
    const humanitarianFactor = humanitarianRelief - humanitarianNeed;
    const governanceFactor = governance - harm;
    const resourceFactor = resources + sustainability - scarcity;
    const educationFactor = (knowledge + access + equity) / 3;
    const migrationFactor = migration + trafficking;
    const iccFactor = icc;

    const raw =
        stabilityFactor +
        humanitarianFactor +
        governanceFactor +
        resourceFactor +
        educationFactor -
        migrationFactor +
        iccFactor +
        parSupply / (population + 1);

    const coherenceScore = Math.max(0, Math.min(1, raw / 100));

    const synthesisVector = {
        stabilityFactor,
        humanitarianFactor,
        governanceFactor,
        resourceFactor,
        educationFactor,
        migrationFactor,
        iccFactor,
        parSupply,
        population
    };

    const synthesisWeights = {
        stability: 0.15,
        humanitarian: 0.15,
        governance: 0.15,
        resources: 0.15,
        education: 0.15,
        migration: 0.10,
        icc: 0.15
    };

    return {
        coherenceScore,
        synthesisVector,
        synthesisWeights
    };
}
