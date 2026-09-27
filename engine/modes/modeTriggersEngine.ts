// engine/modes/modeTriggersEngine.ts

import { ModesState } from "../../core/pillars/modes/MODES_STATE"
import { EcologyState } from "../../core/pillars/ecology/ECOLOGY_STATE"
import { InfrastructureState } from "../../core/pillars/infrastructure/INFRASTRUCTURE_STATE"
import { MarketsState } from "../../core/pillars/markets/MARKETS_STATE"
import { ParState } from "../../core/pillars/par/PAR_STATE"

export function computeModeTriggers({
  modes,
  ecology,
  infrastructure,
  markets,
  par,
}: {
  modes: ModesState
  ecology: EcologyState
  infrastructure: InfrastructureState
  markets: MarketsState
  par: ParState
}): ModesState {
  let activeMode = modes.activeMode

  // 1. Emergency mode: ecology collapse or infrastructure failure
  if (
    ecology.degradationIndex > 0.8 ||
    infrastructure.failureIndex > 0.8 ||
    markets.stabilityIndex < 0.2
  ) {
    activeMode = "emergency"
  }

  // 2. Ecology restoration mode
  else if (ecology.degradationIndex > 0.5) {
    activeMode = "ecology_restoration"
  }

  // 3. Infrastructure expansion mode
  else if (infrastructure.resilienceIndex < 0.4) {
    activeMode = "infrastructure_expansion"
  }

  // 4. Market stabilization mode
  else if (markets.extractivePressureIndex > 0.6) {
    activeMode = "market_stabilization"
  }

  // 5. PAR stabilization mode
  else if (!par.parCapCompliance) {
    activeMode = "par_stabilization"
  }

  // 6. Default cooperative mode
  else {
    activeMode = "cooperative_growth"
  }

  return {
    ...modes,
    activeMode,
  }
}
