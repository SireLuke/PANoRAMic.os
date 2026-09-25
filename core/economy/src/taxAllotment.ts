// core/economy/src/taxAllotment.ts

import { enforceCategoryCap, enforceInfluenceCap } from "./taxCaps";
import { isMoralCategory, FreedomCategory } from "./freedomAllotment";

export type TaxAllocation = {
    citizenId: string;
    category: string | FreedomCategory;
    amount: number;
};

export function allocateTax(
    allocation: TaxAllocation,
    citizenTotal: number,
    globalPool: number
) {
    let capped = enforceCategoryCap(allocation.amount, citizenTotal);
    capped = enforceInfluenceCap(capped, globalPool);

    if (isMoralCategory(allocation.category as FreedomCategory)) {
        return { ...allocation, amount: capped };
    }

    return { ...allocation, amount: capped };
}
