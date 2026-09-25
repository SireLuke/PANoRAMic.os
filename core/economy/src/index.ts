// core/economy/src/index.ts

import { convertPARToLocal } from "./currencyConversion";
import { computeRealAssetValue } from "./realAssetEquivalence";
import { computeNationAdjustment } from "./nationFactors";

export const currency = {
    convert: convertPARToLocal,
    realAssets: computeRealAssetValue,
    nationAdjustment: computeNationAdjustment
};
