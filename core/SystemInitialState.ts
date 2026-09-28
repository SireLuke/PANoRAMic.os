// core/SystemInitialState.ts

import { SystemState } from "./SystemState"

import { defaultMarketsState } from "./pillars/markets/MARKETS_METRICS"
import { defaultCultureState } from "./pillars/culture/CULTURE_METRICS"
import { defaultMicroAiState } from "./pillars/microAI/MICRO_AI_METRICS"
import { defaultNodeState } from "./pillars/nodes/NODES_METRICS"
import { defaultModesState } from "./pillars/modes/MODES_METRICS"
import { defaultWorkforceRotationState } from "./pillars/workforce/WORKFORCE_ROTATION_METRICS"
import { defaultParState } from "./pillars/par/PAR_METRICS"
import { defaultEcologyState } from "./pillars/ecology/ECOLOGY_METRICS"
import { computeInfrastructureMetrics } from "./pillars/infrastructure/INFRASTRUCTURE_METRICS.ts"

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
