import { initKernel } from "./kernel.ts";
import { initFeeds } from "./feeds.ts";
import { runPreAudit } from "./rams.ts";
import { computeRSDV } from "./rsdv.ts";
import { initPAR } from "./par.ts";
import { initDemurrage } from "./demurrage.ts";
import { initStagnation } from "./stagnation.ts";
import { initNodes } from "./nodes.ts";
import { initDashboard } from "./dashboard.ts";

export async function bootSystem() {
  console.log("[BOOT] Initializing PAN Kernel...");
  await initKernel();

  console.log("[BOOT] Initializing feed integration layer...");
  await initFeeds();

  console.log("[RAMS] Running pre-audit...");
  const audit = await runPreAudit();
  console.log("[RAMS] Stability Score:", audit.stabilityScore);

  console.log("[RSDV] Calculating Resource Scarcity Dynamic Vector...");
  const rsdv = computeRSDV(audit);
  console.log("[RSDV] Scarcity vector:", rsdv.toFixed(3));

  console.log("[PAR] Initializing Panitarian Asset Receipt economy...");
  const parState = initPAR(audit.globalPopulation, rsdv);
  console.log("[PAR] Soft-peg cap:", parState.parMax);

  console.log("[DEM] Initializing demurrage engine...");
  initDemurrage(parState);

  console.log("[STAG] Initializing stagnation metric...");
  initStagnation();

  console.log("[NODE] Booting node network...");
  initNodes();

  console.log("[DASH] Bringing PlanetView dashboard online...");
  initDashboard();

  console.log("[PAN] System boot complete.");
}

if (import.meta.main) {
  await bootSystem();
}
