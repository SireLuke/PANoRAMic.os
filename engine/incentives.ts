export function onboardingIncentive(population, projectFraction) {
    const parMax = population * 1.35;
    const incentive = population / 1.35;

    return {
        parMax,
        incentive,
        projectFund: parMax * projectFraction,
        status: "ready"
    };
}