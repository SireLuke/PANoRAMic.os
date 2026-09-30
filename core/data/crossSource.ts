// core/data/crossSource.ts

/**
 * Cross‑Source Agreement Engine:
 * Compares incoming data with other sources received recently.
 */

export class SourceAgreementStore {
  private recentSources: Record<string, any[]> = {}
  private maxSize: number

  constructor(maxSize: number = 50) {
    this.maxSize = maxSize
  }

  add(sourceName: string, data: any) {
    if (!this.recentSources[sourceName]) {
      this.recentSources[sourceName] = []
    }

    this.recentSources[sourceName].push(data)

    if (this.recentSources[sourceName].length > this.maxSize) {
      this.recentSources[sourceName].shift()
    }
  }

  getAllSources() {
    return this.recentSources
  }

  /**
   * Compute agreement score between incoming data and other sources.
   * Returns 0–1.
   */
  computeAgreement(incoming: any): number {
    const allSources = Object.values(this.recentSources)
    if (!allSources.length) return 0.5

    let total = 0
    let matches = 0

    try {
      const incomingKeys = Object.keys(incoming)

      for (const sourceHistory of allSources) {
        for (const past of sourceHistory) {
          total++

          const pastKeys = Object.keys(past)
          const overlap = incomingKeys.filter(k => pastKeys.includes(k)).length
          const ratio = overlap / Math.max(incomingKeys.length, pastKeys.length)

          if (ratio > 0.6) matches++
        }
      }

      return total === 0 ? 0.5 : matches / total
    } catch {
      return 0.4
    }
  }
}