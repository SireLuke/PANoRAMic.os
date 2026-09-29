// core/data/provenance.ts

/**
 * Provenance Tracking Layer:
 * Records where data came from, when it was ingested,
 * and how it affected the world.
 */

export type ProvenanceRecord = {
  timestamp: number
  funnelType: string
  sourceName: string
  sourceUrl?: string
  affectedNodes?: string[]
  affectedPillars?: string[]
  affectedGlobals?: string[]
  trustScore?: number
  rawDataHash?: string
}

export class ProvenanceTracker {
  private history: ProvenanceRecord[] = []

  addRecord(record: ProvenanceRecord) {
    this.history.push(record)
  }

  getHistory() {
    return this.history
  }

  getRecent(limit: number = 20) {
    return this.history.slice(-limit)
  }
}

/**
 * Utility:
 * Hash raw data for integrity checking.
 */
export function hashData(data: any): string {
  try {
    const json = JSON.stringify(data)
    let hash = 0
    for (let i = 0; i < json.length; i++) {
      hash = (hash * 31 + json.charCodeAt(i)) >>> 0
    }
    return hash.toString(16)
  } catch {
    return "0"
  }
}