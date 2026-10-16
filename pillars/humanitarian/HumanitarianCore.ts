// pillars/humanitarian/HumanitarianCore.ts

/**
 * Humanitarian — Crisis Response & Emergency Dignity Protection
 * This pillar models vulnerability detection, aid distribution,
 * harm‑reduction baselines, and humane response under extreme conditions.
 */

/**
 * Baseline values for humanitarian stability.
 */
export interface HumanitarianBaseline {
  baselineVulnerability: number;
  baselineAidCoverage: number;
  baselineHarmReduction: number;
  baselineEmergencyResilience: number;
}

/**
 * Rules governing humanitarian behavior.
 */
export interface HumanitarianRules {
  maxVulnerabilityThreshold: number;
  aidElasticity: number;
  harmReductionElasticity: number;
  resilienceFloor: number;
}

/**
 * Default baseline values for Humanitarian.
 */
export const DefaultHumanitarianBaseline: HumanitarianBaseline = {
  baselineVulnerability: 0.1,
  baselineAidCoverage: 0.75,
  baselineHarmReduction: 0.8,
  baselineEmergencyResilience: 0.65,
};

/**
 * Default rules for Humanitarian behavior.
 */
export const DefaultHumanitarianRules: HumanitarianRules = {
  maxVulnerabilityThreshold: 0.25,
  aidElasticity: 0.7,
  harmReductionElasticity: 0.75,
  resilienceFloor: 0.5,
};
