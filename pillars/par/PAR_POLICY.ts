/** Canonical PAR policy constants and UBE outcome domains. */
export const PAR_TRANSACTION_FEE_RATE = 0.0002 // 0.02%

export interface ParPoolShares {
  humanitarianShare: number
  stewardshipShare: number
}

export const UBE_DOMAINS = [
  "healthcare", "housing", "nutrition", "water_sanitation",
  "energy", "education", "mobility", "connectivity",
] as const
export type UbeDomain = (typeof UBE_DOMAINS)[number]
export type UbeCoverage = Record<UbeDomain, number>

export function validatePoolShares(shares: ParPoolShares): void {
  const { humanitarianShare, stewardshipShare } = shares
  if (!Number.isFinite(humanitarianShare) || !Number.isFinite(stewardshipShare) ||
      humanitarianShare < 0 || stewardshipShare < 0 ||
      Math.abs(humanitarianShare + stewardshipShare - 1) > 1e-12) {
    throw new RangeError("Pool shares must be finite, non-negative, and sum to 1.")
  }
}

export function validateCoverage(coverage: UbeCoverage): void {
  for (const domain of UBE_DOMAINS) {
    const value = coverage[domain]
    if (!Number.isFinite(value) || value < 0 || value > 1) {
      throw new RangeError("UBE coverage for " + domain + " must be normalized to [0, 1].")
    }
  }
}
