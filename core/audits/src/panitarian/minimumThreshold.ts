// core/audits/src/panitarian/minimumThreshold.ts

export function meetsMinimumThreshold(amount: number, accountValue: number) {
    const percentThreshold = 0.005; // 0.5% of account value
    const absoluteMinimum = 500;    // 500 PAR (or equivalent)

    const byPercent = amount >= accountValue * percentThreshold;
    const byAbsolute = amount >= absoluteMinimum;

    return byPercent || byAbsolute;
}
