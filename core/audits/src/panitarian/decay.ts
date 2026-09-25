// core/audits/src/panitarian/decay.ts

export function computeDecayMonths(inactiveMonths: number) {
    if (inactiveMonths <= 12) return 0;

    const monthsOfDecay = inactiveMonths - 12;

    if (monthsOfDecay <= 12) return monthsOfDecay * 0.5;   // year 1–2: 0.5%/month
    if (monthsOfDecay <= 24) return 12 * 0.5 + (monthsOfDecay - 12) * 1.0; // year 2–3: 1%/month

    return 12 * 0.5 + 12 * 1.0 + (monthsOfDecay - 24) * 2.0; // year 3+: 2%/month
}

export function computeDecayPenalty(inactiveMonths: number) {
    const decayPercent = computeDecayMonths(inactiveMonths);
    return Math.min(decayPercent / 100, 1); // 0–1 penalty
}
