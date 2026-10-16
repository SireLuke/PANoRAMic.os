// pillars/stability/StabilityCore.ts

/**
 * Stability — Systemic Balance & Shock Absorption
 * This pillar models drift correction, resilience under stress,
 * cascading failure prevention, and long‑term systemic durability.
 */

/**
 * Baseline values for systemic stability.
 */
export interface StabilityBaseline {
  baselineSystemStability: number;
  baselineShockResistance: number;
  baselineDriftRisk: number;
  baselineResilience: number;
}

/**
 * Rules governing stability behavior.
 */
export interface StabilityRules {
  stabilityFloor: number;
  maxDriftThreshold: number;
  shockElasticity: number;
  resilienceElasticity: number;
}

/**
 * Default baseline values for Stability.
 */
export const DefaultStabilityBaseline: StabilityBaseline = {
  baselineSystemStability: 0.8,
  baselineShockResistance: 0.75,
  baselineDriftRisk: 0.1,
  baselineResilience: 0.7,
};

/**
 * Default rules for Stability behavior.
 */
export const DefaultStabilityRules: StabilityRules = {
  stabilityFloor: 0.65,
  maxDriftThreshold: 0.25,
  shockElasticity: 0.7,
  resilienceElasticity: 0.6,
};
