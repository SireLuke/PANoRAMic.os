// pillars/rams/RAMSCore.ts

/**
 * RAMS — Regional & Global Stability Vectors
 * This pillar tracks drift, stability, and systemic balance across all domains.
 */

/**
 * Baseline values for RAMS stability.
 * Engines and micro‑AI will reference these defaults.
 */
export interface RAMSBaseline {
  baselineDrift: number;
  baselineStability: number;
  baselineRegionalStability: number;
  baselineGlobalStability: number;
}

/**
 * Rules governing RAMS behavior.
 * These will be used by engines later to correct drift and maintain stability.
 */
export interface RAMSRules {
  maxDriftThreshold: number;
  stabilityTarget: number;
  regionalWeight: number;
  globalWeight: number;
}

/**
 * Default baseline values for RAMS.
 */
export const DefaultRAMSBaseline: RAMSBaseline = {
  baselineDrift: 0.0,
  baselineStability: 0.75,
  baselineRegionalStability: 0.7,
  baselineGlobalStability: 0.8,
};

/**
 * Default rules for RAMS behavior.
 */
export const DefaultRAMSRules: RAMSRules = {
  maxDriftThreshold: 0.2,
  stabilityTarget: 0.75,
  regionalWeight: 0.6,
  globalWeight: 0.4,
};
