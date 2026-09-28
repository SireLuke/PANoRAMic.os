// engine/world/worldReporter.ts

import { WorldState } from "./worldState.ts"
import { GlobalFrame } from "../global/globalLoopIntegration.ts"

export interface WorldReport {
  tick: number
  headline: string
  stability: number
  risk: number
  collapsePressure: number
  resilience: number
  recovery: number
  flow: number
  synthesis: number
  population: any
  resources: any
  governance: any
  ecology: any
  economy: any
  humanitarian: any
  infrastructure: any
  migration: any
  trafficking: any
  harmindex: any
  icc: any
  coherence: number
}

export function generateWorldReport(frame: GlobalFrame): WorldReport {
  const { world, signals, tick } = frame

  const headline =
    signals.collapsePressure > 0.7
      ? "⚠ Planet Under High Collapse Pressure"
      : signals.recovery > 0.6
      ? "🌱 Planetary Recovery Surge Detected"
      : signals.stability > 0.6
      ? "🌍 Planetary Stability Holding"
      : "📊 Planetary Status Update"

  return {
    tick,
    headline,

    stability: signals.stability,
    risk: signals.risk,
    collapsePressure: signals.collapsePressure,
    resilience: signals.resilience,
    recovery: signals.recovery,
    flow: signals.flow,
    synthesis: signals.synthesis,

    population: world.population,
    resources: world.resources,
    governance: world.governance,
    ecology: world.ecology,
    economy: world.economy,
    humanitarian: world.humanitarian,
    infrastructure: world.infrastructure,
    migration: world.migration,
    trafficking: world.trafficking,
    harmindex: world.harmindex,
    icc: world.icc,

    coherence: signals.coherence,
  }
}

// Pretty-print for dashboards or CLI
export function printWorldReport(report: WorldReport): string {
  return `
=== PANoRAMic.OS Planetary Report — Tick ${report.tick} ===
${report.headline}

Stability: ${report.stability.toFixed(3)}
Risk: ${report.risk.toFixed(3)}
Collapse Pressure: ${report.collapsePressure.toFixed(3)}
Resilience: ${report.resilience.toFixed(3)}
Recovery: ${report.recovery.toFixed(3)}
Flow: ${report.flow.toFixed(3)}
Synthesis: ${report.synthesis.toFixed(3)}
Coherence: ${report.coherence.toFixed(3)}

Population: ${JSON.stringify(report.population)}
Resources: ${JSON.stringify(report.resources)}
Governance: ${JSON.stringify(report.governance)}
Ecology: ${JSON.stringify(report.ecology)}
Economy: ${JSON.stringify(report.economy)}
Humanitarian: ${JSON.stringify(report.humanitarian)}
Infrastructure: ${JSON.stringify(report.infrastructure)}
Migration: ${JSON.stringify(report.migration)}
Trafficking: ${JSON.stringify(report.trafficking)}
Harm Index: ${JSON.stringify(report.harmindex)}
ICC: ${JSON.stringify(report.icc)}
`
}
