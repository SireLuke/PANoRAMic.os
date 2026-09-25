// engine/worldReducer.ts

import { WorldState } from "./worldState";

// Subsystem imports (append more as they come online)
import { applyMetabolism } from "./metabolism";
import { applyStability } from "./stability";
import { applyCatastrophe } from "./catastrophe";
import { applyDampening } from "./dampening";
import { applySynthesis } from "./synthesis";
import { applyEvents } from "./events";
import { applyRenewables } from "./renewables";
import { applyIncentives } from "./incentives";
import { applyEconomy } from "./economy";

export function reduceWorld(world: WorldState): WorldState {
    let next = { ...world };

    // Apply subsystem updates in logical order
    next = applyMetabolism(next);
    next = applyRenewables(next);
    next = applyIncentives(next);
    next = applyCatastrophe(next);
    next = applyDampening(next);
    next = applyStability(next);
    next = applyEvents(next);
    next = applySynthesis(next);
    next = applyEconomy(next);

    return next;
}
