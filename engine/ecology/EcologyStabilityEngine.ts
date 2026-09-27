// engine/ecology/EcologyStabilityEngine.ts

import { BiomeProfile } from "../../core/pillars/ecology/BiomeProfile"
import { computeEcologyRisk } from "./EcologyRiskEngine"

export function computeEcologyStability(biome: BiomeProfile) {
  const risk = computeEcologyRisk(biome)

  // Stability factors
  const regenerationFactor = biome.regenerationRate * 40
  const biodiversityFactor = biome.biodiversityIndex * 35
  const climateFactor = biome.climateStabilityIndex * 35

  // Penalties
  const degradationPenalty = biome.degradationRate * 35
  const pollutionPenalty = biome.pollutionLoad * 30
  const extractionPenalty = biome.resourceExtractionPressure * 25
  const humanFootprintPenalty = biome.humanFootprintIndex * 25
  const infrastructurePenalty = biome.infrastructureIntrusionIndex * 20

  let stabilityScore =
    regenerationFactor +
    biodiversityFactor +
    climateFactor -
    degradationPenalty -
    pollutionPenalty -
    extractionPenalty -
    humanFootprintPenalty -
    infrastructurePenalty -
    risk.collapseRisk * 20

  // Normalize
  stabilityScore = Math.max(0, Math.min(stabilityScore, 100))

  let stabilityMode = "stable"
  if (stabilityScore < 40) stabilityMode = "critical"
  else if (stabilityScore < 70) stabilityMode = "unstable"

  return {
    stabilityScore,
    stabilityMode,
    breakdown: {
      regenerationFactor,
      biodiversityFactor,
      climateFactor,
      degradationPenalty,
      pollutionPenalty,
      extractionPenalty,
      humanFootprintPenalty,
      infrastructurePenalty,
      collapseRisk: risk.collapseRisk,
    },
  }
}