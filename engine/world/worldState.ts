// engine/world/worldState.ts

import { NodeState } from "../../core/pillars/nodes/NODES_STATE.ts"

export interface WorldClassified {
  records: Record<string, number>
}

export interface WorldState {
  tick: number

  nodes: Record<string, NodeState>

  population: any
  resources: any
  governance: any
  rights: any
  education: any
  economy: any
  ecology: any
  metabolism: any
  infrastructure: any
  humanitarian: any
  migration: any
  trafficking: any
  harmindex: any
  icc: any
  synthesis: any

  classified: WorldClassified
}
