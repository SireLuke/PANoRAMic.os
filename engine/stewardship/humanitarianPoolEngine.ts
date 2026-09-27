// engine/stewardship/humanitarianPoolEngine.ts

export interface HumanitarianPoolProfile {
  currentPoolIndex: number        // total backing for humanitarian megaprojects (0–1 normalized)
  ecologyStressIndex: number      // ecological strain (0–1)
  infrastructureNeedIndex: number // infrastructure demand (0–1)
  commonsRestorationIndex: number // need for commons regeneration (0–1)
}

export interface HumanitarianPoolInput {
  humanitarianPoolIndex: number   // incoming allocation from decay reversion
}

export interface HumanitarianPoolResult {
  updatedPoolIndex: number
  ecologyRestorationBoost: number
  infrastructureBoost: number
  commonsBoost: number
}

/**
 * Humanitarian Pool Engine
 *
 * - Receives humanitarianPoolIndex from decay reversion
 * - Funds global megaprojects (desalination, solar belts, recycling grids)
 * - Boosts ecology, infrastructure, and commons pillars
 * - Does NOT use PAR
 * - Does NOT extract from citizens
 */
export function runHumanitarianPoolEngine(
  profile: HumanitarianPoolProfile,
  input: HumanitarianPoolInput
): HumanitarianPoolResult {
  const {
    currentPoolIndex,
    ecologyStressIndex,
    infrastructureNeedIndex,
    commonsRestorationIndex,
  } = profile

  // Add new backing from decay reversion
  const updatedPoolIndex = Math.min(1, currentPoolIndex + input.humanitarianPoolIndex)

  // Ecology restoration grows with pool strength + stress level
  const ecologyRestorationBoost =
    updatedPoolIndex * 0.7 * (1 - ecologyStressIndex)

  // Infrastructure gets a strong boost from humanitarian pool
  const infrastructureBoost =
    updatedPoolIndex * 0.6 * (1 + infrastructureNeedIndex)

  // Commons regeneration benefits from pool strength + restoration need
  const commonsBoost =
    updatedPoolIndex * 0.5 * (1 + commonsRestorationIndex)

  return {
    updatedPoolIndex,
    ecologyRestorationBoost,
    infrastructureBoost,
    commonsBoost,
  }
}
