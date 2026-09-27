// engine/ecology/EcologyFlowEngine.ts

import { BiomeProfile } from "../../core/pillars/ecology/BiomeProfile"

export function computeEcologyFlow(biome: BiomeProfile) {
  const actions: string[] = []

  let {
    regenerationRate,
    degradationRate,
    pollutionLoad,
    biodiversityIndex,
    climateStabilityIndex,
    humanFootprintIndex,
    infrastructureIntrusionIndex,
  } = biome

  // Regeneration boost
  if (biodiversityIndex > 0.7) {
    actions.push("High biodiversity — boosting regeneration.")
    regenerationRate *= 1.15
  }

  // Climate stability boost
  if (climateStabilityIndex > 0.7) {
    actions.push("Stable climate — boosting regeneration.")
    regenerationRate *= 1.1
  }

  // Pollution penalty
  if (pollutionLoad > 0.5) {
    actions.push("High pollution — increasing degradation.")
    degradationRate *= 1.2
  }

  // Human footprint penalty
  if (humanFootprintIndex > 0.6) {
    actions.push("High human footprint — increasing degradation.")
    degradationRate *= 1.15
  }

  // Infrastructure intrusion penalty
  if (infrastructureIntrusionIndex > 0.6) {
    actions.push("Infrastructure intrusion — increasing degradation.")
    degradationRate *= 1.1
  }

  // Collapse triggers
  const collapseRisk =
    pollutionLoad * 0.3 +
    humanFootprintIndex * 0.3 +
    infrastructureIntrusionIndex * 0.2 +
    (1 - climateStabilityIndex) * 0.2

  if (collapseRisk > 0.7) {
    actions.push("Ecological collapse risk — boosting regeneration and reducing degradation.")
    regenerationRate *= 1.2
    degradationRate *= 0.85
  }

  // Normalize
  regenerationRate = Math.max(0, Math.min(regenerationRate, 1))
  degradationRate = Math.max(0, Math.min(degradationRate, 1))

  // Update biome
  biome.regenerationRate = regenerationRate
  biome.degradationRate = degradationRate

  return {
    actions,
    updatedBiome: biome,
    regenerationRate,
    degradationRate,
    collapseRisk,
  }
}