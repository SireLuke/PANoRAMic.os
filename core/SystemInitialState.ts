// core/SystemInitialState.ts

import { SystemState } from "./SystemState"

import { defaultMarketsState } from "../pillars/markets/MARKETS_METRICS.ts"
import { defaultCultureState } from "../pillars/culture/CULTURE_METRICS.ts"
import { defaultMicroAiState } from "../pillars/microAI/MICRO_AI_METRICS.ts"
import { defaultNodeState } from "../pillars/nodes/NODES_METRICS.ts"
import { defaultModesState } from "../pillars/modes/MODES_METRICS.ts"
import { defaultWorkforceRotationState } from "../pillars/workforce/WORKFORCE_ROTATION_METRICS.ts"
import { defaultParState } from "../pillars/par/PAR_METRICS.ts"
import { defaultEcologyState } from "../pillars/ecology/ECOLOGY_METRICS.ts"
import { computeInfrastructureMetrics } from "../pillars/infrastructure/INFRASTRUCTURE_METRICS.ts"

export const initialSystemState: SystemState = {
  markets: defaultMarketsState,
  culture: defaultCultureState,
  microAi: defaultMicroAiState,
  nodes: [defaultNodeState],
  modes: defaultModesState,
  workforceRotation: defaultWorkforceRotationState,
  par: defaultParState,
  ecology: defaultEcologyState,
  infrastructure: defaultInfrastructureState,
}
