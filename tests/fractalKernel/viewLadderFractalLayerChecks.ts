import { createSierpinskiViewSnapshot } from "../../integrations/pan/view-ladder/fractalGeometryLayer.ts";

function assert(condition: boolean, message: string): void {
  if (!condition) throw new Error(message);
}

export function runViewLadderFractalLayerChecks(): void {
  const height = Math.sqrt(3) / 2;
  const snapshot = createSierpinskiViewSnapshot({
    simplex: { vertices: [[0, 0], [1, 0], [0.5, height]] },
    viewLevel: "L8",
    sourceId: "test-sierpinski-seed-v1",
    iterationDepth: 3,
  });
  assert(snapshot.cellCount === 27, "view snapshot exposes expected recursive cell count");
  assert(snapshot.viewLevel === "L8", "caller-selected View Ladder level is preserved");
  assert(snapshot.readOnly && !snapshot.canonicalRecordsMutated,
    "geometry layer is read-only");
}

runViewLadderFractalLayerChecks();
console.log("View Ladder fractal layer checks passed.");
