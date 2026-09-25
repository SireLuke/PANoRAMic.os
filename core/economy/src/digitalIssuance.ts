// core/economy/src/digitalIssuance.ts

import { computeGlobalParCap } from "./globalFloat";

export function canIssuePar(
    currentSupply: number,
    issueAmount: number,
    worldPopulation: number,
    floatMultiplier = 1.35
) {
    const { globalCap } = computeGlobalParCap({
        worldPopulation,
        floatMultiplier
    });

    return currentSupply + issueAmount <= globalCap;
}
