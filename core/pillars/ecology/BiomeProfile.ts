// core/pillars/ecology/BiomeProfile.ts

export interface BiomeProfile {
  name: string
  biomeType: 
    | "forest"
    | "ocean"
    | "wetland"
    | "grassland"
    | "desert"
    | "tundra"
    | "reef"
    | "freshwater"
    | "urban"
    | "agricultural"

  // Core ecological metrics
  healthIndex: number              // 0–1
  regenerationRate: number         // 0–1
  degradationRate: number          // 0–1
  biodiversityIndex: number        // 0–1
  pollutionLoad: number            // 0–1
  climateStabilityIndex: number    // 0–1

  // Resource metrics
  resourceRenewalRate: number      // 0–1
  resourceExtractionPressure: number // 0–1

  // Human impact metrics
  humanFootprintIndex: number      // 0–1
  infrastructureIntrusionIndex: number // 0–1

  // Risk metrics
  ecologicalRiskIndex: number      // 0–1
  collapseRiskIndex: number        // 0–1
}

export function evaluateBiomeHealth(biome: BiomeProfile) {
  // Base health
  let healthScore =
    biome.healthIndex * 40 +
    biome.regenerationRate * 30 +
    biome.biodiversityIndex * 30

  // Penalties
  healthScore -= biome.degradationRate * 30
  healthScore -= biome.pollutionLoad * 25
  healthScore -= (1 - biome.climateStabilityIndex) * 25
  healthScore -= biome.resourceExtractionPressure * 20
  healthScore -= biome.humanFootprintIndex * 20
  healthScore -= biome.infrastructureIntrusionIndex * 15

  // Normalize
  healthScore = Math.max(0, Math.min(healthScore, 100))

  let mode = "stable"
  if (healthScore < 40) mode = "critical"
  else if (healthScore < 70) mode = "unstable"

  return {
    healthScore,
    mode,
  }
}