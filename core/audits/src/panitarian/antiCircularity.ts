// core/audits/src/panitarian/antiCircularity.ts

export type Transaction = {
    fromId: string;
    toId: string;
    amount: number;
    timestamp: number; // ms since epoch
};

export function isCircularTransfer(tx: Transaction, history: Transaction[]) {
    const thirtyDaysMs = 30 * 24 * 60 * 60 * 1000;

    return history.some(h =>
        h.fromId === tx.toId &&
        h.toId === tx.fromId &&
        Math.abs(tx.timestamp - h.timestamp) <= thirtyDaysMs
    );
}
