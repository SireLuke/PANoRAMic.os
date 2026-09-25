// core/economy/src/freedomAllotment.ts

export type FreedomCategory =
    | "arts"
    | "science"
    | "culture"
    | "innovation"
    | "community"
    | "ethicalEnterprise";

export function isMoralCategory(category: FreedomCategory) {
    const allowed: FreedomCategory[] = [
        "arts",
        "science",
        "culture",
        "innovation",
        "community",
        "ethicalEnterprise"
    ];

    return allowed.includes(category);
}
