import { distance, validateRegularSimplex } from "./simplex.ts";
import type {
  EquilateralTriple,
  GossetProjection2D,
  Point,
  Simplex,
} from "./types.ts";

/**
 * Project supplied 8D coordinates into 2D. The coordinates and projection
 * must be explicitly supplied; this adapter does not invent a Gosset frame.
 */
export function projectGossetVertex(
  vertex: Point,
  projection: GossetProjection2D,
): readonly [number, number] {
  if (vertex.length !== 8) throw new RangeError("Gosset adapter expects 8D input vertices");
  if (!projection.projectionId.trim()) throw new TypeError("projectionId is required");
  if (projection.matrix.length !== 2 ||
      projection.matrix.some((row) => row.length !== 8)) {
    throw new RangeError("Projection matrix must be 2 x 8");
  }
  const projected = projection.matrix.map((row) =>
    row.reduce((sum, coefficient, index) => sum + coefficient * vertex[index], 0)
  );
  if (!projected.every(Number.isFinite)) throw new TypeError("Projection produced non-finite coordinates");
  return Object.freeze([projected[0], projected[1]]);
}

export function projectGossetVertices(
  vertices: readonly Point[],
  projection: GossetProjection2D,
): readonly Point[] {
  return Object.freeze(vertices.map((vertex) => projectGossetVertex(vertex, projection)));
}

/** Find projected triples whose three side lengths agree within tolerance. */
export function findEquilateralTriples(
  points: readonly Point[],
  relativeTolerance = 1e-6,
  maxResults = 1000,
): readonly EquilateralTriple[] {
  if (!Number.isFinite(relativeTolerance) || relativeTolerance < 0) {
    throw new RangeError("relativeTolerance must be finite and non-negative");
  }
  if (!Number.isInteger(maxResults) || maxResults < 1) {
    throw new RangeError("maxResults must be a positive integer");
  }
  points.forEach((point, index) => {
    if (point.length !== 2 || !point.every(Number.isFinite)) {
      throw new TypeError(`points[${index}] must be a finite 2D point`);
    }
  });

  const found: EquilateralTriple[] = [];
  for (let i = 0; i < points.length - 2; i++) {
    for (let j = i + 1; j < points.length - 1; j++) {
      const a = distance(points[i], points[j]);
      if (a === 0) continue;
      for (let k = j + 1; k < points.length; k++) {
        const b = distance(points[j], points[k]);
        const c = distance(points[k], points[i]);
        const mean = (a + b + c) / 3;
        const spread = (Math.max(a, b, c) - Math.min(a, b, c)) / mean;
        if (spread <= relativeTolerance) {
          found.push(Object.freeze({
            indices: Object.freeze([i, j, k]) as readonly [number, number, number],
            sideLength: mean,
            relativeSpread: spread,
          }));
          if (found.length >= maxResults) return Object.freeze(found);
        }
      }
    }
  }
  return Object.freeze(found);
}

export function simplexFromProjectedTriple(
  points: readonly Point[],
  triple: EquilateralTriple,
): Simplex {
  const vertices = triple.indices.map((index) => points[index]);
  const simplex = { vertices };
  validateRegularSimplex(simplex, 1e-6);
  return Object.freeze({
    vertices: Object.freeze(vertices.map((point) => Object.freeze([...point]))),
  });
}
