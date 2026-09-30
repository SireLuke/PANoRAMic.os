import type { PARState } from "./par.ts";

export interface DemurrageConfig {
  baseRate: number;
  highHoardingRate: number;
}

export function initDemurrage(parState: PARState): DemurrageConfig {
  const config: DemurrageConfig = {
    baseRate: 0.01,
    highHoardingRate: 0.03,
  };

  // Later: tie rates to parState.parMax, velocity, stagnation, etc.
  return config;
}
