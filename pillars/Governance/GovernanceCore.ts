// pillars/governance/GovernanceCore.ts

/**
 * Governance — Institutional Stability & Anti‑Capture Systems
 * This pillar models legitimacy, transparency, procedural integrity,
 * and resistance to corporate or political capture.
 */

/**
 * Baseline values for governance stability.
 */
export interface GovernanceBaseline {
  baselineLegitimacy: number;
  baselineTransparency: number;
  baselineAntiCapture: number;
  baselineProceduralIntegrity: number;
}

/**
 * Rules governing governance behavior.
 */
export interface GovernanceRules {
  legitimacyFloor: number;
  transparencyTarget: number;
  maxCaptureRisk: number;
  proceduralElasticity: number;
}

/**
 * Default baseline values for Governance.
 */
export const DefaultGovernanceBaseline: GovernanceBaseline = {
  baselineLegitimacy: 0.75,
  baselineTransparency: 0.8,
  baselineAntiCapture: 0.9,
  baselineProceduralIntegrity: 0.85,
};

/**
 * Default rules for Governance behavior.
 */
export const DefaultGovernanceRules: GovernanceRules = {
  legitimacyFloor: 0.6,
  transparencyTarget: 0.85,
  maxCaptureRisk: 0.2,
  proceduralElasticity: 0.7,
};
