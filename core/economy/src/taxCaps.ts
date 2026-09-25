// core/economy/src/taxCaps.ts

export const CATEGORY_CAP = 0.25;      // 25% max per category
export const INFLUENCE_CAP = 0.001;    // 0.1% max influence
export const CORPORATE_CATEGORY_CAP = 0.10; // 10% max per category

export function enforceCategoryCap(amount: number, total: number) {
    const max = total * CATEGORY_CAP;
    return Math.min(amount, max);
}

export function enforceInfluenceCap(amount: number, globalPool: number) {
    const max = globalPool * INFLUENCE_CAP;
    return Math.min(amount, max);
}

export function enforceCorporateCap(amount: number, corporateTotal: number) {
    const max = corporateTotal * CORPORATE_CATEGORY_CAP;
    return Math.min(amount, max);
}
