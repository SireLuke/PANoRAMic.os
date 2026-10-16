// pillars/gep/GEPCore.ts

/**
 * GEP — Global Economics Platform
 * This pillar models humane, non‑extractive planetary economics.
 */

/**
 * Baseline values for global economics.
 * Engines and micro‑AI will reference these defaults.
 */
export interface GEPBaseline {
  baselineGDP: number;
  baselineTradeFlow: number;
  baselineCurrencyStability: number;
  baselineSovereignRisk: number;
}

/**
 * Rules governing GEP behavior.
 * These will be used by engines later to stabilize economic systems.
 */
export interface GEPRules {
  gdpFloor: number;
  maxRiskThreshold: number;
  tradeElasticity: number;
  currencyStabilityTarget: number;
}

/**
 * Default baseline values for GEP.
 */
export const DefaultGEPBaseline: GEPBaseline = {
  baselineGDP: 1.0,
  baselineTradeFlow: 1.0,
  baselineCurrencyStability: 0.75,
  baselineSovereignRisk: 0.1,
};

/**
 * Default rules for GEP behavior.
 */
export const DefaultGEPRules: GEPRules = {
  gdpFloor: 0.5,
  maxRiskThreshold: 0.25,
  tradeElasticity: 0.8,
  currencyStabilityTarget: 0.75,
};
