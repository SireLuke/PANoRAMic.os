export function parPool(population) {
    const max = population * 1.35;

    return {
        max,
        circulating: "pending-api",
        available: "pending-api",
        status: "ready"
    };
}
