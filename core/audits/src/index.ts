// core/audits/src/index.ts

import { computeImpact } from "./computeImpact";
import { score } from "./score";
import { flags } from "./flags";

export function audits() {
    return {
        computeImpact,
        score,
        flags,
        adapters: {
            un: null,
            nasa: null,
            noaa: null,
            transparency: null,
            environment: null
        }
    };import { auditDynamicFloat } from "./ramsDynamicFloat";

export const ramsFloat = {
    audit: auditDynamicFloat
};

}
