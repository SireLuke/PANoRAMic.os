// core/audits/src/panitarian/index.ts

import { computeRAMS } from "./rams";
import { computeStagnationPenalty } from "./transactionFlow";
import { computeDecayPenalty } from "./decay";
import { computePublicPoolReversion } from "./publicPool";
import { isRealTransfer } from "./realTransfer";

export const panitarianAudit = {
    rams: computeRAMS,
    stagnation: computeStagnationPenalty,
    decay: computeDecayPenalty,
    realTransfer: isRealTransfer,
    publicPool: computePublicPoolReversion
};
