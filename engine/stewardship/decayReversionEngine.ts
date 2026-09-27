// engine/stewardship/decayReversionEngine.ts

export interface StewardshipDecayProfile {
  id: string
  name: string

  // Activity / time
  isActive: boolean
  lastActiveTick: number

  // Capital / presence
  totalCapitalIndex: number          // 0–1 normalized capital presence
  decaySensitivityIndex: number      // 0–1: how quickly this entity should decay when inactive

  // Optional tags
  sector?: string
  region?: string
}

export interface StewardshipDecayConfig {
  currentTick: number
  inactivityThresholdTicks: number   // ticks of inactivity before decay starts
  maxDecayRatePerTick: number        // cap on decay per tick (0–1 of capital index)
  humanitarianShare: number          // fraction of decayed capital → humanitarian pool (e.g. 0.6)
  stewardshipShare: number           // fraction → stewardship fund (e.g. 0.4)
}

export interface StewardshipDecayResult {
  totalDecayedCapitalIndex: number
  humanitarianPoolIndex: number
  stewardshipFundIndex: number
  retainedCapitalByEntity: Record<string, number>
}

/**
 * Decay Reversion Engine
 *
 * - Only decays inactive / stagnant entities
 * - Does NOT touch PAR balances
 * - Routes decayed capital into:
 *   - Humanitarian Infrastructure Pool
 *   - Stewardship Fund (dignity floor backing)
 */
export function runDecayReversionEngine(
  profiles: StewardshipDecayProfile[],
  config: StewardshipDecayConfig
): StewardshipDecayResult {
  let totalDecayedCapitalIndex = 0
  const retainedCapitalByEntity: Record<string, number> = {}

  for (const profile of profiles) {
    const inactiveTicks = config.currentTick - profile.lastActiveTick
    const shouldDecay =
      !profile.isActive && inactiveTicks >= config.inactivityThresholdTicks

    if (!shouldDecay) {
      retainedCapitalByEntity[profile.id] = profile.totalCapitalIndex
      continue
    }

    // Inactivity factor ramps up over time, capped at 1
    const inactivityFactor = Math.min(
      1,
      inactiveTicks / (config.inactivityThresholdTicks * 4)
    )

    // Raw decay rate based on sensitivity, inactivity, and global cap
    const rawDecayRate =
      profile.decaySensitivityIndex *
      inactivityFactor *
      config.maxDecayRatePerTick

    const decayAmount = Math.min(profile.totalCapitalIndex, rawDecayRate)
    const retained = profile.totalCapitalIndex - decayAmount

    retainedCapitalByEntity[profile.id] = retained
    totalDecayedCapitalIndex += decayAmount
  }

  const humanitarianPoolIndex =
    totalDecayedCapitalIndex * config.humanitarianShare
  const stewardshipFundIndex =
    totalDecayedCapitalIndex * config.stewardshipShare

  return {
    totalDecayedCapitalIndex,
    humanitarianPoolIndex,
    stewardshipFundIndex,
    retainedCapitalByEntity,
  }
}
