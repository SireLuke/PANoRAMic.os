export function merge(inputs) {
    return {
        status: "ready",
        inputs,
        output: "pending-calculation"
    };
}
