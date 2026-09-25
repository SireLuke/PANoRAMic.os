import { travel } from "../core/travel/src/index.js";
import { poi } from "../core/travel/src/poi.js";
import { onboardingIncentive } from "./incentive.js";
import { onboardingIncentive } from "./incentive.js";

export function run(world, subsystems) {
    // run incentive logic
    world.incentive = onboardingIncentive(world.population, world.projectFraction);

    return world;
}