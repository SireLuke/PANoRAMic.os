import { WorldState } from "../../engine/worldState";
import { GlobalSignals } from "../../engine/globalSignals";
import { RamsTickReport } from "../../engine/ramsTick";

export type DashboardState = {
    world: WorldState;
    signals: GlobalSignals;
    rams: RamsTickReport;
};
