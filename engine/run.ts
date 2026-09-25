import { travel } from "../core/travel/src/index.js";
import { poi } from "../core/travel/src/poi.js";
import { onboardingIncentive } from "./incentive.js";

export function run(world, subsystems) {

    // Travel subsystem
    world.travel = travel();

    // POI subsystem
    world.poi = poi();

    // PAR onboarding incentive
    world.incentive = onboardingIncentive(
        world.population,
        world.projectFraction
    );
import { WorldState } from "./worldState";

export function createInitialWorldState(): WorldState {
    return {
        time: 0,
        population: {
            total: 0,
            byRegion: {}
        },
        resources: {
            parSupply: 0,
            parCap: 0,
            renewables: 0,
            nonRenewables: 0
        },
        economy: {
            parSupply: 0,
            parCap: 0,
            stewardshipFund: 0,
            humanitarianPool: 0,
            taxLoad: 0
        },
        education: {},
        governance: {},
        humanitarian: {},
        stability: {},
        catastrophe: {},
        migration: {},
        trafficking: {},
        harmindex: {},
        travel: {}
    };
}

    return world;
}
