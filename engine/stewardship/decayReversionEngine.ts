// engine/stewardship/decayReversionEngine.ts

export interface EntityCapitalProfile {
  id: string
  name: string
  isActive: boolean
  lastActiveTick: number
  totalCapital: number          // normalized 0–1 representation of capital
  decaySensitivityIndex: number // 0–1: how quickly this entity should decay when inactive
}

export interface DecayReversionResult {
  totalDecayedCapital: number
  humanitarianPoolAllocation: number
  stewardshipFundAllocation: number
  retainedCapitalByEntity: Record<string, number>
}

interface DecayReversionConfig {
  currentTick: number
  inactivityThresholdTicks: number // after this many ticks, decay begins
  humanitarianShare: number        // e.g. 0.6 → 60% to humanitarian pool
  stewardshipShare: number         // e.g. 0.4 → 40% to stewardship fund
  maxDecayRatePerTick: number      // cap on how fast capital can decay per tick
}

export function runDecayReversionEngine(
  entities: EntityCapitalProfile[],
  config: DecayReversionConfig
): DecayReversionResult {
  let totalDecayedCapital = 0
  const retainedCapitalByEntity: Record<string, number> = {}

  for (const entity of entities) {
    const inactiveTicks = config.currentTick - entity.lastActiveTick
    const shouldDecay = !entity.isActive && inactiveTicks >= config.inactivityThresholdTicks

    if (!shouldDecay) {
      retainedCapitalByEntity[entity.id] = entity.totalCapital
      continue
    }

    // Decay rate scales with inactivity and sensitivity, capped by maxDecayRatePerTick
    const inactivityFactor = Math.min(1, inactiveTicks / (config.inactivityThresholdTicks * 4))
    const rawDecayRate =
      entity.decaySensitivityIndex * inactivityFactor * config.maxDecayRatePerTick

    const decayAmount = Math.min(entity.totalCapital, rawDecayRate)

    const retained = entity.totalCapital - decayAmount
    retainedCapitalByEntity[entity.id] = retained
    totalDecayedCapital += decayAmount
  }

  const humanitarianPoolAllocation = totalDecayedCapital * config.humanitarianShare
  const stewardshipFundAllocation = totalDecayedCapital * config.stewardshipShare

  return {
    totalDecayedCapital,
    humanitarianPoolAllocation,
    stewardshipFundAllocation,
    retainedCapitalByEntity,
  }
}
