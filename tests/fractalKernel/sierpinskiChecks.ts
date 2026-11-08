import {
  analyzeSimplexSymmetry,
  findEquilateralTriples,
  iterateSimplex,
  projectGossetVertices,
  retainedMeasureFraction,
  simplexFromProjectedTriple,
  simplexHausdorffDimension,
  type GossetProjection2D,
  type Simplex,
} from "../../fractal-kernel/geometries/sierpinski/index.ts";

function assert(condition: boolean, message: string): void {
  if (!condition) throw new Error(message);
}
function close(actual: number, expected: number, tolerance = 1e-9): boolean {
  return Math.abs(actual - expected) <= tolerance;
}

export function runSierpinskiChecks(): void {
  const h = Math.sqrt(3) / 2;
  const triangle: Simplex = {
    vertices: [[0, 0], [1, 0], [0.5, h]],
  };

  assert(iterateSimplex(triangle, 0).length === 1, "depth zero has one seed cell");
  assert(iterateSimplex(triangle, 1).length === 3, "depth one has three cells");
  assert(iterateSimplex(triangle, 2).length === 9, "depth two has nine cells");
  assert(iterateSimplex(triangle, 3).length === 27, "depth three has 27 cells");
  assert(close(simplexHausdorffDimension(3), Math.log(3) / Math.log(2)),
    "triangle similarity dimension");
  assert(close(retainedMeasureFraction(2, 1), 0.75), "one-step area fraction");
  assert(close(retainedMeasureFraction(2, 2), 0.5625), "two-step area fraction");

  const symmetry = analyzeSimplexSymmetry(triangle);
  assert(symmetry.group === "D3 ≅ S3", "equilateral triangle has D3 symmetry");
  assert(symmetry.groupOrder === 6, "D3 has six elements");
  assert(symmetry.recursiveEquivariance, "IFS is equivariant under D3");

  // The same equilateral seed embedded in R8 remains equilateral.
  const triangle8: Simplex = {
    vertices: [
      [1, 0, 0, 0, 0, 0, 0, 0],
      [-0.5, h, 0, 0, 0, 0, 0, 0],
      [-0.5, -h, 0, 0, 0, 0, 0, 0],
    ],
  };
  assert(iterateSimplex(triangle8, 2).length === 9, "8D embedded triangle iterates");

  const projection: GossetProjection2D = {
    projectionId: "test-xy-projection-v1",
    matrix: [
      [1, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 0, 0, 0, 0],
    ],
  };
  const projected = projectGossetVertices(triangle8.vertices, projection);
  const triples = findEquilateralTriples(projected);
  assert(triples.length === 1, "projection identifies the equilateral seed");
  const recovered = simplexFromProjectedTriple(projected, triples[0]);
  assert(iterateSimplex(recovered, 2).length === 9, "projected triple seeds recursion");

  let rejected = false;
  try {
    iterateSimplex(triangle, -1);
  } catch {
    rejected = true;
  }
  assert(rejected, "negative iteration depth is rejected");
}

runSierpinskiChecks();
console.log("Sierpinski geometry checks passed.");
