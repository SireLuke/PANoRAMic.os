// core/audits/src/panitarian/rams.ts

import { computeDynamicDebtRatio, BehaviorScores } from "./dynamicRatio";
import { computeDecayPenalty } from "./decay";
import { isRealTransfer } from "./realTransfer";
import { Transaction } from "./antiCircularity";
import { Entity } from "./entityVerification";

export type RAMSInput = {
    accountValue: number;
    inactiveMonths: number;
    behavior: BehaviorScores;
    lastTransaction?: Transaction;
    history: Transaction[];
    fromEntity: Entity;
    toEntity: Entity;
};

export function computeRAMS(input: RAMSInput) {
    const decayPenalty = computeDecayPenalty(input.inactiveMonths);

    const realTransferHappened = input.lastTransaction
        ? isRealTransfer(
              input.lastTransaction,
              input.fromEntity,
              input.toEntity,
              input.accountValue,
              input.history
          )
        : false;

    const fakeActivityPenalty = realTransferHappened ? 0 : 0.5;

    const scores: BehaviorScores = {
        ...input.behavior,
        decayPenalty,
        fakeActivityPenalty
    };

    const ratio = computeDynamicDebtRatio(scores);

    return {
        ratio,
        decayPenalty,
        realTransferHappened,
        fakeActivityPenalty
    };
}
