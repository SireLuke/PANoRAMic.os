// engine/par/parForecastEngine.ts

export function computeParForecast({
  liquidity,
  velocity,
  markets,
  ecology,
  infrastructure,
  nodes,
  microAi,
  salaries,
  dashboard,
}: {
  liquidity: number
  velocity: number
  markets: any
  ecology: any
  infrastructure: any
  nodes: any[]
  microAi: any
  salaries: any
  dashboard: any
}) {
  // Trend calculations
  const liquidityTrend = liquidity > 1.5 ? 1 : liquidity < 0.7 ? -1 : 0
  const velocityTrend = velocity > 1.2 ? 1 : velocity < 0.6 ? -1 : 0
  const extractionTrend =
    markets.extractivePressureIndex > 0.6 ? -1 : markets.extractivePressureIndex < 0.3 ? 1 : 0

  const ecologyTrend =
    ecology.regenerationIndex > ecology.degradationIndex ? 1 : -1

  const infrastructureTrend =
    infrastructure.resilienceIndex > infrastructure.failureIndex ? 1 : -1

  const nodeTrend =
    nodes.reduce((sum, n) => sum + n.nodeHealthIndex, 0) / Math.max(nodes.length, 1) > 0.5
      ? 1
      : -1

  const microAiTrend =
    microAi.microAiCoverageIndex > 0.5 &&
    microAi.retrievalQualityIndex > 0.5
      ? 1
      : -1

  const dignityTrend =
    salaries.dignityFloor > 60 ? 1 : salaries.dignityFloor < 50 ? -1 : 0

  const planetaryRiskTrend =
    dashboard.catastropheProbability > 0.3 ? -1 : 1

  // Combine trends into a forecast score
  let forecastScore =
    liquidityTrend * 10 +
    velocityTrend * 10 +
    extractionTrend * 15 +
    ecologyTrend * 15 +
    infrastructureTrend * 15 +
    nodeTrend * 10 +
    microAiTrend * 10 +
    dignityTrend * 10 +
    planetaryRiskTrend * 20

  // Normalize to 0–100
  forecastScore = Math.max(0, Math.min(forecastScore + 50, 100))

  let forecastMode = "positive"
  if (forecastScore < 30) forecastMode = "negative"
  else if (forecastScore < 60) forecastMode = "neutral"

  return {
    forecastScore,
    forecastMode,
    trends: {
      liquidityTrend,
      velocityTrend,
      extractionTrend,
      ecologyTrend,
      infrastructureTrend,
      nodeTrend,
      microAiTrend,
      dignityTrend,
      planetaryRiskTrend,
    },
  }
}
