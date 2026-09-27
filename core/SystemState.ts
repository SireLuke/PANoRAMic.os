// core/SystemState.ts
import { MarketsState } from "./pillars/markets/MARKETS_STATE"
import { CultureState } from "./pillars/culture/CULTURE_STATE"
import { MicroAiState } from "./pillars/microAI/MICRO_AI_STATE"
import { NodeState } from "./pillars/nodes/NODES_STATE"
import { ModesState } from "./pillars/modes/MODES_STATE"
// + Rights, Workforce, Ecology, PAR, Infrastructure, Labor, Commons

export interface SystemState {
  markets: MarketsState
  culture: CultureState
  microAi: MicroAiState
  nodes: NodeState[]
  modes: ModesState
  // rights, workforce, ecology, par, infrastructure, labor, commons...
}
