// core/audits/src/ramsResources.ts

import { WorldState } from "../../../engine/worldState";

/**
 * RAMS Resource Audit
 *
 * Ensures:
 * - resource stability
 * - sustainability
 * - scarcity monitoring
 * - extraction vs regeneration balance
 */

export function auditResources(input: { world: WorldState }) {
    const res = input.world.resources;

    if (!res) {
        return {
            ok: false,
            reason: "No resource subsystem present",
            resourceScore: 0,
            scarcityScore: 0,
            sustainabilityScore: 0
        };
    }

    const ok =
        res.sustainabilityScore >= 0.2 &&
        res.scarcityScore <= 0.8;

    return {
        ok,
        reason: ok ? null : "Resource sustainability or scarcity thresholds violated",
        resourceScore: res.resourceScore,
        scarcityScore: res.scarcityScore,
        sustainabilityScore: res.sustainabilityScore
    };
}
