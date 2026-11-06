import {
  PAR_TRANSACTION_FEE_RATE, ParPoolShares, validatePoolShares,
} from "../../pillars/par/PAR_POLICY"

export interface ParFeeAllocationInput {
  transactionValue: number
  shares: ParPoolShares
  feeRate?: number
}
export interface ParFeeAllocationResult {
  feeRate: number
  feeAmount: number
  humanitarianAllocation: number
  stewardshipAllocation: number
  allocatedTotal: number
}

/** Routes the 0.02% default PAR micro-levy across the two configured pools. */
export function runParFeeAllocationEngine(input: ParFeeAllocationInput): ParFeeAllocationResult {
  const feeRate = input.feeRate ?? PAR_TRANSACTION_FEE_RATE
  if (!Number.isFinite(input.transactionValue) || input.transactionValue < 0)
    throw new RangeError("transactionValue must be finite and non-negative.")
  if (!Number.isFinite(feeRate) || feeRate < 0 || feeRate > 1)
    throw new RangeError("feeRate must be finite and within [0, 1].")
  validatePoolShares(input.shares)
  const feeAmount = input.transactionValue * feeRate
  const humanitarianAllocation = feeAmount * input.shares.humanitarianShare
  const stewardshipAllocation = feeAmount * input.shares.stewardshipShare
  return {
    feeRate, feeAmount, humanitarianAllocation, stewardshipAllocation,
    allocatedTotal: humanitarianAllocation + stewardshipAllocation,
  }
}
