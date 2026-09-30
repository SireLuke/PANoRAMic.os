// core/data/alertEngine.ts

/**
 * Global Alerts Engine:
 * Raises alerts based on globalSignals thresholds.
 */

export type GlobalSignals = {
  stability?: number
  risk?: number
  collapsePressure?: number
  recoveryStrength?: number
  synthesis?: number
  [key: string]: number | undefined
}

export type Alert = {
  id: string
  type: "collapse" | "risk" | "stability" | "recovery"
  severity: "low" | "medium" | "high" | "critical"
  message: string
  timestamp: number
}

export class AlertEngine {
  private alerts: Alert[] = []

  evaluate(globalSignals: GlobalSignals) {
    const now = Date.now()

    const { stability = 0.5, risk = 0.5, collapsePressure = 0.5, recoveryStrength = 0.5 } = globalSignals

    // Collapse alerts
    if (collapsePressure > 0.7 && stability < 0.4) {
      this.add({
        id: `collapse-${now}`,
        type: "collapse",
        severity: collapsePressure > 0.85 ? "critical" : "high",
        message: "High collapse pressure with low stability detected.",
        timestamp: now
      })
    }

    // Risk alerts
    if (risk > 0.7) {
      this.add({
        id: `risk-${now}`,
        type: "risk",
        severity: risk > 0.85 ? "critical" : "high",
        message: "Global risk levels elevated.",
        timestamp: now
      })
    }

    // Stability alerts
    if (stability < 0.3) {
      this.add({
        id: `stability-${now}`,
        type: "stability",
        severity: "high",
        message: "Global stability dangerously low.",
        timestamp: now
      })
    }

    // Recovery alerts
    if (recoveryStrength > 0.7 && collapsePressure < 0.5) {
      this.add({
        id: `recovery-${now}`,
        type: "recovery",
        severity: "medium",
        message: "Strong recovery signals detected.",
        timestamp: now
      })
    }
  }

  private add(alert: Alert) {
    this.alerts.push(alert)
    if (this.alerts.length > 200) {
      this.alerts.shift()
    }
    console.warn(`[PAN‑OS ALERT] ${alert.type.toUpperCase()} (${alert.severity}): ${alert.message}`)
  }

  getAlerts() {
    return this.alerts
  }

  getRecent(limit: number = 20) {
    return this.alerts.slice(-limit)
  }
}