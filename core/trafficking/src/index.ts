// core/trafficking/src/index.ts

import { computeTrafficking } from "./compute";
import { scoreTrafficking } from "./score";
import { traffickingFlags } from "./flags";

export function trafficking() {
    return {
        compute: computeTrafficking,
        score: scoreTrafficking,
        flags: traffickingFlags
    };
}
