// core/economy/src/physicalMintingRules.ts

import { PhysicalPARNote } from "./physicalPAR";
import { computeDynamicParCap } from "./dynamicFloat";

export type MintContext = {
    digitalParBalance: number;
    totalParSupply: number;
    worldPopulation: number;
    resourceParValue: number;
    floatMultiplier: number;     // 1.35
    resourceMultiplier: number;  // 0.90
    maxPhysicalRatio: number;    // e.g. 0.2
};

export function canMintPhysicalPAR(context: MintContext, requestedParAmount: number) {
    const { globalCap } = computeDynamicParCap({
        worldPopulation: context.worldPopulation,
        floatMultiplier: context.floatMultiplier,
        resourceParValue: context.resourceParValue,
        resourceMultiplier: context.resourceMultiplier
    });

    const newTotal = context.totalParSupply + requestedParAmount;

    if (newTotal > globalCap) {
        return false; // exceeds dynamic global cap
    }

    const maxPhysical = context.digitalParBalance * context.maxPhysicalRatio;
    return requestedParAmount <= maxPhysical;
}

export function applyMint(context: MintContext, note: PhysicalPARNote): MintContext {
    return {
        ...context,
        digitalParBalance: context.digitalParBalance - note.parAmount,
        totalParSupply: context.totalParSupply + note.parAmount
    };
}

