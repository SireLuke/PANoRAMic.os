// cli/src/commands/dashboard.ts

import { initialWorld } from "../../engine/worldState";
import { buildDashboard } from "../../engine/dashboard";

export function dashboardCommand() {
    const dashboard = buildDashboard(initialWorld);

    console.log("PANoRAMic.os Dashboard (CLI)");
    console.log("-----------------------------");

    console.log("World:");
    console.log(`  Population: ${dashboard.signals.population}`);
    console.log(`  Risk: ${dashboard.signals.risk}`);
    console.log(`  Resilience: ${dashboard.signals.resilience}`);

    console.log("\nEconomy:");
    console.log(`  PAR Supply: ${dashboard.signals.parSupply}`);
    console.log(`  PAR Cap: ${dashboard.signals.parCap}`);
    console.log(`  Stewardship: ${dashboard.signals.stewardship}`);

    console.log("\nGovernance:");
    console.log(`  Panitarian Score: ${dashboard.signals.governance}`);

    console.log("\nHumanitarian:");
    console.log(`  Need: ${dashboard.signals.humanitarianNeed}`);
    console.log(`  Relief: ${dashboard.signals.humanitarianRelief}`);

    console.log("\nHarm:");
    console.log(`  Harm Score: ${dashboard.signals.harm}`);

    console.log("\nResources:");
    console.log(`  Resource Score: ${dashboard.signals.resources}`);
    console.log(`  Scarcity: ${dashboard.signals.scarcity}`);
    console.log(`  Sustainability: ${dashboard.signals.sustainability}`);

    console.log("\nSynthesis:");
    console.log(`  Coherence: ${dashboard.world.synthesis.coherenceScore ?? 0}`);
}
