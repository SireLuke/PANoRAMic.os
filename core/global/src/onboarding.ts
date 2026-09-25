export function onboardingPAR(voterProfile) {
    return {
        eligibility: voterProfile.isVerified,
        metrics: "pending-api",
        share: "pending-calculation",
        status: "ready"
    };
}