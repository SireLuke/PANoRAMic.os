// engine/par/parImmuneEngine.ts

export function computeParImmuneResponse({
  par,
  salaries,
  liquidity,
  velocity,
  markets,
  ecology,
  infrastructure,
  risk,
  integrity,
  synthesis,
  dashboard,
}: {
  par: any
  salaries: any
  liquidity: number
  velocity: number
  markets: any
  ecology: any
  infrastructure: any
  risk: any
  integrity: any
  synthesis: any
  dashboard: any
}) {
  const immuneActions: string[] = []
  let immuneActive = false

  // Trigger conditions
  const triggers = {
    dignityCollapse: salaries.dignityFloor < 50,
    liquidityCollapse: liquidity < 0.5,
    velocityCollapse: velocity < 0.5,
    extractionSpike: markets.extractivePressureIndex > 0.75,
    ecologicalCollapse: ecology.degradationIndex > ecology.regenerationIndex * 1.5,
    infrastructureCollapse: infrastructure.failureIndex > infrastructure.resilienceIndex * 1.5,
    riskCritical: risk.totalRisk >= 70,
    integrityCritical: integrity.integrityScore < 40,
    synthesisCritical: synthesis.synthesisScore < 30,
    catastropheRisk: dashboard.catastropheProbability > 0.35,
  }

  // If ANY trigger is true → immune system activates
  immuneActive = Object.values(triggers).some(v => v === true)

  if (!immuneActive) {
    return {
      immuneActive: false,
      immuneActions: [],
      updated: {
        par,
        salaries,
        liquidity,
        velocity,
        markets,
        ecology,
        infrastructure,
      },
    }
  }

  // Immune system actions
  if (triggers.dignityCollapse) {
    immuneActions.push("Dignity collapse detected — raising dignity floor.")
    salaries.dignityFloor += 10
  }

  if (triggers.liquidityCollapse) {
    immuneActions.push("Liquidity collapse detected — boosting mint rate and liquidity.")
    par.parMintRate *= 1.15
    liquidity *= 1.25
  }

  if (triggers.velocityCollapse) {
    immuneActions.push("Velocity collapse detected — boosting velocity.")
    velocity *= 1.2
  }

  if (triggers.extractionSpike) {
    immuneActions.push("Extraction spike detected — dampening extraction pressure.")
    markets.extractivePressureIndex *= 0.8
  }

  if (triggers.ecologicalCollapse) {
    immuneActions.push("Ecological collapse detected — boosting regeneration and reducing degradation.")
    ecology.regenerationIndex *= 1.15
    ecology.degradationIndex *= 0.9
  }

  if (triggers.infrastructureCollapse) {
    immuneActions.push("Infrastructure collapse detected — boosting resilience and reducing failure.")
    infrastructure.resilienceIndex *= 1.15
    infrastructure.failureIndex *= 0.9
  }

  if (triggers.riskCritical) {
    immuneActions.push("Critical risk detected — activating emergency dampening.")
    par.parMintRate *= 0.85
    markets.extractivePressureIndex *= 0.85
  }

  if (triggers.integrityCritical) {
    immuneActions.push("Integrity failure detected — correcting inconsistencies.")
    par.parMintRate = Math.min(par.parMintRate, par.parCap)
    if (salaries.dignityFloor < 50) salaries.dignityFloor = 50
  }

  if (triggers.synthesisCritical) {
    immuneActions.push("Synthesis collapse detected — boosting all positive subsystems.")
    ecology.regenerationIndex *= 1.1
    infrastructure.resilienceIndex *= 1.1
    liquidity *= 1.1
    velocity *= 1.1
  }

  if (triggers.catastropheRisk) {
    immuneActions.push("Catastrophe probability high — activating global dampening.")
    par.parMintRate *= 0.8
    markets.extractivePressureIndex *= 0.8
    ecology.degradationIndex *= 0.9
    infrastructure.failureIndex *= 0.9
  }

  return {
    immuneActive,
    immuneActions,
    updated: {
      par,
      salaries,
      liquidity,
      velocity,
      markets,
      ecology,
      infrastructure,
    },
  }
}
