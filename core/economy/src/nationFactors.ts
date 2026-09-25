// core/economy/src/nationFactors.ts

export type NationFactors = {
    corruption: number; // 0–1
    inflation: number;  // 0–1
    scarcity: number;   // 0–1
    humanitarianNeed: number; // 0–1
};

export function computeNationAdjustment(factors: NationFactors) {
    const honestyBoost = 1 - factors.corruption;
    const stabilityBoost = 1 - factors.inflation;
    const scarcityProtection = 1 - factors.scarcity;
    const humanitarianBoost = 1 + factors.humanitarianNeed;

    return honestyBoost * stabilityBoost * scarcityProtection * humanitarianBoost;
}
