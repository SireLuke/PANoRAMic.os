// core/economy/src/stewardshipGovernance.ts

import { StewardContribution } from "./stewardshipFund";

export function auditStewardship(contributions: StewardContribution[]) {
    const total = contributions.reduce((sum, c) => sum + c.amount, 0);

    return {
        total,
        count: contributions.length,
        lastContribution: contributions[contributions.length - 1] || null
    };
}
