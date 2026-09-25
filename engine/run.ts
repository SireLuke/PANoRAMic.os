import { onboardingIncentive } from "./incentive.js";

export function run(world, subsystems) {
    // run incentive logic
    world.incentive = onboardingIncentive(world.population, world.projectFraction);

    return world;
}