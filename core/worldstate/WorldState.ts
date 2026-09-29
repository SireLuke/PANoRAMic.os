// core/worldstate/WorldState.ts

import { NodeState } from "../pillars/nodes/NODES_STATE"

export interface WorldState {
  tick: number

  // Node system
  nodes: Record<string, NodeState>

  // Pillars
  population: any
  resources: any
  economy: any
  governance: any
  humanitarian: any
  medical: any
  antigenocide: any
  markets: any
  crime: any
  education: any
  migration: any
  trafficking: any
  transparency: any
  corporatecapture: any
  epistemic: any
  repairability: any
  quantum: any

  // Global signals
  globalSignals: {
    stability: number
    risk: number
    synthesis: number
    collapsePressure: number
    recoveryStrength: number
  }

  // Configuration
  config: {
    tickRate: number
    maxTicks: number
  }
}

// Default world
export const createWorldState = (): WorldState => ({
  tick: 0,

  nodes: {},

  population: {},
  resources: {},
  economy: {},
  governance: {},
  humanitarian: {},
  medical: {},
  antigenocide: {},
  markets: {},
  crime: {},
  education: {},
  migration: {},
  trafficking: {},
  transparency: {},
  corporatecapture: {},
  epistemic: {},
  repairability: {},
  quantum: {},

  globalSignals: {
    stability: 0,
    risk: 0,
    synthesis: 0,
    collapsePressure: 0,
    recoveryStrength: 0
  },

  config: {
    tickRate: 1,
    maxTicks: Infinity
  }
})
