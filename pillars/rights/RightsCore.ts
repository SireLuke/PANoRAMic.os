// pillars/rights/RightsCore.ts

/**
 * Rights — Dignity, Safety, and Anti‑Coercion Systems
 * This pillar models civil rights stability, worker protections,
 * exploitation risk, and systemic fairness.
 */

/**
 * Baseline values for rights stability.
 */
export interface RightsBaseline {
  baselineDignity: number;
  baselineSafety: number;
  baselineFairTreatment: number;
  baselineExploitationRisk: number;
}

/**
 * Rules governing rights behavior.
 */
export interface RightsRules {
  dignityFloor: number;
  safetyFloor: number;
  maxExploitationThreshold: number;
  fairnessElasticity: number;
}

/**
 * Default baseline values for Rights.
 */
export const DefaultRightsBaseline: RightsBaseline = {
  baselineDignity: 0.85,
  baselineSafety: 0.8,
  baselineFairTreatment: 0.9,
  baselineExploitationRisk: 0.05,
};

/**
 * Default rules for Rights behavior.
 */
export const DefaultRightsRules: RightsRules = {
  dignityFloor: 0.7,
  safetyFloor: 0.65,
  maxExploitationThreshold: 0.15,
  fairnessElasticity: 0.75,
};
