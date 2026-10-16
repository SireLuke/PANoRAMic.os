// pillars/labor/LaborCore.ts

/**
 * Labor — Worker Stability, Fairness, and Cooperative Productivity
 * This pillar models worker well‑being, burnout risk, wage fairness,
 * job mobility, and exploitation detection.
 */

/**
 * Baseline values for labor stability.
 */
export interface LaborBaseline {
  baselineWorkerStability: number;
  baselineBurnoutRisk: number;
  baselineWageFairness: number;
  baselineJobMobility: number;
}

/**
 * Rules governing labor behavior.
 */
export interface LaborRules {
  stabilityFloor: number;
  maxBurnoutThreshold: number;
  fairnessElasticity: number;
  mobilityElasticity: number;
}

/**
 * Default baseline values for Labor.
 */
export const DefaultLaborBaseline: LaborBaseline = {
  baselineWorkerStability: 0.8,
  baselineBurnoutRisk: 0.1,
  baselineWageFairness: 0.75,
  baselineJobMobility: 0.6,
};

/**
 * Default rules for Labor behavior.
 */
export const DefaultLaborRules: LaborRules = {
  stabilityFloor: 0.65,
  maxBurnoutThreshold: 0.25,
  fairnessElasticity: 0.7,
  mobilityElasticity: 0.6,
};
