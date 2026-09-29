// core/data/history.ts

/**
 * Historical Data Store:
 * Keeps a rolling history of incoming datasets for consistency checks.
 */

export class HistoryStore {
  private history: any[] = []
  private maxSize: number

  constructor(maxSize: number = 100) {
    this.maxSize = maxSize
  }

  add(data: any) {
    this.history.push(data)
    if (this.history.length > this.maxSize) {
      this.history.shift()
    }
  }

  getAll() {
    return this.history
  }

  getLast() {
    return this.history[this.history.length - 1]
  }
}

/**
 * Compare incoming data with historical patterns.
 * Returns a consistency score between 0 and 1.
 */
export function computeHistoricalConsistency(history: any[], incoming: any): number {
  if (!history.length) return 0.5

  const last = history[history.length - 1]

  try {
    const incomingHash = JSON.stringify(incoming)
    const lastHash = JSON.stringify(last)

    if (incomingHash === lastHash) return 1

    // If structurally similar, partial consistency
    const incomingKeys = Object.keys(incoming)
    const lastKeys = Object.keys(last)

    const overlap = incomingKeys.filter(k => lastKeys.includes(k)).length
    const ratio = overlap / Math.max(incomingKeys.length, lastKeys.length)

    return ratio
  } catch {
    return 0.3
  }
}