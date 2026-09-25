// core/economy/src/physicalMintingRules.ts

import { PhysicalPARNote } from "./physicalPAR";

export type MintContext = {
    digitalParBalance: number;
    maxPhysicalRatio: number; // e.g. 0.2 = max 20% of PAR can be physical
};

export function canMintPhysicalPAR(
    context: MintContext,
    requestedParAmount: number
) {
    const maxPhysical = context.digitalParBalance * context.maxPhysicalRatio;
    return requestedParAmount <= maxPhysical;
}

export function applyMint(
    context: MintContext,
    note: PhysicalPARNote
): MintContext {
    return {
        ...context,
        digitalParBalance: context.digitalParBalance - note.parAmount
    };
}
