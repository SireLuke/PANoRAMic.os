// engine/par/parStabilityEngine.ts

export function computeParStability({
  par,
  salaries,
  liquidity,
  velocity,
  markets,
  dashboard,
}: {
  par: any
  salaries: any
  liquidity: number
  velocity: number
  markets: any
  dashboard: any
}) {
  let stabilityScore = 0

  // Liquidity contributes heavily to stability
  stabilityScore += liquidity * 15

  // Velocity contributes moderately
  stabilityScore += velocity * 10

  // Dignity compliance boosts stability
  stabilityScore += salaries.dignityFloor * 0.2

  // Extraction pressure harms stability
  stabilityScore -= markets.extractivePressureIndex * 25

  // Catastrophe probability sharply reduces stability
  stabilityScore -= dashboard.catastropheProbability * 40

  // Immune system activation stabilizes the economy
  if (dashboard.immuneSystemActive) {
    stabilityScore += 20
  }

  // Bound stability score between 0 and 100
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  // Determine stability mode
  let stabilityMode = "stable"

  if (stabilityScore < 30) stabilityMode = "critical"
  else if (stabilityScore < 60) stabilityMode = "unstable"
  else stabilityMode = "stable"

  return {
    stabilityScore,
    stabilityMode,
  }
}
