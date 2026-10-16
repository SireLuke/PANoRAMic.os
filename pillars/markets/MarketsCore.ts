// pillars/markets/MarketsCore.ts

/**
 * Markets — Cooperative, Anti‑Extraction Commerce
 * This pillar models market fairness, extraction risk, and cooperative flows.
 */

/**
 * Baseline values for market behavior.
 */
export interface MarketsBaseline {
  baselineExtractionRisk: number;
  baselineFairnessIndex: number;
  baselineCooperativeFlow: number;
}

/**
 * Rules governing market behavior.
 */
export interface MarketsRules {
  maxExtractionThreshold: number;
  fairnessTarget: number;
  cooperativeWeight: number;
}

/**
 * Default baseline values for Markets.
 */
export const DefaultMarketsBaseline: MarketsBaseline = {
  baselineExtractionRisk: 0.0,
  baselineFairnessIndex: 0.75,
  baselineCooperativeFlow: 0.6,
};

/**
 * Default rules for Markets behavior.
 */
export const DefaultMarketsRules: MarketsRules = {
  maxExtractionThreshold: 0.2,
  fairnessTarget: 0.8,
  cooperativeWeight: 0.7,
};
