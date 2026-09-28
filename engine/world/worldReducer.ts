// engine/world/worldReducer.ts

import { WorldState } from "./worldState.ts"
import { GlobalFrame } from "../global/globalLoopIntegration.ts"

// Reducer result
export interface WorldReducerResult {
  world: WorldState
  tick: number
  signals: GlobalFrame["signals"]
}

// Main reducer
export function worldReducer(prev: WorldState, frame: GlobalFrame): WorldReducerResult {
  const { world: updatedWorld, signals, tick } = frame

  // Merge world state immutably
  const nextWorld: WorldState = {
    ...prev,

    // Replace nodes with updated nodes
    nodes: updatedWorld.nodes,

    // Replace subsystem slices if present
    population: updatedWorld.population ?? prev.population,
    resources: updatedWorld.resources ?? prev.resources,
    governance: updatedWorld.governance ?? prev.governance,
    rights: updatedWorld.rights ?? prev.rights,
    education: updatedWorld.education ?? prev.education,
    economy: updatedWorld.economy ?? prev.economy,
    ecology: updatedWorld.ecology ?? prev.ecology,
    metabolism: updatedWorld.metabolism ?? prev.metabolism,
    infrastructure: updatedWorld.infrastructure ?? prev.infrastructure,
    humanitarian: updatedWorld.humanitarian ?? prev.humanitarian,
    migration: updatedWorld.migration ?? prev.migration,
    trafficking: updatedWorld.trafficking ?? prev.trafficking,
    harmindex: updatedWorld.harmindex ?? prev.harmindex,
    icc: updatedWorld.icc ?? prev.icc,
    synthesis: updatedWorld.synthesis ?? prev.synthesis,
  }

  return {
    world: nextWorld,
    tick,
    signals,
  }
}
