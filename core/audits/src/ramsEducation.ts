// core/audits/src/ramsEducation.ts

export type RamsEducationAuditInput = {
    education: {
        topic: string;
        original: string;
        translated: string;
        classification: {
            domain: string;
            safe: boolean;
            educationalValue: number;
            ageGroup: string;
        };
        sourceUrl: string | null;
    } | null;
};

export function auditEducation(input: RamsEducationAuditInput) {
    const edu = input.education;

    if (!edu) {
        return {
            ok: false,
            reason: "No education data present",
            details: null
        };
    }

    const safe = edu.classification.safe === true;
    const hasSource = typeof edu.sourceUrl === "string" && edu.sourceUrl.length > 0;
    const valueHigh = edu.classification.educationalValue >= 0.5;

    const ok = safe && hasSource && valueHigh;

    return {
        ok,
        reason: ok ? null : "Education module failed safety or validity checks",
        details: {
            topic: edu.topic,
            safe,
            hasSource,
            educationalValue: edu.classification.educationalValue,
            ageGroup: edu.classification.ageGroup
        }
    };
}
