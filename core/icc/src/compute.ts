// core/icc/src/compute.ts

import { ICCFlags } from "./flags";

export function computeICC(flags: ICCFlags): number {
    let score = 1;

    if (flags.rightsViolation) score -= 0.4;
    if (flags.corruptionRisk) score -= 0.3;
    if (flags.accessBlocked) score -= 0.2;
    if (flags.transparencyLow) score -= 0.1;

    return Math.max(0, score);
}
