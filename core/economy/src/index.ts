// core/economy/src/index.ts
import { convertPARToLocal } from "./currencyConversion";
import { computeRealAssetValue } from "./realAssetEquivalence";
import { computeNationAdjustment } from "./nationFactors";

export const currency = {
    convert: convertPARToLocal,
    realAssets: computeRealAssetValue,
    nationAdjustment: computeNationAdjustment
};import { computeGlobalParCap } from "./globalFloat";
import { canIssuePar } from "./digitalIssuance";

export const globalFloat = {
    cap: computeGlobalParCap,
    canIssue: canIssuePar
};import {
    createStewardshipFund,
    addContribution
} from "./stewardshipFund";

import {
    canPaySteward,
    applyStewardPayment
} from "./stewardshipCaps";

import { auditStewardship } from "./stewardshipGovernance";

export const stewardship = {
    create: createStewardshipFund,
    contribute: addContribution,
    canPay: canPaySteward,
    pay: applyStewardPayment,
    audit: auditStewardship
};import {
    createStewardshipFund,
    addContribution
} from "./stewardshipFund";

import {
    canPaySteward,
    applyStewardPayment
} from "./stewardshipCaps";

import { auditStewardship } from "./stewardshipGovernance";

export const stewardship = {
    create: createStewardshipFund,
    contribute: addContribution,
    canPay: canPaySteward,
    pay: applyStewardPayment,
    audit: auditStewardship
};
import { computeDynamicParCap } from "./dynamicFloat";
import { canIssueParDynamic } from "./digitalIssuance";

export const dynamicFloat = {
    cap: computeDynamicParCap,
    canIssue: canIssueParDynamic
};
