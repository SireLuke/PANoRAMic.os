// engine/stewardship/stewardshipFundEngine.ts

export interface StewardshipFundProfile {
  currentFundIndex: number        // total backing for dignity floor (0–1 normalized)
  dignityDemandIndex: number      // global demand for baseline guarantees (0–1)
  rightsStabilityIndex: number    // how stable rights are globally (0–1)
  populationPressureIndex: number // how much strain population puts on the floor (0–1)
}

export interface StewardshipFundInput {
  stewardshipFundIndex: number    // incoming allocation from decay reversion
}

export interface StewardshipFundResult {
  updatedFundIndex: number
  dignityFloorStrength: number
  rightsBoost: number
  populationRelief: number
}

/**
 * Stewardship Fund Engine
 *
 * - Receives stewardshipFundIndex from decay reversion
 * - Strengthens the dignity floor
 * - Stabilizes rights
 * - Reduces population pressure
 * - Does NOT use PAR
 * - Does NOT extract from citizens
 */
export function runStewardshipFundEngine(
  profile: StewardshipFundProfile,
  input: StewardshipFundInput
): StewardshipFundResult {
  const { currentFundIndex, dignityDemandIndex, rightsStabilityIndex, populationPressureIndex } =
    profile

  // Add new backing from decay reversion
  const updatedFundIndex = Math.min(1, currentFundIndex + input.stewardshipFundIndex)

  // Dignity floor strength grows with fund + demand
  const dignityFloorStrength =
    updatedFundIndex * 0.6 + dignityDemandIndex * 0.4

  // Rights stability gets a boost from fund strength
  const rightsBoost =
    updatedFundIndex * 0.5 + rightsStabilityIndex * 0.5

  // Population pressure is relieved by stronger fund
  const populationRelief =
    updatedFundIndex * (1 - populationPressureIndex)

  return {
    updatedFundIndex,
    dignityFloorStrength,
    rightsBoost,
    populationRelief,
  }
}
