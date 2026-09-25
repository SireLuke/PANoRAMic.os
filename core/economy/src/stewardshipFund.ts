// core/economy/src/stewardshipFund.ts

export type StewardContribution = {
    contributorId: string;
    amount: number;
    timestamp: number;
};

export type StewardshipFund = {
    total: number;
    contributions: StewardContribution[];
    annualCap: number; // max steward income per year
    stewardId: string;
    paidOutThisYear: number;
};

export function createStewardshipFund(
    stewardId: string,
    annualCap: number
): StewardshipFund {
    return {
        total: 0,
        contributions: [],
        annualCap,
        stewardId,
        paidOutThisYear: 0
    };
}

export function addContribution(
    fund: StewardshipFund,
    contribution: StewardContribution
): StewardshipFund {
    return {
        ...fund,
        total: fund.total + contribution.amount,
        contributions: [...fund.contributions, contribution]
    };
}
