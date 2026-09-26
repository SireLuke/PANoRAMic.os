// engine/worldReducer.ts

import { WorldState } from "./worldState";

import { applyMetabolism } from "./metabolism";
import { applyStability } from "./stability";
import { applyCatastrophe } from "./catastrophe";
import { applyDampening } from "./dampening";
import { applySynthesis } from "./synthesis";
import { applyEvents } from "./events";
import { applyRenewables } from "./renewables";
import { applyIncentives } from "./incentives";
import { applyEconomy } from "./economy";
import { applyICC } from "./icc";
import { applyEducation } from "./education";
import { applyPanitarian } from "./panitarian";
import { applyMigration } from "./migration";

export async function reduceWorld(world: WorldState): Promise<WorldState> {
    let next = { ...world };

    next = applyMetabolism(next);
    next = applyRenewables(next);
    next = applyIncentives(next);
    next = applyCatastrophe(next);
    next = applyDampening(next);
    next = applyStability(next);
    next = applyEvents(next);
    next = applyEconomy(next);
    next = applyICC(next);
    next = await applyEducation(next);
    next = applyPanitarian(next);
    next = applyMigration(next);
    next = applySynthesis(next);

    return next;
}
