// engine/par/parRiskEngine.ts

export function computeParRisk({
  liquidity,
  velocity,
  salaries,
  markets,
  ecology,
  infrastructure,
  nodes,
  microAi,
  dashboard,
}: {
  liquidity: number
  velocity: number
  salaries: any
  markets: any
  ecology: any
  infrastructure: any
  nodes: any[]
  microAi: any
  dashboard: any
}) {
  // Liquidity risk: low liquidity = high risk
  const liquidityRisk = liquidity < 0.5 ? (1 - liquidity) * 40 : 0

  // Velocity risk: too slow or too fast = instability
  const velocityRisk =
    velocity < 0.5 ? (1 - velocity) * 30 : velocity > 1.5 ? (velocity - 1.5) * 20 : 0

  // Dignity risk: dignity floor violations
  const dignityRisk = salaries.dignityFloor < 50 ? 30 : 0

  // Market extraction risk
  const extractionRisk = markets.extractivePressureIndex * 50

  // Ecological risk
  const ecologyRisk =
    ecology.degradationIndex > ecology.regenerationIndex
      ? (ecology.degradationIndex - ecology.regenerationIndex) * 40
      : 0

  // Infrastructure risk
  const infrastructureRisk =
    infrastructure.failureIndex > 0.4
      ? (infrastructure.failureIndex - 0.4) * 40
      : 0

  // Node network risk
  const nodeRisk =
    nodes.length === 0
      ? 20
      : nodes.reduce(
          (sum, n) =>
            sum +
            (1 - n.nodeHealthIndex) * 10 +
            (1 - n.nodeConnectivityIndex) * 10,
          0
        ) / nodes.length

  // Micro-AI risk
  const microAiRisk =
    (1 - microAi.microAiCoverageIndex) * 20 +
    (1 - microAi.retrievalQualityIndex) * 20

  // Planetary risk (catastrophe probability)
  const planetaryRisk = dashboard.catastropheProbability * 100

  // Combine all risks
  let totalRisk =
    liquidityRisk +
    velocityRisk +
    dignityRisk +
    extractionRisk +
    ecologyRisk +
    infrastructureRisk +
    nodeRisk +
    microAiRisk +
    planetaryRisk

  // Normalize to 0–100
  totalRisk = Math.max(0, Math.min(totalRisk, 100))

  // Risk mode
  let riskMode = "low"
  if (totalRisk >= 70) riskMode = "critical"
  else if (totalRisk >= 40) riskMode = "high"
  else if (totalRisk >= 20) riskMode = "moderate"

  return {
    totalRisk,
    riskMode,
    breakdown: {
      liquidityRisk,
      velocityRisk,
      dignityRisk,
      extractionRisk,
      ecologyRisk,
      infrastructureRisk,
      nodeRisk,
      microAiRisk,
      planetaryRisk,
    },
  }
}
