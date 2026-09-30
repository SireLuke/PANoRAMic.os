// core/data/stateDiff.ts

/**
 * World State Diff Engine:
 * Compares two snapshots and produces a change packet.
 */

export type StateDiff = {
  timestamp: number
  globalChanges: Record<string, number>
  pillarChanges: Record<string, number>
  nodeChanges: {
    totalNodesDelta: number
    averageHealthDelta: number
  }
  newAlerts: any[]
  resolvedAlerts: any[]
  forecastDelta: Record<string, number>
}

export function computeDiff(prev: any, next: any): StateDiff {
  const timestamp = Date.now()

  const globalChanges: Record<string, number> = {}
  for (const key in next.globalSignals) {
    const oldVal = prev.globalSignals[key] ?? 0
    const newVal = next.globalSignals[key] ?? 0
    globalChanges[key] = newVal - oldVal
  }

  const pillarChanges: Record<string, number> = {}
  for (const key in next.pillarHealth) {
    const oldVal = prev.pillarHealth[key] ?? 0
    const newVal = next.pillarHealth[key] ?? 0
    pillarChanges[key] = newVal - oldVal
  }

  const nodeChanges = {
    totalNodesDelta: next.nodeSummary.totalNodes - prev.nodeSummary.totalNodes,
    averageHealthDelta: next.nodeSummary.averageHealth - prev.nodeSummary.averageHealth
  }

  const prevAlerts = new Set(prev.activeAlerts.map((a: any) => a.id))
  const nextAlerts = new Set(next.activeAlerts.map((a: any) => a.id))

  const newAlerts = next.activeAlerts.filter((a: any) => !prevAlerts.has(a.id))
  const resolvedAlerts = prev.activeAlerts.filter((a: any) => !nextAlerts.has(a.id))

  const forecastDelta: Record<string, number> = {}
  const prevForecast = prev.forecast[prev.forecast.length - 1] || {}
  const nextForecast = next.forecast[next.forecast.length - 1] || {}

  for (const key in nextForecast) {
    const oldVal = prevForecast[key] ?? 0
    const newVal = nextForecast[key] ?? 0
    forecastDelta[key] = newVal - oldVal
  }

  return {
    timestamp,
    globalChanges,
    pillarChanges,
    nodeChanges,
    newAlerts,
    resolvedAlerts,
    forecastDelta
  }
}