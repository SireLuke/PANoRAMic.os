// core/audits/src/panitarian/dynamicRatio.ts

export type BehaviorScores = {
    honestyBonus: number;        // 0–1
    laborBonus: number;          // 0–1
    corruptionPenalty: number;   // 0–1
    stagnationPenalty: number;   // 0–1
    decayPenalty: number;        // 0–1
    fakeActivityPenalty: number; // 0–1
};

export function computeDynamicDebtRatio(scores: BehaviorScores) {
    let ratio = 3;

    ratio -= scores.honestyBonus;
    ratio -= scores.laborBonus;

    ratio += scores.corruptionPenalty;
    ratio += scores.stagnationPenalty;
    ratio += scores.decayPenalty;
    ratio += scores.fakeActivityPenalty;

    if (ratio < 2) ratio = 2;
    if (ratio > 4) ratio = 4;

    return ratio;
}
