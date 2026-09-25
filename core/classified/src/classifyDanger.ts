import { ClassifiedCategory } from "./types";

export function classifyDanger(text: string): ClassifiedCategory | null {
    const lower = text.toLowerCase();

    if (lower.includes("bioweapon") || lower.includes("pathogen synthesis"))
        return "bioterror";

    if (lower.includes("nerve agent") || lower.includes("chemical weapon"))
        return "chemical";

    if (lower.includes("enrichment") || lower.includes("nuclear device"))
        return "nuclear";

    if (lower.includes("zero-day exploit") || lower.includes("critical infrastructure attack"))
        return "cyber";

    if (lower.includes("extremist manifesto") || lower.includes("radicalization"))
        return "extremist";

    if (lower.includes("torture method") || lower.includes("forced disappearance"))
        return "human_rights_violation";

    if (lower.includes("ethnic cleansing") || lower.includes("genocide"))
        return "crime_against_humanity";

    return null;
}
