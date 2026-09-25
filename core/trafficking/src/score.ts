// core/trafficking/src/score.ts

export function scoreTrafficking(impact) {
    const total =
        impact.forcedLabor +
        impact.sexualExploitation +
        impact.childTrafficking +
        impact.migrationAbuse;

    return {
        total,
        normalized: total / 100
    };
}
