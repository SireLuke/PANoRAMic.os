import { ParPoolShares, validatePoolShares } from "../../pillars/par/PAR_POLICY"

export interface ParDemurrageInput {
  openingBalance: number
  /** Completed cycles; zero means no demurrage cycle has elapsed. */
  cyclesElapsed: number
  /** Initial fraction of openingBalance reverted in cycle one. */
  initialRatePerCycle: number
  /** Compounding growth applied to the cumulative percentage each cycle. */
  compoundingFactor: number
  shares: ParPoolShares
}
export interface ParDemurrageResult {
  cumulativeDemurrageRate: number
  previousCumulativeDemurrageRate: number
  demurrageThisCycle: number
  totalDemurrageToDate: number
  retainedBalance: number
  humanitarianAllocation: number
  stewardshipAllocation: number
  totalPoolAllocation: number
  fullyReverted: boolean
}

/**
 * Cumulative percentage compounds against the original opening balance:
 * R(n)=min(1, initialRate*(1+factor)^(n-1)); R(0)=0.
 * Charge only the incremental difference R(n)-R(n-1), preventing duplicates.
 * The 100% cap ensures total reversion never exceeds the opening balance.
 */
export function runParDemurrageEngine(input: ParDemurrageInput): ParDemurrageResult {
  const { openingBalance, cyclesElapsed, initialRatePerCycle, compoundingFactor, shares } = input
  if (!Number.isFinite(openingBalance) || openingBalance < 0)
    throw new RangeError("openingBalance must be finite and non-negative.")
  if (!Number.isSafeInteger(cyclesElapsed) || cyclesElapsed < 0)
    throw new RangeError("cyclesElapsed must be a non-negative safe integer.")
  if (!Number.isFinite(initialRatePerCycle) || initialRatePerCycle <= 0 || initialRatePerCycle > 1)
    throw new RangeError("initialRatePerCycle must be finite and in (0, 1].")
  if (!Number.isFinite(compoundingFactor) || compoundingFactor < 0)
    throw new RangeError("compoundingFactor must be finite and non-negative.")
  validatePoolShares(shares)

  const rateAt = (cycle: number): number => cycle <= 0 ? 0 :
    Math.min(1, initialRatePerCycle * Math.pow(1 + compoundingFactor, cycle - 1))
  const cumulativeDemurrageRate = rateAt(cyclesElapsed)
  const previousCumulativeDemurrageRate = rateAt(cyclesElapsed - 1)
  const demurrageThisCycle = openingBalance *
    Math.max(0, cumulativeDemurrageRate - previousCumulativeDemurrageRate)
  const totalDemurrageToDate = openingBalance * cumulativeDemurrageRate
  const retainedBalance = Math.max(0, openingBalance - totalDemurrageToDate)
  const humanitarianAllocation = demurrageThisCycle * shares.humanitarianShare
  const stewardshipAllocation = demurrageThisCycle * shares.stewardshipShare
  return {
    cumulativeDemurrageRate, previousCumulativeDemurrageRate, demurrageThisCycle,
    totalDemurrageToDate, retainedBalance, humanitarianAllocation, stewardshipAllocation,
    totalPoolAllocation: humanitarianAllocation + stewardshipAllocation,
    fullyReverted: cumulativeDemurrageRate >= 1,
  }
}
