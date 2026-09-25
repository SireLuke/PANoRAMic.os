// core/civilization/src/index.ts

import { CivilizationPillars } from "./pillars";

export function civilization() {
    return {
        pillars: CivilizationPillars,
        count: Object.values(CivilizationPillars)
            .flat()
            .length
    };
}
