// core/audits/src/ramsIntegrity.ts

import { auditDynamicFloat } from "./ramsDynamicFloat";

export type RamsIntegrityInput = {
    worldPopulation: number;
    resourceParValue: number;
    floatMultiplier: number;     // 1.35
    resourceMultiplier: number;  // 0.90
    totalParSupply: number;
};

export type RamsIntegrityResult = {
    ok: boolean;
    float: ReturnType<typeof auditDynamicFloat>;
};

export function auditIntegrity(input: RamsIntegrityInput): RamsIntegrityResult {
    const floatAudit = auditDynamicFloat(input);

    const ok = floatAudit.withinCap;

    return {
        ok,
        float: floatAudit
    };
}
