// engine/par/parIntegrityEngine.ts

export function computeParIntegrity({
  par,
  salaries,
  liquidity,
  velocity,
  markets,
  ecology,
  infrastructure,
}: {
  par: any
  salaries: any
  liquidity: number
  velocity: number
  markets: any
  ecology: any
  infrastructure: any
}) {
  const issues: string[] = []

  // Mint rate must not exceed cap
  if (par.parMintRate > par.parCap) {
    issues.push("Mint rate exceeds PAR Cap — integrity violation.")
  }

  // Dignity floor must be respected
  if (salaries.dignityFloor < 50) {
    issues.push("Dignity floor below minimum threshold.")
  }

  // Liquidity must match velocity direction
  if (velocity > 1.5 && liquidity < 1.0) {
    issues.push("High velocity but low liquidity — inconsistent flow.")
  }

  if (velocity < 0.5 && liquidity > 2.0) {
    issues.push("Low velocity but high liquidity — inconsistent flow.")
  }

  // Extraction pressure must match market stability
  if (markets.extractivePressureIndex > 0.7 && markets.stabilityIndex > 0.7) {
    issues.push("High extraction pressure but high stability — contradiction.")
  }

  // Ecology degradation must not exceed regeneration too far
  if (ecology.degradationIndex > ecology.regenerationIndex * 2) {
    issues.push("Ecology degrading far faster than regenerating — integrity risk.")
  }

  // Infrastructure failure must not exceed resilience too far
  if (infrastructure.failureIndex > infrastructure.resilienceIndex * 2) {
    issues.push("Infrastructure failing far faster than resilient — integrity risk.")
  }

  // Integrity score (0–100)
  let integrityScore = 100 - issues.length * 10
  integrityScore = Math.max(0, integrityScore)

  let integrityMode = "stable"
  if (integrityScore < 40) integrityMode = "critical"
  else if (integrityScore < 70) integrityMode = "unstable"

  return {
    integrityScore,
    integrityMode,
    issues,
  }
}
