import { ParPoolShares, validatePoolShares } from "../../pillars/par/PAR_POLICY"

export interface ParDemurrageInput {
  openingBalance: number
  /** Completed cycles; zero means no demurrage cycle has elapsed. */
  cyclesElapsed: number
  /** Initial fraction of openingBalance reverted in cycle one. */
  /** Initial fraction of the eligible opening balance reverted in cycle one. */
  initialRatePerCycle: number
  /** Compounding growth applied to the cumulative percentage each cycle. */
  compoundingFactor: number
  shares: ParPoolShares
  /**
   * Protected personal dignity reserve supplied by the identity-aware policy
   * layer after aggregating the holder's eligible reserve across wallets.
   * Defaults to zero for backwards compatibility; production callers must
   * supply the independently calculated protected floor.
   */
  protectedBalanceFloor?: number
}
export interface ParDemurrageResult {
  cumulativeDemurrageRate: number
  previousCumulativeDemurrageRate: number
  eligibleOpeningBalance: number
  protectedBalanceFloor: number
  demurrageThisCycle: number
  totalDemurrageToDate: number
  retainedBalance: number
  humanitarianAllocation: number
  stewardshipAllocation: number
  totalPoolAllocation: number
  fullyReverted: boolean
}

/**
 * Cumulative percentage compounds against the eligible opening balance:
 * E=max(0, openingBalance-protectedBalanceFloor)
 * R(n)=min(1, initialRate*(1+factor)^(n-1)); R(0)=0.
 * Charge only the incremental difference R(n)-R(n-1), preventing duplicates.
 * The 100% cap applies only to E; the protected floor is never chargeable.
 */
export function runParDemurrageEngine(input: ParDemurrageInput): ParDemurrageResult {
  const {
    openingBalance, cyclesElapsed, initialRatePerCycle, compoundingFactor, shares,
    protectedBalanceFloor = 0,
  } = input
  if (!Number.isFinite(openingBalance) || openingBalance < 0)
    throw new RangeError("openingBalance must be finite and non-negative.")
 * Cumulative percentage compounds against the eligible opening balance:
 * E=max(0, openingBalance-protectedBalanceFloor)
 * R(n)=min(1, initialRate*(1+factor)^(n-1)); R(0)=0.
 * Charge only the incremental difference R(n)-R(n-1), preventing duplicates.
 * The 100% cap applies only to E; the protected floor is never chargeable.
 */
export function runParDemurrageEngine(input: ParDemurrageInput): ParDemurrageResult {
  const {
    openingBalance, cyclesElapsed, initialRatePerCycle, compoundingFactor, shares,
    protectedBalanceFloor = 0,
  } = input
  if (!Number.isFinite(openingBalance) || openingBalance < 0)
    throw new RangeError("openingBalance must be finite and non-negative.")
  if (!Number.isFinite(protectedBalanceFloor) || protectedBalanceFloor < 0 ||
      protectedBalanceFloor > openingBalance)
    throw new RangeError("protectedBalanceFloor must be finite and within [0, openingBalance].")
  if (!Number.isSafeInteger(cyclesElapsed) || cyclesElapsed < 0)
    throw new RangeError("cyclesElapsed must be a non-negative safe integer.")
  if (!Number.isFinite(initialRatePerCycle) || initialRatePerCycle <= 0 || initialRatePerCycle > 1)
    throw new RangeError("initialRatePerCycle must be finite and in (0, 1].")
  if (!Number.isFinite(compoundingFactor) || compoundingFactor < 0)
    throw new RangeError("compoundingFactor must be finite and non-negative.")
  validatePoolShares(shares)

  const eligibleOpeningBalance = Math.max(0, openingBalance - protectedBalanceFloor)
  const rateAt = (cycle: number): number => cycle <= 0 ? 0 :
    Math.min(1, initialRatePerCycle * Math.pow(1 + compoundingFactor, cycle - 1))
  const cumulativeDemurrageRate = rateAt(cyclesElapsed)
  const previousCumulativeDemurrageRate = rateAt(cyclesElapsed - 1)
  const demurrageThisCycle = eligibleOpeningBalance *
    Math.max(0, cumulativeDemurrageRate - previousCumulativeDemurrageRate)
  const totalDemurrageToDate = eligibleOpeningBalance * cumulativeDemurrageRate
  const retainedBalance = Math.max(protectedBalanceFloor, openingBalance - totalDemurrageToDate)
  const humanitarianAllocation = demurrageThisCycle * shares.humanitarianShare
  const stewardshipAllocation = demurrageThisCycle * shares.stewardshipShare
  return {
    cumulativeDemurrageRate, previousCumulativeDemurrageRate, eligibleOpeningBalance,
    protectedBalanceFloor, demurrageThisCycle, totalDemurrageToDate, retainedBalance,
    humanitarianAllocation, stewardshipAllocation,
    totalPoolAllocation: humanitarianAllocation + stewardshipAllocation,
    fullyReverted: cumulativeDemurrageRate >= 1,
  const demurrageThisCycle = eligibleOpeningBalance *
    Math.max(0, cumulativeDemurrageRate - previousCumulativeDemurrageRate)
  const totalDemurrageToDate = eligibleOpeningBalance * cumulativeDemurrageRate
  const retainedBalance = Math.max(protectedBalanceFloor, openingBalance - totalDemurrageToDate)
  const humanitarianAllocation = demurrageThisCycle * shares.humanitarianShare
  const stewardshipAllocation = demurrageThisCycle * shares.stewardshipShare
  return {
    cumulativeDemurrageRate, previousCumulativeDemurrageRate, eligibleOpeningBalance,
    protectedBalanceFloor, demurrageThisCycle, totalDemurrageToDate, retainedBalance,
    humanitarianAllocation, stewardshipAllocation,
    totalPoolAllocation: humanitarianAllocation + stewardshipAllocation,
    fullyReverted: eligibleOpeningBalance > 0 && cumulativeDemurrageRate >= 1,
  }
}
