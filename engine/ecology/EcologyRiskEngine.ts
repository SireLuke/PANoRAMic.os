// engine/ecology/EcologyRiskEngine.ts

import { BiomeProfile } from "../../core/pillars/ecology/BiomeProfile"

export function computeEcologyRisk(biome: BiomeProfile) {
  // Risk factors
  const pollutionRisk = biome.pollutionLoad * 40
  const biodiversityRisk = (1 - biome.biodiversityIndex) * 35
  const climateRisk = (1 - biome.climateStabilityIndex) * 35
  const extractionRisk = biome.resourceExtractionPressure * 30
  const humanFootprintRisk = biome.humanFootprintIndex * 30
  const infrastructureRisk = biome.infrastructureIntrusionIndex * 25
  const degradationRisk = biome.degradationRate * 30

  // Collapse risk synthesis
  const collapseRisk =
    pollutionRisk * 0.2 +
    biodiversityRisk * 0.2 +
    climateRisk * 0.2 +
    extractionRisk * 0.15 +
    humanFootprintRisk * 0.15 +
    infrastructureRisk * 0.1

  let riskScore =
    pollutionRisk +
    biodiversityRisk +
    climateRisk +
    extractionRisk +
    humanFootprintRisk +
    infrastructureRisk +
    degradationRisk

  // Normalize
  riskScore = Math.max(0, Math.min(riskScore, 100))

  let riskMode = "low"
  if (riskScore >= 75) riskMode = "critical"
  else if (riskScore >= 50) riskMode = "high"
  else if (riskScore >= 25) riskMode = "moderate"

  return {
    riskScore,
    riskMode,
    collapseRisk,
    breakdown: {
      pollutionRisk,
      biodiversityRisk,
      climateRisk,
      extractionRisk,
      humanFootprintRisk,
      infrastructureRisk,
      degradationRisk,
    },
  }
}