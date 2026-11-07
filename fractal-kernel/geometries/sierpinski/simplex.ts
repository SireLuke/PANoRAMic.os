import type {
  Point,
  Simplex,
  SimplexCell,
  SymmetryProfile,
} from "./types.ts";

const EPSILON = 1e-12;

function assertFinitePoint(point: Point, label: string): void {
  if (!Array.isArray(point) || point.length === 0) {
    throw new TypeError(`${label} must be a non-empty coordinate array`);
  }
  point.forEach((value, index) => {
    if (!Number.isFinite(value)) {
      throw new TypeError(`${label}[${index}] must be finite`);
    }
  });
}

export function distance(a: Point, b: Point): number {
  if (a.length !== b.length) throw new RangeError("Point dimensions must match");
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += (a[i] - b[i]) ** 2;
  return Math.sqrt(sum);
}

export function validateRegularSimplex(
  simplex: Simplex,
  relativeTolerance = 1e-9,
): void {
  if (!simplex || !Array.isArray(simplex.vertices)) {
    throw new TypeError("A simplex with vertices is required");
  }
  const vertices = simplex.vertices;
  if (vertices.length < 2) throw new RangeError("A simplex needs at least two vertices");
  const dimension = vertices[0].length;
  vertices.forEach((point, index) => {
    assertFinitePoint(point, `vertices[${index}]`);
    if (point.length !== dimension) throw new RangeError("All vertices must share a dimension");
  });
  if (!Number.isFinite(relativeTolerance) || relativeTolerance < 0) {
    throw new RangeError("relativeTolerance must be finite and non-negative");
  }

  const lengths: number[] = [];
  for (let i = 0; i < vertices.length; i++) {
    for (let j = i + 1; j < vertices.length; j++) {
      lengths.push(distance(vertices[i], vertices[j]));
    }
  }
  const mean = lengths.reduce((sum, value) => sum + value, 0) / lengths.length;
  if (mean <= EPSILON) throw new RangeError("Simplex vertices must be distinct");
  const spread = Math.max(...lengths) - Math.min(...lengths);
  if (spread / mean > relativeTolerance) {
    throw new RangeError("Seed vertices do not form a regular simplex within tolerance");
  }
}

/** F_i(x) = (x + v_i) / 2, the equal-ratio simplex IFS. */
export function contractToward(anchor: Point, point: Point): Point {
  if (anchor.length !== point.length) throw new RangeError("Point dimensions must match");
  return Object.freeze(anchor.map((value, index) => (value + point[index]) / 2));
}

/**
 * Returns all finite-stage cells, including the seed at level zero.
 * Cell count at depth k is (n + 1)^k for an n-simplex.
 */
export function iterateSimplex(simplex: Simplex, depth: number): readonly SimplexCell[] {
  validateRegularSimplex(simplex);
  if (!Number.isInteger(depth) || depth < 0) {
    throw new RangeError("depth must be a non-negative integer");
  }

  let cells: SimplexCell[] = [{
    vertices: simplex.vertices.map((point) => Object.freeze([...point])),
    address: [],
  }];
  for (let level = 0; level < depth; level++) {
    const next: SimplexCell[] = [];
    for (const cell of cells) {
      for (let anchorIndex = 0; anchorIndex < cell.vertices.length; anchorIndex++) {
        const anchor = cell.vertices[anchorIndex];
        next.push(Object.freeze({
          vertices: Object.freeze(cell.vertices.map((point) => contractToward(anchor, point))),
          address: Object.freeze([...cell.address, anchorIndex]),
        }));
      }
    }
    cells = next;
  }
  return Object.freeze(cells);
}

export function simplexHausdorffDimension(vertexCount: number): number {
  if (!Number.isInteger(vertexCount) || vertexCount < 2) {
    throw new RangeError("vertexCount must be an integer >= 2");
  }
  return Math.log(vertexCount) / Math.log(2);
}

/** Retained n-dimensional measure fraction after depth iterations. */
export function retainedMeasureFraction(simplexDimension: number, depth: number): number {
  if (!Number.isInteger(simplexDimension) || simplexDimension < 1) {
    throw new RangeError("simplexDimension must be an integer >= 1");
  }
  if (!Number.isInteger(depth) || depth < 0) {
    throw new RangeError("depth must be a non-negative integer");
  }
  const oneStep = (simplexDimension + 1) / (2 ** simplexDimension);
  return oneStep ** depth;
}

function factorial(value: number): number {
  let result = 1;
  for (let i = 2; i <= value; i++) result *= i;
  return result;
}

/**
 * A regular n-simplex has vertex-permutation symmetry S_(n+1).
 * For n=2 this is D3 (six symmetries): a 120-degree cycle and a reflection.
 * The equal-ratio IFS is equivariant under every vertex permutation.
 */
export function analyzeSimplexSymmetry(simplex: Simplex): SymmetryProfile {
  validateRegularSimplex(simplex);
  const vertexCount = simplex.vertices.length;
  const dimension = vertexCount - 1;
  if (dimension === 2) {
    return Object.freeze({
      simplexDimension: dimension,
      vertexCount,
      group: "D3 ≅ S3",
      groupOrder: 6,
      trianglePointGroup: "D3",
      generators: Object.freeze([
        Object.freeze([1, 2, 0]),
        Object.freeze([0, 2, 1]),
      ]),
      recursiveEquivariance: true,
      explanation: "The 120-degree vertex cycle and a reflection generate all six symmetries; the three contraction maps are permuted by the same action at every recursion depth.",
    });
  }
  return Object.freeze({
    simplexDimension: dimension,
    vertexCount,
    group: `S_${vertexCount}`,
    groupOrder: factorial(vertexCount),
    recursiveEquivariance: true,
    explanation: "Every permutation of the regular simplex vertices permutes the equal-ratio contraction maps, so the IFS is equivariant at every depth.",
  });
}
