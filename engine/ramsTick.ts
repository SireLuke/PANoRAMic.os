// engine/ramsTick.ts

import { WorldState } from "./worldState";
import { ramsClassified } from "../core/audits/src/index";
import {
    ramsIntegrity,
    ramsEducation,
    ramsFloat,
    ramsEconomy,
    ramsTrafficking,
    ramsMigration,
    ramsStability,
    ramsCatastrophe,
    ramsHumanitarian,
    ramsGovernance,
    ramsICC
} from "../core/audits/src/index";



export type RamsTickReport = {
    integrity: ReturnType<typeof ramsIntegrity.audit>;
    education: ReturnType<typeof ramsEducation.audit>;
    float: ReturnType<typeof ramsFloat.audit>;
    economy: ReturnType<typeof ramsEconomy.audit>;
    trafficking: ReturnType<typeof ramsTrafficking.audit>;
    migration: ReturnType<typeof ramsMigration.audit>;
    stability: ReturnType<typeof ramsStability.audit>;
    catastrophe: ReturnType<typeof ramsCatastrophe.audit>;
    humanitarian: ReturnType<typeof ramsHumanitarian.audit>;
    governance: ReturnType<typeof ramsGovernance.audit>;
    icc: ReturnType<typeof ramsICC.audit>;
    classified: ReturnType<typeof ramsClassified.audit>;

};

export function runRamsTick(world: WorldState): RamsTickReport {
    return {
        integrity: ramsIntegrity.audit({ world }),
        education: ramsEducation.audit({ world }),
        float: ramsFloat.audit({ world }),
        economy: ramsEconomy.audit({ world }),
        trafficking: ramsTrafficking.audit({ world }),
        migration: ramsMigration.audit({ world }),
        stability: ramsStability.audit({ world }),
        catastrophe: ramsCatastrophe.audit({ world }),
        humanitarian: ramsHumanitarian.audit({ world }),
        governance: ramsGovernance.audit({ world }),
        icc: ramsICC.audit({ world })
        classified: ramsClassified.audit({ world }),

    };
}

