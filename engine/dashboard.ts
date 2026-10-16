// engine/dashboard.ts
// CLI-facing dashboard builder. Canonical packet builder is engine/world/dashboard.ts.

import type { WorldState } from "./world/worldState";
import { buildDashboard as buildDashboardPacket } from "./world/dashboard";

export function buildDashboard(world: WorldState) {
  const packet = buildDashboardPacket({
    world,
    signals: world.synthesis,
    tick: world.tick,
  });

  return {
    ...packet,
    world,
    signals: {
      population: world.population?.total ?? 0,
      risk: packet.collapseRisk,
      resilience: packet.recoveryStrength,
      parSupply: world.economy?.parSupply ?? 0,
      parCap: world.economy?.parCap ?? 0,
      stewardship: world.economy?.stewardshipFund ?? 0,
      governance: world.governance?.panitarianScore ?? 0,
      humanitarianNeed: world.humanitarian?.needScore ?? 0,
      humanitarianRelief: world.humanitarian?.reliefScore ?? 0,
      harm: world.harmindex?.harmScore ?? 0,
      resources: world.resources?.resourceScore ?? 0,
      scarcity: world.resources?.scarcityScore ?? 0,
      sustainability: world.resources?.sustainabilityScore ?? 0,
    },
  };
}
