// engine/dashboard.ts

import { WorldState } from "./worldState";
import { buildDashboardState } from "../dashboard/src/state";

export function buildDashboard(world: WorldState) {
    return buildDashboardState(world);
}
