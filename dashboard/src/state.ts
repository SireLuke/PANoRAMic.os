import { WorldState } from "../../engine/worldState";
import { aggregateSignals } from "../../engine/globalSignals";
import { runRamsTick } from "../../engine/ramsTick";
import { DashboardState } from "./types";

export function buildDashboardState(world: WorldState): DashboardState {
    const signals = aggregateSignals(world);
    const rams = runRamsTick(world);

    return {
        world,
        signals,
        rams
    };
}
