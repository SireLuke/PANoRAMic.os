// core/harmIndex/src/compute.ts

export function computeHarm(data) {
    return {
        environmental: data.environmental || 0,
        humanRights: data.humanRights || 0,
        trafficking: data.trafficking || 0,
        migration: data.migration || 0,
        governance: data.governance || 0,
        supplyChain: data.supplyChain || 0
    };
}
