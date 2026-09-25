// core/trafficking/src/compute.ts

export function computeTrafficking(data) {
    return {
        forcedLabor: data.forcedLabor || 0,
        sexualExploitation: data.sexualExploitation || 0,
        childTrafficking: data.childTrafficking || 0,
        migrationAbuse: data.migrationAbuse || 0
    };
}
