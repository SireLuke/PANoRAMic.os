// engine/par/parShockAbsorptionEngine.ts

export function computeParShockAbsorption({
  par,
  liquidity,
  velocity,
  markets,
  ecology,
  infrastructure,
  dashboard,
}: {
  par: any
  liquidity: number
  velocity: number
  markets: any
  ecology: any
  infrastructure: any
  dashboard: any
}) {
  const interventions: string[] = []

  // Ecological shock
  if (ecology.degradationIndex > ecology.regenerationIndex * 1.5) {
    interventions.push("Ecological shock detected — boosting regeneration and reducing degradation.")
    ecology.regenerationIndex *= 1.1
    ecology.degradationIndex *= 0.9
  }

  // Infrastructure shock
  if (infrastructure.failureIndex > infrastructure.resilienceIndex * 1.5) {
    interventions.push("Infrastructure shock detected — boosting resilience and reducing failure.")
    infrastructure.resilienceIndex *= 1.1
    infrastructure.failureIndex *= 0.9
  }

  // Market extraction shock
  if (markets.extractivePressureIndex > 0.8) {
    interventions.push("Extraction shock detected — dampening extraction pressure.")
    markets.extractivePressureIndex *= 0.85
  }

  // Liquidity shock
  if (liquidity < 0.5) {
    interventions.push("Liquidity shock detected — boosting liquidity.")
    par.parMintRate *= 1.1
    liquidity *= 1.2
  }

  // Velocity shock
  if (velocity < 0.5) {
    interventions.push("Velocity shock detected — boosting velocity.")
    velocity *= 1.2
  }

  // Planetary catastrophe shock
  if (dashboard.catastropheProbability > 0.4) {
    interventions.push("Catastrophe shock detected — activating emergency dampening.")
    par.parMintRate *= 0.8
    markets.extractivePressureIndex *= 0.8
    ecology.degradationIndex *= 0.9
    infrastructure.failureIndex *= 0.9
  }

  return {
    interventions,
    updated: {
      par,
      liquidity,
      velocity,
      markets,
      ecology,
      infrastructure,
    },
  }
}
