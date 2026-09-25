// core/economy/src/dynamicFloat.ts

export type DynamicFloatConfig = {
    worldPopulation: number;   // P
    floatMultiplier: number;   // F = 1.35
    resourceParValue: number;  // R (real asset value)
    resourceMultiplier: number; // S = 0.90
};

export function computeDynamicParCap(config: DynamicFloatConfig) {
    const {
        worldPopulation,
        floatMultiplier,
        resourceParValue,
        resourceMultiplier
    } = config;

    const populationCap = worldPopulation * floatMultiplier;
    const resourceCap = resourceParValue * resourceMultiplier;

    const globalCap = Math.min(populationCap, resourceCap);

    return {
        globalCap,
        populationCap,
        resourceCap
    };
}
