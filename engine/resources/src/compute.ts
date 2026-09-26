import { ResourceState } from "./types";

export function computeResourceScores(resources: ResourceState) {
    const total =
        resources.water +
        resources.food +
        resources.minerals +
        resources.energy +
        resources.renewables;

    const scarcity = Math.max(0, 1000 - total) / 1000;

    const sustainability =
        (resources.renewables + resources.water) /
        (total + 1);

    const resourceScore = total / 1000;

    return {
        resourceScore,
        scarcityScore: scarcity,
        sustainabilityScore: sustainability
    };
}
