// panitarian/entityVerification.ts

export type EntityProfile = {
    id: string;
    name: string;
    clearance: number; // 0–5
    verified: boolean;
    reputation: number; // 0–1
};

export function verifyEntity(entity: EntityProfile): boolean {
    if (!entity) return false;
    if (!entity.verified) return false;
    if (entity.reputation < 0.2) return false;
    return true;
}

export function canAccessClassified(entity: EntityProfile): boolean {
    return entity.clearance >= 5;
}

export function canAccessGovernance(entity: EntityProfile): boolean {
    return entity.clearance >= 3;
}

export function canAccessPublicPool(entity: EntityProfile): boolean {
    return entity.clearance >= 2;
}
