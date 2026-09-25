// core/economy/src/globalFloat.ts

export type GlobalFloatConfig = {
    worldPopulation: number;
    floatMultiplier: number; // default 1.35
};

export function computeGlobalParCap(config: GlobalFloatConfig) {
    const { worldPopulation, floatMultiplier } = config;

    const globalCap = worldPopulation * floatMultiplier;
    const perCapita = globalCap / worldPopulation;

    return {
        globalCap,
        perCapita
    };
}
