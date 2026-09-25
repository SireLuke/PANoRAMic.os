// core/icc/src/score.ts

import { ICCFlags } from "./flags";
import { computeICC } from "./compute";

export type ICCScore = {
    score: number;
    flags: ICCFlags;
};

export function scoreICC(flags: ICCFlags): ICCScore {
    return {
        score: computeICC(flags),
        flags
    };
}
