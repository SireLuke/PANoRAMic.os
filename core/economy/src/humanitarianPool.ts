// core/economy/src/humanitarianPool.ts

export type PoolSource = "decay" | "taxAllotment" | "corporateOptIn" | "governanceGrant";

export type PoolContribution = {
    source: PoolSource;
    amount: number;
};

export type HumanitarianPool = {
    total: number;
    contributions: PoolContribution[];
};

export function createHumanitarianPool(): HumanitarianPool {
    return {
        total: 0,
        contributions: []
    };
}

export function addToHumanitarianPool(
    pool: HumanitarianPool,
    contribution: PoolContribution
): HumanitarianPool {
    return {
        total: pool.total + contribution.amount,
        contributions: [...pool.contributions, contribution]
    };
}
