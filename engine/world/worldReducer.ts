// engine/world/worldReducer.ts

import { WorldState } from "./worldState.ts"
import { GlobalFrame } from "../global/globalLoopIntegration.ts"
import { applyResources } from "../resources/resources.ts"

export function worldReducer(prev: WorldState, frame: GlobalFrame) {
  const { world: updatedWorld, signals, tick } = frame

  const nextWorld: WorldState = {
    ...prev,
    ...updatedWorld,
    resources: applyResources(updatedWorld.resources),
  }

  return {
    world: nextWorld,
    tick,
    signals,
  }
}

}
