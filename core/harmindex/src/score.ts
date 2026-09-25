// core/harmindex/src/score.ts

export function scoreHarm(impact) {
    const total =
        impact.environmental +
        impact.humanRights +
        impact.trafficking +
        impact.migration +
        impact.governance +
        impact.supplyChain;

    return {
        total,
        normalized: total / 100
    };
}
