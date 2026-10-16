// pillars/ecology/EcologyCore.ts

/**
 * Ecology — Planetary Regeneration & Biome Stability
 * This pillar models biome health, regeneration cycles, and ecological risk.
 */

/**
 * Baseline values for ecological stability.
 */
export interface EcologyBaseline {
  baselineBiomeHealth: number;
  baselineRegenerationRate: number;
  baselineEcologicalRisk: number;
}

/**
 * Rules governing ecological behavior.
 */
export interface EcologyRules {
  minBiomeHealth: number;
  maxRiskThreshold: number;
  regenerationElasticity: number;
}

/**
 * Default baseline values for Ecology.
 */
export const DefaultEcologyBaseline: EcologyBaseline = {
  baselineBiomeHealth: 0.8,
  baselineRegenerationRate: 0.05,
  baselineEcologicalRisk: 0.1,
};

/**
 * Default rules for Ecology behavior.
 */
export const DefaultEcologyRules: EcologyRules = {
  minBiomeHealth: 0.5,
  maxRiskThreshold: 0.25,
  regenerationElasticity: 0.75,
};
