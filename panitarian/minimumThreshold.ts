// panitarian/minimumThreshold.ts

export function minimumThreshold(population: number): number {
    return Math.max(1, population * 0.01);
}
