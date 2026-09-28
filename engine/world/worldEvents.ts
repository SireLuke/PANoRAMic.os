// engine/world/worldEvents.ts

import { WorldState } from "./worldState.ts"
import { GlobalFrame } from "../global/globalLoopIntegration.ts"

// Event types
export type WorldEventType =
  | "tick"
  | "world-initialized"
  | "nodes-updated"
  | "signals-updated"
  | "collapse-warning"
  | "recovery-surge"
  | "real-world-life-report"

// Event payload
export interface WorldEvent {
  type: WorldEventType
  tick: number
  world: WorldState
  signals: any
  message?: string
}

// Event listeners
type Listener = (event: WorldEvent) => void

const listeners: Listener[] = []

// Subscribe to world events
export function onWorldEvent(listener: Listener) {
  listeners.push(listener)
}

// Emit event
export function emitWorldEvent(event: WorldEvent) {
  for (const listener of listeners) {
    listener(event)
  }
}

// Emit tick event
export function emitTickEvent(frame: GlobalFrame) {
  emitWorldEvent({
    type: "tick",
    tick: frame.tick,
    world: frame.world,
    signals: frame.signals,
  })
}

// Emit real-world life report event
export function emitRealWorldLifeReport(frame: GlobalFrame, message: string) {
  emitWorldEvent({
    type: "real-world-life-report",
    tick: frame.tick,
    world: frame.world,
    signals: frame.signals,
    message,
  })
}

// Emit subsystem-specific events
export function emitSubsystemEvents(frame: GlobalFrame) {
  const { signals } = frame

  if (signals.collapsePressure > 0.7) {
    emitWorldEvent({
      type: "collapse-warning",
      tick: frame.tick,
      world: frame.world,
      signals,
      message: "High collapse pressure detected",
    })
  }

  if (signals.recovery > 0.6) {
    emitWorldEvent({
      type: "recovery-surge",
      tick: frame.tick,
      world: frame.world,
      signals,
      message: "Recovery surge detected",
    })
  }
}
