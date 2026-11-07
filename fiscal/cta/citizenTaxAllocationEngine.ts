/**
 * Citizen Tax Allocation (CTA) is a native PANoRAMic.os fiscal subsystem.
 * It calculates a governed distribution of collected citizen-tax revenue.
 * It does not mint PAR, debit wallets, or post ledger entries itself.
 */
export interface CtaPoolShares {
  humanitarianShare: number
  stewardshipShare: number
}

export interface CtaAllocationInput {
  collectedCitizenTaxRevenue: number
  shares: CtaPoolShares
}

export interface CtaAllocationResult {
  collectedCitizenTaxRevenue: number
  humanitarianAllocation: number
  stewardshipAllocation: number
  allocatedTotal: number
  unallocatedRemainder: number
}

export function validateCtaPoolShares(shares: CtaPoolShares): void {
  const { humanitarianShare, stewardshipShare } = shares
  if (!Number.isFinite(humanitarianShare) || !Number.isFinite(stewardshipShare) ||
      humanitarianShare < 0 || stewardshipShare < 0 ||
      Math.abs(humanitarianShare + stewardshipShare - 1) > 1e-12) {
    throw new RangeError("CTA pool shares must be finite, non-negative, and sum to 1.")
  }
}

export function runCitizenTaxAllocationEngine(input: CtaAllocationInput): CtaAllocationResult {
  const { collectedCitizenTaxRevenue, shares } = input
  if (!Number.isFinite(collectedCitizenTaxRevenue) || collectedCitizenTaxRevenue < 0)
    throw new RangeError("collectedCitizenTaxRevenue must be finite and non-negative.")
  validateCtaPoolShares(shares)
  const humanitarianAllocation = collectedCitizenTaxRevenue * shares.humanitarianShare
  const stewardshipAllocation = collectedCitizenTaxRevenue * shares.stewardshipShare
  const allocatedTotal = humanitarianAllocation + stewardshipAllocation
  return {
    collectedCitizenTaxRevenue, humanitarianAllocation, stewardshipAllocation,
    allocatedTotal,
    unallocatedRemainder: collectedCitizenTaxRevenue - allocatedTotal,
  }
}
