// pillars/commons/CommonsCore.ts

/**
 * Commons — Shared Resources & Cooperative Infrastructure
 * This pillar models public goods, community resilience, and non‑market value.
 */

/**
 * Baseline values for commons stability.
 */
export interface CommonsBaseline {
  baselinePublicGoods: number;
  baselineCooperativeAccess: number;
  baselineCommonsHealth: number;
  baselinePrivatizationRisk: number;
}

/**
 * Rules governing commons behavior.
 */
export interface CommonsRules {
  publicGoodsFloor: number;
  maxPrivatizationThreshold: number;
  cooperativeElasticity: number;
  commonsStabilityTarget: number;
}

/**
 * Default baseline values for Commons.
 */
export const DefaultCommonsBaseline: CommonsBaseline = {
  baselinePublicGoods: 0.8,
  baselineCooperativeAccess: 0.75,
  baselineCommonsHealth: 0.85,
  baselinePrivatizationRisk: 0.1,
};

/**
 * Default rules for Commons behavior.
 */
export const DefaultCommonsRules: CommonsRules = {
  publicGoodsFloor: 0.6,
  maxPrivatizationThreshold: 0.2,
  cooperativeElasticity: 0.7,
  commonsStabilityTarget: 0.8,
};
