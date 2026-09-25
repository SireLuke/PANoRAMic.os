// core/audits/src/score.ts

export function score(impact) {
    // Simple placeholder scoring
    const total =
        impact.environmental +
        impact.humanitarian +
        impact.governance +
        impact.supplyChain;

    return {
        total,
        normalized: total / 100
    };
}
