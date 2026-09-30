// core/data/stateSnapshot.ts

/**
 * World State Snapshot Engine:
 * Produces a unified, human-readable snapshot of the entire world model.
 */

export type WorldSnapshot = {
  timestamp: number
  globalSignals: Record<string, number>
  pillarHealth: Record<string, number>
  activeAlerts: any[]
  forecast: any[]
  nodeSummary: {
    totalNodes: number
    averageHealth: number
  }
}

export function generateSnapshot(world: any, alerts: any[], forecast: any[]): WorldSnapshot {
  const timestamp = Date.now()

  // Pillar health summary
  const pillarHealth: Record<string, number> = {}
  for (const pillarName in world.pillars) {
    const pillar = world.pillars[pillarName]
    const values = Object.values(pillar)
    const avg = values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0
    pillarHealth[pillarName] = avg
  }

  // Node summary
  const nodes = world.nodes || []
  const nodeValues = nodes.map((n: any) => n.health ?? 0)
  const averageHealth = nodeValues.length
    ? nodeValues.reduce((a, b) => a + b, 0) / nodeValues.length
    : 0

  return {
    timestamp,
    globalSignals: world.globalSignals,
    pillarHealth,
    activeAlerts: alerts,
    forecast,
    nodeSummary: {
      totalNodes: nodes.length,
      averageHealth
    }
  }
}