// panitarian/antiCircularity.ts

export function antiCircularity(amount: number): number {
    // Prevent circular wealth extraction
    return Math.max(0, amount * 0.9);
}
