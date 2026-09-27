// engine/par/parSynthesisEngine.ts

export function computeParSynthesis({
  par,
  ecology,
  infrastructure,
  markets,
  nodes,
  microAi,
  workforceRotation,
  salaries,
  liquidity,
  velocity,
  stability,
  modes,
}: {
  par: any
  ecology: any
  infrastructure: any
  markets: any
  nodes: any[]
  microAi: any
  workforceRotation: any
  salaries: any
  liquidity: number
  velocity: number
  stability: any
  modes: any
}) {
  // Ecology contribution
  const ecologyImpact =
    ecology.regenerationIndex * 0.4 -
    ecology.degradationIndex * 0.3

  // Infrastructure contribution
  const infrastructureImpact =
    infrastructure.resilienceIndex * 0.4 -
    infrastructure.failureIndex * 0.3

  // Market contribution
  const marketImpact =
    markets.stabilityIndex * 0.4 +
    markets.cooperativeMarketShare * 0.3 -
    markets.extractivePressureIndex * 0.5

  // Node contribution
  const nodeImpact =
    nodes.reduce(
      (sum, n) =>
        sum +
        n.nodeHealthIndex * 0.3 +
        n.nodeConnectivityIndex * 0.2 +
        n.nodeAiPresenceIndex * 0.2,
      0
    ) / Math.max(nodes.length, 1)

  // Micro-AI contribution
  const microAiImpact =
    microAi.microAiCoverageIndex * 0.4 +
    microAi.retrievalQualityIndex * 0.3 +
    microAi.nodeIntelligenceIndex * 0.3

  // Workforce rotation contribution
  const workforceImpact =
    workforceRotation.skillGainRate * 0.4 +
    workforceRotation.rotationIndex * 0.3

  // PAR internal metrics
  const parInternalImpact =
    liquidity * 0.3 +
    velocity * 0.3 +
    stability.stabilityScore * 0.4

  // Dignity contribution
  const dignityImpact =
    salaries.dignityFloor * 0.2 +
    salaries.stewardshipSalary * 0.1 +
    salaries.contributionSalary * 0.1

  // Mode contribution
  const modeImpact =
    modes.stabilityIndex * 0.4 +
    modes.responsivenessIndex * 0.3

  // Combine all impacts
  let synthesisScore =
    ecologyImpact +
    infrastructureImpact +
    marketImpact +
    nodeImpact +
    microAiImpact +
    workforceImpact +
    parInternalImpact +
    dignityImpact +
    modeImpact

  // Normalize to 0–100
  synthesisScore = Math.max(0, Math.min(synthesisScore, 100))

  return {
    synthesisScore,
    synthesisMode:
      synthesisScore < 30
        ? "critical"
        : synthesisScore < 60
        ? "unstable"
        : "stable",
  }
}
