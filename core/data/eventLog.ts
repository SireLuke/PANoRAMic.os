// core/data/eventLog.ts

/**
 * World Event Log:
 * Stores every world-state change, alert, forecast shift, and ingestion event.
 */

export type WorldEvent = {
  id: string
  timestamp: number
  type: "ingestion" | "alert" | "forecast" | "diff"
  description: string
  payload: any
}

export class EventLog {
  private events: WorldEvent[] = []
  private maxSize: number

  constructor(maxSize: number = 5000) {
    this.maxSize = maxSize
  }

  add(type: WorldEvent["type"], description: string, payload: any) {
    const event: WorldEvent = {
      id: `${type}-${Date.now()}-${Math.random().toString(36).slice(2)}`,
      timestamp: Date.now(),
      type,
      description,
      payload
    }

    this.events.push(event)

    if (this.events.length > this.maxSize) {
      this.events.shift()
    }
  }

  getAll() {
    return this.events
  }

  getRecent(limit: number = 50) {
    return this.events.slice(-limit)
  }
}