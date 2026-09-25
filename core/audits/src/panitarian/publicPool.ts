// core/audits/src/panitarian/publicPool.ts

export function computePublicPoolReversion(decayPercent: number, accountValue: number) {
    const reverted = accountValue * decayPercent;
    const remaining = accountValue - reverted;

    return {
        reverted,
        remaining
    };
}
