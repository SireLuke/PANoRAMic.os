export type ClassifiedCategory =
    | "bioterror"
    | "chemical"
    | "nuclear"
    | "cyber"
    | "extremist"
    | "human_rights_violation"
    | "crime_against_humanity";

export type ClassifiedRecord = {
    id: string;
    category: ClassifiedCategory;
    summary: string;
    riskLevel: number; // 0–1
    timestamp: number;
};
