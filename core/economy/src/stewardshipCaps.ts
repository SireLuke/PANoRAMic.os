// core/economy/src/stewardshipCaps.ts

import { StewardshipFund } from "./stewardshipFund";

export function canPaySteward(
    fund: StewardshipFund,
    requestedAmount: number
) {
    const remainingCap = fund.annualCap - fund.paidOutThisYear;

    if (requestedAmount > remainingCap) {
        return false;
    }

    if (requestedAmount > fund.total) {
        return false;
    }

    return true;
}

export function applyStewardPayment(
    fund: StewardshipFund,
    amount: number
): StewardshipFund {
    return {
        ...fund,
        total: fund.total - amount,
        paidOutThisYear: fund.paidOutThisYear + amount
    };
}
