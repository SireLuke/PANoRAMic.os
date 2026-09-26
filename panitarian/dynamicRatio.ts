// panitarian/dynamicRatio.ts

export function dynamicRatio(governanceScore: number): number {
    return Math.min(1, Math.max(0, governanceScore * 0.75));
}
