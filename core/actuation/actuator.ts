// core/actuation/actuator.ts

/**
 * Actuation Layer:
 * PAN-OS output engine for sending signals to external systems.
 *
 * This does NOT execute real-world commands yet.
 * It provides a safe, structured interface for:
 * - dashboards
 * - hardware controllers
 * - micro-AI agents
 * - reactor boards
 * - robotics
 * - infrastructure
 */

export type ActuationSignal = {
  id: string
  timestamp: number
  type: "alert" | "forecast" | "globalSignal" | "nodeUpdate" | "custom"
  payload: any
}

export class Actuator {
  private listeners: ((signal: ActuationSignal) => void)[] = []

  send(type: ActuationSignal["type"], payload: any) {
    const signal: ActuationSignal = {
      id: `${type}-${Date.now()}-${Math.random().toString(36).slice(2)}`,
      timestamp: Date.now(),
      type,
      payload
    }

    for (const listener of this.listeners) {
      listener(signal)
    }
  }

  onSignal(listener: (signal: ActuationSignal) => void) {
    this.listeners.push(listener)
  }
}