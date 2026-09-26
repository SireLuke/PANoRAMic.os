// panitarian/governanceScore.ts

export function governanceScore(
    dignity: number,
    transparency: number,
    stewardship: number
): number {
    return Math.min(1, (dignity + transparency + stewardship) / 3);
}
