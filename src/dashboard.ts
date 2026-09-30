import { serve } from "https://deno.land/std/http/server.ts";
import { runPreAudit } from "./rams.ts";
import { computeRSDV } from "./rsdv.ts";
import { initPAR } from "./par.ts";
import { initStagnation } from "./stagnation.ts";

export async function initDashboard() {
  console.log("[DASH] Starting PlanetView server on http://localhost:3000");

  const audit = await runPreAudit();
  const rsdv = computeRSDV(audit);
  const par = initPAR(audit.globalPopulation, rsdv);
  const stag = initStagnation();

  const metrics = { stability: audit.stabilityScore, rsdv, parMax: par.parMax, stagnation: stag.metric };

  serve((req) => {
    if (req.url === "/metrics") {
      return new Response(JSON.stringify(metrics), { headers: { "content-type": "application/json" } });
    }
    return new Response(Deno.readTextFileSync("./dashboard/index.html"), { headers: { "content-type": "text/html" } });
  }, { port: 3000 });
}
