// core/economy/src/realAssetEquivalence.ts

export type RealAssetBundle = {
    water: number;        // liters
    solar: number;        // kWh
    recycling: number;    // kg processed
    food: number;         // kg
    logistics: number;    // km of transport
    manufacturing: number;// unit output
    infrastructure: number;// maintenance credits
};

export function computeRealAssetValue(bundle: RealAssetBundle) {
    return (
        bundle.water * 0.001 +
        bundle.solar * 0.002 +
        bundle.recycling * 0.001 +
        bundle.food * 0.003 +
        bundle.logistics * 0.0005 +
        bundle.manufacturing * 0.005 +
        bundle.infrastructure * 0.01
    );
}
