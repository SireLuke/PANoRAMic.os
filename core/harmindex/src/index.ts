// core/harmIndex/src/index.ts

import { computeHarm } from "./compute";
import { scoreHarm } from "./score";
import { harmFlags } from "./flags";

export function harmIndex() {
    return {
        compute: computeHarm,
        score: scoreHarm,
        flags: harmFlags
    };
}
