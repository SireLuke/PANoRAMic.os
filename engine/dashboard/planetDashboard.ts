// engine/dashboard/planetDashboard.ts

import { SystemState } from "../../core/SystemState"
import { computeDashboard } from "./dashboardEngine"

export type PlanetDashboardView = {
  globalHealth: number
  globalStability: number
  globalRisk: number
  globalSynthesis: number
  catastropheProbability: number
  immuneSystemActive: boolean
  activeMode: string
  par: {
    cap: number
    mintRate: number
    velocity: number
    dignityFloor: number
    stewardshipSalary: number
  }
  ecology: {
    regen: number
    degradation: number
  }
  infrastructure: {
    resilience: number
    failure: number
  }
  markets: {
    stability: number
    extraction: number
  }
  nodes: number
}

export function buildPlanetDashboard(state: SystemState): PlanetDashboardView {
  const dashboard = computeDashboard(state)

  return {
    globalHealth: dashboard.globalHealth,
    globalStability: dashboard.globalStability,
    globalRisk: dashboard.globalRisk,
    globalSynthesis: dashboard.globalSynthesis,
    catastropheProbability: dashboard.catastropheProbability,
    immuneSystemActive: dashboard.immuneSystemActive,
    activeMode: dashboard.activeMode,
    par: {
      cap: dashboard.par.cap,
      mintRate: dashboard.par.mintRate,
      velocity: dashboard.par.velocity,
      dignityFloor: dashboard.par.dignityFloor,
      stewardshipSalary: dashboard.par.stewardshipSalary,
    },
    ecology: {
      regen: dashboard.ecology.regen,
      degradation: dashboard.ecology.degradation,
    },
    infrastructure: {
      resilience: dashboard.infrastructure.resilience,
      failure: dashboard.infrastructure.failure,
    },
    markets: {
      stability: dashboard.markets.stability,
      extraction: dashboard.markets.extraction,
    },
    nodes: dashboard.nodes,
  }
}
