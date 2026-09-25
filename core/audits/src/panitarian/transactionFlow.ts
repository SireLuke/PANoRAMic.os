// core/audits/src/panitarian/transactionFlow.ts

import { Transaction } from "./antiCircularity";

export function computeStagnationPenalty(history: Transaction[]) {
    if (!history.length) return 1; // fully stagnant

    const last = history[history.length - 1];
    const now = Date.now();

    const monthsInactive =
        (now - last.timestamp) / (1000 * 60 * 60 * 24 * 30);

    if (monthsInactive < 3) return 0;
    if (monthsInactive < 6) return 0.25;
    if (monthsInactive < 12) return 0.5;

    return 1; // fully stagnant
}
