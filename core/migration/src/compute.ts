// core/migration/src/compute.ts

export function computeMigration(data) {
    return {
        displaced: data.displaced || 0,          // UNHCR displacement reports
        refugees: data.refugees || 0,            // UNHCR refugee counts
        asylumSeekers: data.asylumSeekers || 0,  // IOM + UNHCR
        conflictDriven: data.conflictDriven || 0 // public conflict migration indicators
    };
}
