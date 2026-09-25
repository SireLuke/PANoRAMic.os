// core/economy/src/physicalMintingRules.ts

import { PhysicalPARNote } from "./physicalPAR";
import { computeGlobalParCap } from "./globalFloat";

export type MintContext = {
    digitalParBalance: number;
    totalParSupply: number;
    worldPopulation: number;
    floatMultiplier: number; // default 1.35
    maxPhysicalRatio: number; // e.g. 0.2 = max 20% physical
};

export function canMintPhysicalPAR(
    context: MintContext,
    requestedParAmount: number
) {
    const { globalCap } = computeGlobalParCap({
        worldPopulation: context.worldPopulation,
        floatMultiplier: context.floatMultiplier
    });

    const newTotal = context.totalParSupply + requestedParAmount;

    if (newTotal > globalCap) {
        return false; // exceeds global PAR ceiling
    }

    const maxPhysical = context.digitalParBalance * context.maxPhysicalRatio;
    return requestedParAmount <= maxPhysical;
}

export function applyMint(
    context: MintContext,
    note: PhysicalPARNote
): MintContext {
    return {
        ...context,
        digitalParBalance: context.digitalParBalance - note.parAmount,
        totalParSupply: context.totalParSupply + note.parAmount
    };
}
