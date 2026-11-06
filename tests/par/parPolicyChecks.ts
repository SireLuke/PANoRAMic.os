import { runParFeeAllocationEngine } from "../../engine/par/parFeeAllocationEngine"
import { runParDemurrageEngine } from "../../engine/par/demurrageEngine"
import { validateCoverage, UbeCoverage } from "../../pillars/par/PAR_POLICY"

function assert(ok: boolean, message: string): void {
  if (!ok) throw new Error("PAR policy check failed: " + message)
}
function close(actual: number, expected: number, message: string): void {
  assert(Math.abs(actual - expected) <= 1e-10, message + ": expected " + expected + ", got " + actual)
}
const shares = { humanitarianShare: 0.6, stewardshipShare: 0.4 }
const fee = runParFeeAllocationEngine({ transactionValue: 1000, shares })
close(fee.feeAmount, 0.2, "0.02% fee")
close(fee.allocatedTotal, fee.feeAmount, "fee conservation")
close(fee.humanitarianAllocation, 0.12, "humanitarian fee share")
close(fee.stewardshipAllocation, 0.08, "stewardship fee share")

const cycle1 = runParDemurrageEngine({
  openingBalance: 1000, cyclesElapsed: 1, initialRatePerCycle: 0.1,
  compoundingFactor: 0.5, shares,
})
close(cycle1.cumulativeDemurrageRate, 0.1, "cycle 1 cumulative rate")
close(cycle1.demurrageThisCycle, 100, "cycle 1 charge")
close(cycle1.totalPoolAllocation, 100, "cycle 1 pool conservation")
const cycle2 = runParDemurrageEngine({
  openingBalance: 1000, cyclesElapsed: 2, initialRatePerCycle: 0.1,
  compoundingFactor: 0.5, shares,
})
close(cycle2.cumulativeDemurrageRate, 0.15, "cycle 2 compounded rate")
close(cycle2.demurrageThisCycle, 50, "cycle 2 incremental charge")
close(cycle2.totalDemurrageToDate, 150, "cycle 2 cumulative charge")
const finalCycle = runParDemurrageEngine({
  openingBalance: 1000, cyclesElapsed: 100, initialRatePerCycle: 0.1,
  compoundingFactor: 0.5, shares,
})
assert(finalCycle.fullyReverted, "100% cumulative cap is reached")
close(finalCycle.cumulativeDemurrageRate, 1, "demurrage rate cap")
close(finalCycle.retainedBalance, 0, "full reversion leaves zero balance")
close(finalCycle.totalDemurrageToDate, 1000, "full opening balance routed")

const coverage: UbeCoverage = {
  healthcare: 0.8, housing: 0.7, nutrition: 0.9, water_sanitation: 0.95,
  energy: 0.8, education: 0.75, mobility: 0.6, connectivity: 0.9,
}
validateCoverage(coverage)
let rejected = false
try {
  runParFeeAllocationEngine({ transactionValue: 100,
    shares: { humanitarianShare: 0.7, stewardshipShare: 0.4 } })
} catch { rejected = true }
assert(rejected, "invalid pool split rejected")
rejected = false
try { validateCoverage({ ...coverage, healthcare: 1.1 }) } catch { rejected = true }
assert(rejected, "out-of-range UBE coverage rejected")
console.log("PAR policy checks passed.")

import {
  evaluateParDemurrageEligibility,
  PAR_SMALL_MEDIUM_PROTECTION_YEARS,
  PAR_DEMURRAGE_NOTICE_GRACE_YEARS,
  PAR_DEMURRAGE_EFFECTIVE_YEAR,
} from "../../engine/par/demurrageEligibilityEngine"

assert(PAR_SMALL_MEDIUM_PROTECTION_YEARS === 5, "five-year small/medium protection")
assert(PAR_DEMURRAGE_NOTICE_GRACE_YEARS === 1, "one-year notice grace")
assert(PAR_DEMURRAGE_EFFECTIVE_YEAR === 6, "demurrage cannot begin before account year six")
const year4 = evaluateParDemurrageEligibility({
  accountAgeYears: 4.99, qualifiesAsSmallOrMedium: true, hasQualifyingActivity: false,
})
assert(year4.status === "protected" && !year4.noticeRequired && !year4.demurrageEligible,
  "small/medium account protected before year five")
const year5 = evaluateParDemurrageEligibility({
  accountAgeYears: 5, qualifiesAsSmallOrMedium: true, hasQualifyingActivity: false,
})
assert(year5.status === "notice_grace" && year5.noticeRequired && !year5.demurrageEligible,
  "year-five notice starts a full one-year grace interval")
const year599 = evaluateParDemurrageEligibility({
  accountAgeYears: 5.99, qualifiesAsSmallOrMedium: true, hasQualifyingActivity: false,
})
assert(year599.status === "notice_grace" && !year599.demurrageEligible,
  "no demurrage during the full notice year")
const year6Inactive = evaluateParDemurrageEligibility({
  accountAgeYears: 6, qualifiesAsSmallOrMedium: true, hasQualifyingActivity: false,
})
assert(year6Inactive.status === "demurrage_eligible" && year6Inactive.demurrageEligible,
  "inactive account becomes eligible only after six full years")
const year6Active = evaluateParDemurrageEligibility({
  accountAgeYears: 6, qualifiesAsSmallOrMedium: true, hasQualifyingActivity: true,
})
assert(year6Active.status === "activity_maintained" && !year6Active.demurrageEligible,
  "qualifying activity maintains account protection after year six")
const standard = evaluateParDemurrageEligibility({
  accountAgeYears: 0, qualifiesAsSmallOrMedium: false, hasQualifyingActivity: false,
})
assert(standard.status === "standard_schedule" && standard.demurrageEligible,
  "accounts outside protected tier use standard eligibility")
let invalidAgeRejected = false
try {
  evaluateParDemurrageEligibility({
    accountAgeYears: -1, qualifiesAsSmallOrMedium: true, hasQualifyingActivity: false,
  })
} catch { invalidAgeRejected = true }
assert(invalidAgeRejected, "negative account age rejected")
