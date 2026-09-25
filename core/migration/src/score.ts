// core/migration/src/score.ts

export function scoreMigration(impact) {
    const total =
        impact.displaced +
        impact.refugees +
        impact.asylumSeekers +
        impact.conflictDriven;

    return {
        total,
        normalized: total / 100
    };
}
