// core/audits/src/panitarian/entityVerification.ts

export type Entity = {
    id: string;
    type: "citizen" | "business" | "cooperative" | "publicService" | "humanitarian" | "infrastructure";
    verified: boolean;
    isShellCorp?: boolean;
    isZombieCompany?: boolean;
};

export function isRealEntity(entity: Entity) {
    if (!entity.verified) return false;
    if (entity.isShellCorp) return false;
    if (entity.isZombieCompany) return false;

    return true;
}
