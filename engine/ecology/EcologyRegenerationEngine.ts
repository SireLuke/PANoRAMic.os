// engine/ecology/EcologyRegenerationEngine.ts

import { BiomeProfile } from "../../core/pillars/ecology/BiomeProfile"

export function applyEcologyRegeneration(biome: BiomeProfile) {
  const actions: string[] = []

  let {
    regenerationRate,
    biodiversityIndex,
    pollutionLoad,
    climateStabilityIndex,
    resourceRenewalRate,
  } = biome

  // Natural regeneration
  actions.push("Applying natural regeneration.")
  regenerationRate *= 1.05

  // Biodiversity restoration
  if (biodiversityIndex < 0.6) {
    actions.push("Low biodiversity — boosting biodiversity restoration.")
    biodiversityIndex += 0.1
  }

  // Pollution reduction
  if (pollutionLoad > 0.4) {
    actions.push("High pollution — reducing pollution load.")
    pollutionLoad *= 0.85
  }

  // Climate stabilization
  if (climateStabilityIndex < 0.7) {
    actions.push("Climate instability — boosting climate stabilization.")
    climateStabilityIndex += 0.08
  }

  // Resource renewal
  actions.push("Boosting resource renewal rate.")
  resourceRenewalRate *= 1.1

  // Normalize
  regenerationRate = Math.max(0, Math.min(regenerationRate, 1))
  biodiversityIndex = Math.max(0, Math.min(biodiversityIndex, 1))
  pollutionLoad = Math.max(0, Math.min(pollutionLoad, 1))
  climateStabilityIndex = Math.max(0, Math.min(climateStabilityIndex, 1))
  resourceRenewalRate = Math.max(0, Math.min(resourceRenewalRate, 1))

  // Update biome
  biome.regenerationRate = regenerationRate
  biome.biodiversityIndex = biodiversityIndex
  biome.pollutionLoad = pollutionLoad
  biome.climateStabilityIndex = climateStabilityIndex
  biome.resourceRenewalRate = resourceRenewalRate

  return {
    actions,
    updatedBiome: biome,
    regenerationRate,
    biodiversityIndex,
    pollutionLoad,
    climateStabilityIndex,
    resourceRenewalRate,
  }
}