import { getClassified } from "../core/classified/src/store";
import { canAccessClassified } from "../panitarian/entityVerification";

export function fetchClassified(entity: { clearance: number }) {
    if (!canAccessClassified(entity)) {
        return { error: "Access denied: insufficient clearance." };
    }

    return getClassified();
}
