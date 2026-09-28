// engine/global/globalLoopIntegration.ts

import { WorldState } from "../world/worldState.ts"
import { updateNodeMap } from "../../nodeMap/nodeMap.ts"
import { computeGlobalSignals } from "../../signals/globalSignals.ts"

// Global loop tick result
export interface GlobalFrame {
  world: WorldState
  signals: ReturnType<typeof computeGlobalSignals>
  tick: number
}

// Main planetary loop
export function runGlobalLoop(world: WorldState, tick: number = 0): GlobalFrame {
  // 1. Update node subsystem
  const updatedNodes = updateNodeMap(world.nodes)

  // 2. Update world state with new nodes
  const updatedWorld: WorldState = {
    ...world,
    nodes: updatedNodes,
  }

  // 3. Compute global signals
  const signals = computeGlobalSignals(updatedWorld)

  // 4. Return new planetary frame
  return {
    world: updatedWorld,
    signals,
    tick: tick + 1,
  }
}

