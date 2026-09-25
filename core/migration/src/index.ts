// core/migration/src/index.ts

import { computeMigration } from "./compute";
import { scoreMigration } from "./score";
import { migrationFlags } from "./flags";

export function migration() {
    return {
        compute: computeMigration,
        score: scoreMigration,
        flags: migrationFlags
    };
}
