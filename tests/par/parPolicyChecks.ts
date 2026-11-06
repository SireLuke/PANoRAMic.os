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
