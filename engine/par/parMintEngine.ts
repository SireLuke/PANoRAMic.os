// engine/par/PARMintEngine.ts

export interface PARMintProfile {
  renewableBackingIndex: number      // 0–1: ecological + renewable capacity
  globalDignityIndex: number         // 0–1: rights + autonomy + safety stability
  adoptionIndex: number              // 0–1: how many participants are active
  currentSupplyIndex: number         // 0–1 normalized PAR supply
}

export interface PARMintResult {
  mintedPARIndex: number             // new PAR created this tick
  updatedSupplyIndex: number         // new total supply
}

/**
 * PAR Mint Engine
 *
 * - Mints new PAR based on renewable backing, dignity stability, and adoption rate
 * - Does NOT dilute existing holders
 * - Does NOT extract from citizens
 * - Supply expands only when the world is stable enough to support it
 */
export function runPARMintEngine(
  profile: PARMintProfile
): PARMintResult {
  const {
    renewableBackingIndex,
    globalDignityIndex,
    adoptionIndex,
    currentSupplyIndex,
  } = profile

  // Minting capacity is driven by renewable + dignity
  const baseCapacity =
    renewableBackingIndex * 0.6 +
    globalDignityIndex * 0.4

  // Adoption determines how much of that capacity activates
  const activationFactor = adoptionIndex

  // Mint amount (normalized)
  const mintedPARIndex = baseCapacity * activationFactor * 0.1

  // Update supply, capped at 1
  const updatedSupplyIndex = Math.min(
    1,
    currentSupplyIndex + mintedPARIndex
  )

  return {
    mintedPARIndex,
    updatedSupplyIndex,
  }
}
