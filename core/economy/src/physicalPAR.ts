// core/economy/src/physicalPAR.ts

export type PhysicalPARNote = {
    id: string;
    serial: string;
    parAmount: number;
    assetSignatureId: string; // links to real asset bundle
    issuedAt: number;         // ms since epoch
    expiresAt?: number;       // optional, for time‑bound vouchers
};

export function createPhysicalPARNote(
    id: string,
    serial: string,
    parAmount: number,
    assetSignatureId: string,
    issuedAt: number,
    expiresAt?: number
): PhysicalPARNote {
    return {
        id,
        serial,
        parAmount,
        assetSignatureId,
        issuedAt,
        expiresAt
    };
}
