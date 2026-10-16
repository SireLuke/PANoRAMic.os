// pillars/education/EducationCore.ts

/**
 * Education — Knowledge Distribution & Cooperative Skill Formation
 * This pillar models literacy, learning capacity, epistemic stability,
 * and generational uplift.
 */

/**
 * Baseline values for educational stability.
 */
export interface EducationBaseline {
  baselineLiteracy: number;
  baselineNumeracy: number;
  baselineLearningCapacity: number;
  baselineEpistemicStability: number;
}

/**
 * Rules governing educational behavior.
 */
export interface EducationRules {
  literacyFloor: number;
  numeracyFloor: number;
  misinformationThreshold: number;
  learningElasticity: number;
}

/**
 * Default baseline values for Education.
 */
export const DefaultEducationBaseline: EducationBaseline = {
  baselineLiteracy: 0.8,
  baselineNumeracy: 0.75,
  baselineLearningCapacity: 0.7,
  baselineEpistemicStability: 0.85,
};

/**
 * Default rules for Education behavior.
 */
export const DefaultEducationRules: EducationRules = {
  literacyFloor: 0.6,
  numeracyFloor: 0.55,
  misinformationThreshold: 0.2,
  learningElasticity: 0.7,
};
