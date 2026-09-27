// core/SystemState.ts
import { MarketsState } from "./pillars/markets/MARKETS_STATE"
import { CultureState } from "./pillars/culture/CULTURE_STATE"
import { MicroAiState } from "./pillars/microAI/MICRO_AI_STATE"
import { NodeState } from "./pillars/nodes/NODES_STATE"
import { ModesState } from "./pillars/modes/MODES_STATE"
import { WorkforceRotationState } from "./pillars/workforce/WORKFORCE_ROTATION_STATE"
import { ParState } from "./pillars/par/PAR_STATE"
import { EcologyState } from "./pillars/ecology/ECOLOGY_STATE"
import { InfrastructureState } from "./pillars/infrastructure/INFRASTRUCTURE_STATE"

export interface SystemState {
  markets: MarketsState
  culture: CultureState
  microAi: MicroAiState
  nodes: NodeState[]
  modes: ModesState
  workforceRotation: WorkforceRotationState
  par: ParState
  ecology: EcologyState
  infrastructure: InfrastructureState
}
