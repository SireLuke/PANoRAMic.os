// core/economy/src/currencyConversion.ts

import { computeRealAssetValue, RealAssetBundle } from "./realAssetEquivalence";
import { computeNationAdjustment, NationFactors } from "./nationFactors";

export function convertPARToLocal(
    parAmount: number,
    bundle: RealAssetBundle,
    factors: NationFactors
) {
    const assetValue = computeRealAssetValue(bundle);
    const adjustment = computeNationAdjustment(factors);

    const localValue = parAmount * assetValue * adjustment;

    return {
        par: parAmount,
        localValue,
        assetValue,
        adjustment
    };
}
