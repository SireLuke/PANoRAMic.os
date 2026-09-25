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

    return world;
}