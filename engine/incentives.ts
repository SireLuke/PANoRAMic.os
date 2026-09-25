export function onboardingIncentive(population, projectFraction) {
    const parMax = population * 1.35;
    const incentive = population / 1.35;
    const projectFund = parMax * projectFraction;

    return {
        parMax,
        incentive,
        projectFund,
        status: "ready"
    };
    export function onboardingPAR(voterProfile) {
    return {
        eligibility: voterProfile.isVerified,
        metrics: "pending-api",
        share: "pending-calculation",
        status: "ready"
    };
}
}
