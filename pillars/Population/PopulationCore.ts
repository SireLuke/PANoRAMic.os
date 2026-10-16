// pillars/population/PopulationCore.ts

/**
 * Population — Demographic Stability & Household Resilience
 * This pillar models demographic balance, migration flows,
 * household stability, and long‑term civilizational viability.
 */

/**
 * Baseline values for population stability.
 */
export interface PopulationBaseline {
  baselinePopulationHealth: number;
  baselineBirthRate: number;
  baselineDeathRate: number;
  baselineMigrationFlow: number;
  baselineDependencyRatio: number;
}

/**
 * Rules governing population behavior.
 */
export interface PopulationRules {
  minPopulationHealth: number;
  maxDependencyThreshold: number;
  migrationElasticity: number;
  birthRateElasticity: number;
}

/**
 * Default baseline values for Population.
 */
export const DefaultPopulationBaseline: PopulationBaseline = {
  baselinePopulationHealth: 0.8,
  baselineBirthRate: 0.02,
  baselineDeathRate: 0.01,
  baselineMigrationFlow: 0.0,
  baselineDependencyRatio: 0.5,
};

/**
 * Default rules for Population behavior.
 */
export const DefaultPopulationRules: PopulationRules = {
  minPopulationHealth: 0.6,
  maxDependencyThreshold: 0.7,
  migrationElasticity: 0.5,
  birthRateElasticity: 0.4,
};
