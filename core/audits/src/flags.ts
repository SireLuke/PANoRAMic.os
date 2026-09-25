// core/audits/src/flags.ts

export function flags(score) {
    return {
        highRisk: score.total > 70,
        mediumRisk: score.total > 40 && score.total <= 70,
        lowRisk: score.total <= 40
    };
}
