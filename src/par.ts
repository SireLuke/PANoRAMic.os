export interface PARState {
  parMax: number;
  dignityFloor: number;
  stewardshipBase: number;
  extractionLimit: number;
  velocityBaseline: number;
}

export function initPAR(globalPopulation: number, rsdv: number): PARState {
  const parMax = globalPopulation * 1.35 * rsdv;

  return {
    parMax,
    dignityFloor: parMax * 0.00000001,
    stewardshipBase: parMax * 0.00000002,
    extractionLimit: 0.7,
    velocityBaseline: 1.0,
  };
}
