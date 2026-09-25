// core/audits/src/ramsDynamicFloat.ts

import { computeDynamicParCap } from "../../economy/src/dynamicFloat";

export type RamsFloatAuditInput = {
    worldPopulation: number;
    resourceParValue: number;
    floatMultiplier: number;     // 1.35
    resourceMultiplier: number;  // 0.90
    totalParSupply: number;
};

export function auditDynamicFloat(input: RamsFloatAuditInput) {
    const {
        worldPopulation,
        resourceParValue,
        floatMultiplier,
        resourceMultiplier,
        totalParSupply
    } = input;

    const { globalCap, populationCap, resourceCap } = computeDynamicParCap({
        worldPopulation,
        floatMultiplier,
        resourceParValue,
        resourceMultiplier
    });

    const withinCap = totalParSupply <= globalCap;

    return {
        withinCap,
        globalCap,
        populationCap,
        resourceCap,
        totalParSupply,
        violation: withinCap ? null : "Total PAR supply exceeds dynamic global cap"
    };
}
