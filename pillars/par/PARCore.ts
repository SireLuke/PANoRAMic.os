// pillars/par/PARCore.ts

import { ParState } from "./PAR_STATE.ts";

/**
 * Baseline values for the PAR dignity currency.
 * These are the defaults engines and micro‑AI will reference.
 */
export interface PARBaseline {
  baselineDignity: number;
  baselineStability: number;
  baselineRecovery: number;
  baselineExtractionRisk: number;
}

/**
 * Rules governing PAR behavior.
 * These will be used by engines later.
 */
export interface PARRules {
  dignityFloor: number;
  maxExtractionThreshold: number;
  stabilityTarget: number;
  recoveryRate: number;
}

/**
 * Default baseline values for PAR.
 */
export const DefaultPARBaseline: PARBaseline = {
  baselineDignity: 1.0,
  baselineStability: 0.75,
  baselineRecovery: 0.5,
  baselineExtractionRisk: 0.0,
};

/**
 * Default rules for PAR behavior.
 */
export const DefaultPARRules: PARRules = {
  dignityFloor: 1.0,
  maxExtractionThreshold: 0.15,
  stabilityTarget: 0.75,
  recoveryRate: 0.05,
};
