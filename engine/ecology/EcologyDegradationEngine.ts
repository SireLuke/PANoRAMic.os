// engine/ecology/EcologyDegradationEngine.ts

import { BiomeProfile } from "../../core/pillars/ecology/BiomeProfile"

export function applyEcologyDegradation(biome: BiomeProfile) {
  const actions: string[] = []

  let {
    degradationRate,
    biodiversityIndex,
    pollutionLoad,
    climateStabilityIndex,
    resourceRenewalRate,
    humanFootprintIndex,
    infrastructureIntrusionIndex,
  } = biome

  // Natural degradation
  actions.push("Applying natural degradation.")
  degradationRate *= 1.05

  // Pollution increase
  actions.push("Increasing pollution load.")
  pollutionLoad *= 1.1

  // Biodiversity loss
  if (biodiversityIndex > 0.3) {
    actions.push("Biodiversity loss occurring.")
    biodiversityIndex -= 0.05
  }

  // Climate destabilization
  if (climateStabilityIndex > 0.4) {
    actions.push("Climate destabilization increasing.")
    climateStabilityIndex -= 0.05
  }

  // Resource depletion
  actions.push("Resource renewal rate decreasing due to extraction pressure.")
  resourceRenewalRate *= 0.9

  // Human footprint escalation
  actions.push("Human footprint increasing.")
  humanFootprintIndex *= 1.1

  // Infrastructure intrusion damage
  actions.push("Infrastructure intrusion causing ecological stress.")
  infrastructureIntrusionIndex *= 1.1

  // Normalize
  degradationRate = Math.max(0, Math.min(degradationRate, 1))
  biodiversityIndex = Math.max(0, Math.min(biodiversityIndex, 1))
  pollutionLoad = Math.max(0, Math.min(pollutionLoad, 1))
  climateStabilityIndex = Math.max(0, Math.min(climateStabilityIndex, 1))
  resourceRenewalRate = Math.max(0, Math.min(resourceRenewalRate, 1))
  humanFootprintIndex = Math.max(0, Math.min(humanFootprintIndex, 1))
  infrastructureIntrusionIndex = Math.max(0, Math.min(infrastructureIntrusionIndex, 1))

  // Update biome
  biome.degradationRate = degradationRate
  biome.biodiversityIndex = biodiversityIndex
  biome.pollutionLoad = pollutionLoad
  biome.climateStabilityIndex = climateStabilityIndex
  biome.resourceRenewalRate = resourceRenewalRate
  biome.humanFootprintIndex = humanFootprintIndex
  biome.infrastructureIntrusionIndex = infrastructureIntrusionIndex

  return {
    actions,
    updatedBiome: biome,
    degradationRate,
    biodiversityIndex,
    pollutionLoad,
    climateStabilityIndex,
    resourceRenewalRate,
    humanFootprintIndex,
    infrastructureIntrusionIndex,
  }
}