// engine/ramsTick.ts

import { WorldState } from "./worldState";
import { ramsIntegrity } from "../core/audits/src/index";
import { ramsEducation } from "../core/audits/src/index";
import { ramsFloat } from "../core/audits/src/index";

export type RamsTickReport = {
    integrity: ReturnType<typeof ramsIntegrity.audit>;
    education: ReturnType<typeof ramsEducation.audit>;
    float: ReturnType<typeof ramsFloat.audit>;
};

export function runRamsTick(world: WorldState): RamsTickReport {
    const integrity = ramsIntegrity.audit({
        worldPopulation: world.population.total,
        resourceParValue: world.resources.renewables,
        floatMultiplier: 1.35,
        resourceMultiplier: 0.9,
        totalParSupply: world.economy.parSupply
    });

    const education = ramsEducation.audit({
        education: {
            topic: world.education.topic ?? "",
            original: world.education.original ?? "",
            translated: world.education.translated ?? "",
            classification: {
                domain: "general",
                safe: true,
                educationalValue: world.education.qualityScore ?? 0,
                ageGroup: "all"
            },
            sourceUrl: null
        }
    });

    const float = ramsFloat.audit({
        worldPopulation: world.population.total,
        resourceParValue: world.resources.renewables,
        floatMultiplier: 1.35,
        resourceMultiplier: 0.9,
        totalParSupply: world.economy.parSupply
    });

    return { integrity, education, float };
}
