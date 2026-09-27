// engine/ecology/EcologySynthesisEngine.ts

import { BiomeProfile } from "../../core/pillars/ecology/BiomeProfile"
import { computeEcologyRisk } from "./EcologyRiskEngine"
import { computeEcologyStability } from "./EcologyStabilityEngine"

export function computeEcologySynthesis(biome: BiomeProfile) {
  const risk = computeEcologyRisk(biome)
  const stability = computeEcologyStability(biome)

  // Additional synthesis indicators
  const regenerationFactor = biome.regenerationRate * 30
  const biodiversityFactor = biome.biodiversityIndex * 30
  const climateFactor = biome.climateStabilityIndex * 30

  const degradationPenalty = biome.degradationRate * 30
  const pollutionPenalty = biome.pollutionLoad * 25
  const extractionPenalty = biome.resourceExtractionPressure * 25
  const humanFootprintPenalty = biome.humanFootprintIndex * 20
  const infrastructurePenalty = biome.infrastructureIntrusionIndex * 20

  // Synthesis score combines:
  // - stability
  // - inverse risk
  // - regeneration
  // - biodiversity
  // - climate stability
  // - penalties for degradation, pollution, extraction, footprint, intrusion

  let synthesisScore =
    stability.stabilityScore * 0.4 +
    (100 - risk.riskScore) * 0.3 +
    regenerationFactor +
    biodiversityFactor +
    climateFactor -
    degradationPenalty -
    pollutionPenalty -
    extractionPenalty -
    humanFootprintPenalty -
    infrastructurePenalty

  // Normalize
  synthesisScore = Math.max(0, Math.min(synthesisScore, 100))

  let synthesisMode = "stable"
  if (synthesisScore < 40) synthesisMode = "critical"
  else if (synthesisScore < 70) synthesisMode = "unstable"

  return {
    synthesisScore,
    synthesisMode,
    breakdown: {
      stabilityScore: stability.stabilityScore,
      riskScore: risk.riskScore,
      regenerationFactor,
      biodiversityFactor,
      climateFactor,
      degradationPenalty,
      pollutionPenalty,
      extractionPenalty,
      humanFootprintPenalty,
      infrastructurePenalty,
    },
  }
}