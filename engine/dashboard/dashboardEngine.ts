// engine/dashboard/dashboardEngine.ts

import { SystemState } from "../../core/SystemState"

export function computeDashboard(state: SystemState) {
  // Global health (ecology + infrastructure + population)
  const globalHealth =
    state.ecology.regenerationIndex * 0.4 +
    state.infrastructure.resilienceIndex * 0.4 +
    state.population.populationHealthIndex * 0.2

  // Global stability (markets + modes + par)
  const globalStability =
    state.markets.stabilityIndex * 0.4 +
    state.modes.stabilityIndex * 0.3 +
    (state.par.parCapCompliance ? 1 : 0) * 0.3

  // Global risk (ecology degradation + infrastructure failure + market extraction)
  const globalRisk =
    state.ecology.degradationIndex * 0.4 +
    state.infrastructure.failureIndex * 0.3 +
    state.markets.extractivePressureIndex * 0.3

  // Global synthesis (how well systems cooperate)
  const globalSynthesis =
    state.microAi.microAiCoverageIndex * 0.3 +
    state.workforceRotation.skillGainRate * 0.3 +
    state.nodes.reduce((sum, n) => sum + n.nodeConnectivityIndex, 0) /
      Math.max(state.nodes.length, 1) *
      0.4

  // Catastrophe probability (immune system trigger)
  const catastropheProbability =
    globalRisk * 0.6 +
    (1 - globalStability) * 0.4

  // Immune system activation
  const immuneSystemActive = catastropheProbability > 0.7

  return {
    globalHealth,
    globalStability,
    globalRisk,
    globalSynthesis,
    catastropheProbability,
    immuneSystemActive,
    activeMode: state.modes.activeMode,
    par: {
      cap: state.par.parCap,
      mintRate: state.par.parMintRate,
      velocity: state.par.parVelocity,
      dignityFloor: state.par.dignityFloor,
      stewardshipSalary: state.par.stewardshipSalary,
    },
    ecology: {
      regen: state.ecology.regenerationIndex,
      degradation: state.ecology.degradationIndex,
    },
    infrastructure: {
      resilience: state.infrastructure.resilienceIndex,
      failure: state.infrastructure.failureIndex,
    },
    markets: {
      stability: state.markets.stabilityIndex,
      extraction: state.markets.extractivePressureIndex,
    },
    nodes: state.nodes.length,
  }
}
