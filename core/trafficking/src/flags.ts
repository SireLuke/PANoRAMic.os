// core/trafficking/src/flags.ts

export function traffickingFlags(score) {
    return {
        severe: score.total > 70,
        moderate: score.total > 40 && score.total <= 70,
        low: score.total <= 40
    };
}
