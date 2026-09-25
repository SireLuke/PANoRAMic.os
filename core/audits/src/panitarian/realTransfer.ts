// core/audits/src/panitarian/realTransfer.ts

import { meetsMinimumThreshold } from "./minimumThreshold";
import { isRealEntity, Entity } from "./entityVerification";
import { isCircularTransfer, Transaction } from "./antiCircularity";

export function isRealTransfer(
    tx: Transaction,
    fromEntity: Entity,
    toEntity: Entity,
    accountValue: number,
    history: Transaction[]
) {
    if (!meetsMinimumThreshold(tx.amount, accountValue)) return false;
    if (!isRealEntity(toEntity)) return false;
    if (isCircularTransfer(tx, history)) return false;

    return true;
}
