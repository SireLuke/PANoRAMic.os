/**
 * Batch allocation of daily baseline claims and contribution-based awards
 * against one pool. Run independently for the Humanitarian/Ecological Pool
 * and the Stewardship/Dignity Pool.
 *
 * Baseline claims have priority and are allocated pro rata when underfunded.
 * Contribution awards are then allocated pro rata from the remaining balance.
 * This is a deterministic allocator, not a contribution verifier or ledger.
 */
export interface PoolClaimRequest {
  claimId: string
  baselineRequested: number
  contributionRequested: number
}

export interface PoolClaimAllocation {
  claimId: string
  baselinePaid: number
  contributionPaid: number
  baselineUnpaid: number
  contributionUnpaid: number
  totalPaid: number
}

export interface PoolClaimsResult {
  openingPoolBalance: number
  baselinePaidTotal: number
  contributionPaidTotal: number
  totalPaid: number
  closingPoolBalance: number
  allocations: PoolClaimAllocation[]
}

function validateAmount(value: number, label: string): void {
  if (!Number.isFinite(value) || value < 0)
    throw new RangeError(label + " must be finite and non-negative.")
}

function allocateProRata(requests: number[], available: number): number[] {
  const total = requests.reduce((sum, value) => sum + value, 0)
  if (total <= 0 || available <= 0) return requests.map(() => 0)
  const factor = Math.min(1, available / total)
  return requests.map(value => value * factor)
}

export function runPoolClaimsAllocationEngine(
  openingPoolBalance: number,
  requests: PoolClaimRequest[],
): PoolClaimsResult {
  validateAmount(openingPoolBalance, "openingPoolBalance")
  const ids = new Set<string>()
  for (const request of requests) {
    if (!request.claimId || ids.has(request.claimId))
      throw new TypeError("Each pool claim requires a unique non-empty claimId.")
    ids.add(request.claimId)
    validateAmount(request.baselineRequested, "baselineRequested")
    validateAmount(request.contributionRequested, "contributionRequested")
  }

  const baselinePaid = allocateProRata(
    requests.map(request => request.baselineRequested), openingPoolBalance,
  )
  const baselinePaidTotal = baselinePaid.reduce((sum, value) => sum + value, 0)
  const remainingAfterBaseline = Math.max(0, openingPoolBalance - baselinePaidTotal)
  const contributionPaid = allocateProRata(
    requests.map(request => request.contributionRequested), remainingAfterBaseline,
  )
  const contributionPaidTotal = contributionPaid.reduce((sum, value) => sum + value, 0)
  const allocations = requests.map((request, index) => ({
    claimId: request.claimId,
    baselinePaid: baselinePaid[index],
    contributionPaid: contributionPaid[index],
    baselineUnpaid: request.baselineRequested - baselinePaid[index],
    contributionUnpaid: request.contributionRequested - contributionPaid[index],
    totalPaid: baselinePaid[index] + contributionPaid[index],
  }))
  const totalPaid = baselinePaidTotal + contributionPaidTotal
  return {
    openingPoolBalance, baselinePaidTotal, contributionPaidTotal, totalPaid,
    closingPoolBalance: Math.max(0, openingPoolBalance - totalPaid),
    allocations,
  }
}
