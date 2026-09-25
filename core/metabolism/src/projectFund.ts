export function projectFund(population, fraction) {
    const max = population * 1.35;

    return {
        max,
        fraction,
        fund: "pending-api",
        status: "ready"
    };
}
