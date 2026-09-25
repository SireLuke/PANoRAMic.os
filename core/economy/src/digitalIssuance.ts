// core/economy/src/digitalIssuance.ts

import { computeDynamicParCap } from "./dynamicFloat";

export function canIssueParDynamic(
    currentSupply: number,
    issueAmount: number,
    worldPopulation: number,
    resourceParValue: number,
    floatMultiplier = 1.35,
    resourceMultiplier = 0.90
) {
    const { globalCap } = computeDynamicParCap({
        worldPopulation,
        floatMultiplier,
        resourceParValue,
        resourceMultiplier
    });

    return currentSupply + issueAmount <= globalCap;
}
