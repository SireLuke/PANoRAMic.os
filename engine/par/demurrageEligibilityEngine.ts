/**
 * PAR small/medium-account demurrage protection and notice transition.
 *
 * This is an eligibility gate, not a wallet ledger or activity detector.
 * The caller supplies the account's verified tier and whether it met the
 * separately governed qualifying-activity rule for the relevant period.
 */
export const PAR_SMALL_MEDIUM_PROTECTION_YEARS = 5
export const PAR_DEMURRAGE_NOTICE_GRACE_YEARS = 1
export const PAR_DEMURRAGE_EFFECTIVE_YEAR =
  PAR_SMALL_MEDIUM_PROTECTION_YEARS + PAR_DEMURRAGE_NOTICE_GRACE_YEARS

export type ParDemurrageProtectionStatus =
  | "standard_schedule"
  | "protected"
  | "notice_grace"
  | "activity_maintained"
  | "demurrage_eligible"

export interface ParDemurrageEligibilityInput {
  /** Completed account age in anniversary years; may include a fractional year. */
  accountAgeYears: number
  /** Must be derived from the governed small/medium account classification. */
  qualifiesAsSmallOrMedium: boolean
  /** Supplied by the ledger's separately governed activity evaluator. */
  hasQualifyingActivity: boolean
}

export interface ParDemurrageEligibilityResult {
  status: ParDemurrageProtectionStatus
  noticeRequired: boolean
  qualifyingActivityRequired: boolean
  demurrageEligible: boolean
  protectionYearsComplete: number
  noticeGraceYears: number
  demurrageEffectiveAtAccountYear: number
}

/**
 * Five full years of protection are followed by a one-year notice/grace period.
 * At or after account year six, a qualifying small/medium account remains
 * outside demurrage while it meets the qualifying-activity rule. If it does
 * not, it becomes eligible for the existing demurrage schedule.
 *
 * This function deliberately does not define account-size thresholds,
 * transaction frequency/value thresholds, identity verification, or ledger
 * posting. Those are separate governance/integration responsibilities.
 */
export function evaluateParDemurrageEligibility(
  input: ParDemurrageEligibilityInput,
): ParDemurrageEligibilityResult {
  const { accountAgeYears, qualifiesAsSmallOrMedium, hasQualifyingActivity } = input
  if (!Number.isFinite(accountAgeYears) || accountAgeYears < 0)
    throw new RangeError("accountAgeYears must be finite and non-negative.")
  if (typeof qualifiesAsSmallOrMedium !== "boolean" ||
      typeof hasQualifyingActivity !== "boolean")
    throw new TypeError("Account tier and qualifying activity must be explicit booleans.")

  const noticeRequired = qualifiesAsSmallOrMedium &&
    accountAgeYears >= PAR_SMALL_MEDIUM_PROTECTION_YEARS
  const qualifyingActivityRequired = noticeRequired

  if (!qualifiesAsSmallOrMedium) {
    return {
      status: "standard_schedule",
      noticeRequired: false,
      qualifyingActivityRequired: false,
      demurrageEligible: true,
      protectionYearsComplete: PAR_SMALL_MEDIUM_PROTECTION_YEARS,
      noticeGraceYears: PAR_DEMURRAGE_NOTICE_GRACE_YEARS,
      demurrageEffectiveAtAccountYear: PAR_DEMURRAGE_EFFECTIVE_YEAR,
    }
  }

  if (accountAgeYears < PAR_SMALL_MEDIUM_PROTECTION_YEARS) {
    return {
      status: "protected",
      noticeRequired: false,
      qualifyingActivityRequired: false,
      demurrageEligible: false,
      protectionYearsComplete: PAR_SMALL_MEDIUM_PROTECTION_YEARS,
      noticeGraceYears: PAR_DEMURRAGE_NOTICE_GRACE_YEARS,
      demurrageEffectiveAtAccountYear: PAR_DEMURRAGE_EFFECTIVE_YEAR,
    }
  }

  if (accountAgeYears < PAR_DEMURRAGE_EFFECTIVE_YEAR) {
    return {
      status: "notice_grace",
      noticeRequired: true,
      qualifyingActivityRequired: true,
      demurrageEligible: false,
      protectionYearsComplete: PAR_SMALL_MEDIUM_PROTECTION_YEARS,
      noticeGraceYears: PAR_DEMURRAGE_NOTICE_GRACE_YEARS,
      demurrageEffectiveAtAccountYear: PAR_DEMURRAGE_EFFECTIVE_YEAR,
    }
  }

  if (hasQualifyingActivity) {
    return {
      status: "activity_maintained",
      noticeRequired: true,
      qualifyingActivityRequired: true,
      demurrageEligible: false,
      protectionYearsComplete: PAR_SMALL_MEDIUM_PROTECTION_YEARS,
      noticeGraceYears: PAR_DEMURRAGE_NOTICE_GRACE_YEARS,
      demurrageEffectiveAtAccountYear: PAR_DEMURRAGE_EFFECTIVE_YEAR,
    }
  }

  return {
    status: "demurrage_eligible",
    noticeRequired: true,
    qualifyingActivityRequired: true,
    demurrageEligible: true,
    protectionYearsComplete: PAR_SMALL_MEDIUM_PROTECTION_YEARS,
    noticeGraceYears: PAR_DEMURRAGE_NOTICE_GRACE_YEARS,
    demurrageEffectiveAtAccountYear: PAR_DEMURRAGE_EFFECTIVE_YEAR,
  }
}
