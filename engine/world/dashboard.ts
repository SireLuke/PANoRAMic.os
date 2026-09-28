// engine/world/dashboard.ts

import { WorldStatus, computeWorldStatus } from "./worldStatus.ts"
import { WorldReport, generateWorldReport, printWorldReport } from "./worldReporter.ts"
import { GlobalFrame } from "../global/globalLoopIntegration.ts"

export interface DashboardPacket {
  tick: number

  // High-level
  headline: string
  overallHealth: number
  collapseRisk: number
  recoveryStrength: number
  coherence: number

  // Node health
  nodesHealthy: number
  nodesUnstable: number
  nodesCritical: number

  // Subsystem summaries
  subsystem: Record<string, number>

  // Full report
  report: WorldReport

  // Full status
  status: WorldStatus
}

// Convert world frame → dashboard packet
export function buildDashboard(frame: GlobalFrame): DashboardPacket {
  const status = computeWorldStatus(frame)
  const report = generateWorldReport(frame)

  return {
    tick: status.tick,

    headline: report.headline,
    overallHealth: status.overallHealth,
    collapseRisk: status.collapseRisk,
    recoveryStrength: status.recoveryStrength,
    coherence: status.coherence,

    nodesHealthy: status.nodesHealthy,
    nodesUnstable: status.nodesUnstable,
    nodesCritical: status.nodesCritical,

    subsystem: status.subsystem,

    report,
    status,
  }
}

// Pretty-print for CLI or logs
export function printDashboard(packet: DashboardPacket): string {
  return `
=== PANoRAMic.OS Planetary Dashboard — Tick ${packet.tick} ===
${packet.headline}

Overall Health: ${packet.overallHealth.toFixed(3)}
Collapse Risk: ${packet.collapseRisk.toFixed(3)}
Recovery Strength: ${packet.recoveryStrength.toFixed(3)}
Coherence: ${packet.coherence.toFixed(3)}

Nodes Healthy: ${packet.nodesHealthy}
Nodes Unstable: ${packet.nodesUnstable}
Nodes Critical: ${packet.nodesCritical}

Subsystem Summary:
${Object.entries(packet.subsystem)
  .map(([k, v]) => `  ${k}: ${v}`)
  .join("\n")}

----------------------------------------
Full Report:
${printWorldReport(packet.report)}
`
}
