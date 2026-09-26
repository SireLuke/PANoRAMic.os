// panitarian/transactionFlow.ts

export function transactionFlow(amount: number): number {
    return Math.max(0, amount * 0.95);
}
