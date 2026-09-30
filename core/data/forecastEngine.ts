// core/data/forecastEngine.ts

/**
 * Global Forecast Engine:
 * Predicts collapse and recovery trajectories based on signal trends.
 */

export type Forecast = {
  timestamp: number
  collapseTrajectory: number
  recoveryTrajectory: number
  riskTrajectory: number
  stabilityTrajectory: number
}

export class ForecastEngine {
  private history: Forecast[] = []
  private maxSize: number

  constructor(maxSize: number = 200) {
    this.maxSize = maxSize
  }

  compute(globalSignals: any): Forecast {
    const now = Date.now()

    const {
      collapsePressure = 0.5,
      recoveryStrength = 0.5,
      risk = 0.5,
      stability = 0.5
    } = globalSignals

    // Simple trend projection using weighted deltas
    const collapseTrajectory = collapsePressure * (1 - stability)
    const recoveryTrajectory = recoveryStrength * (1 - collapsePressure)
    const riskTrajectory = risk * (1 - stability)
    const stabilityTrajectory = stability * (1 - risk)

    const forecast: Forecast = {
      timestamp: now,
      collapseTrajectory,
      recoveryTrajectory,
      riskTrajectory,
      stabilityTrajectory
    }

    this.history.push(forecast)
    if (this.history.length > this.maxSize) {
      this.history.shift()
    }

    return forecast
  }

  getHistory() {
    return this.history
  }

  getRecent(limit: number = 20) {
    return this.history.slice(-limit)
  }
}