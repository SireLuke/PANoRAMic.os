// core/economy/src/physicalVerification.ts

import { PhysicalPARNote } from "./physicalPAR";

export type VerificationResult = {
    valid: boolean;
    reason?: string;
};

export function verifyPhysicalPARNote(
    note: PhysicalPARNote,
    now: number
): VerificationResult {
    if (note.parAmount <= 0) {
        return { valid: false, reason: "Invalid PAR amount" };
    }

    if (note.expiresAt && now > note.expiresAt) {
        return { valid: false, reason: "Note expired" };
    }

    if (!note.assetSignatureId) {
        return { valid: false, reason: "Missing asset signature" };
    }

    return { valid: true };
}
