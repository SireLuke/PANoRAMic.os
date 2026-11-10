import {
  analyzeSimplexSymmetry,
  iterateSimplex,
  simplexHausdorffDimension,
  type Simplex,
} from "../../../fractal-kernel/geometries/sierpinski/index.ts";

/** Cross-level lens; it does not create a new geographic/abstraction rung. */
export type ViewLadderLevel = "L0" | "L1" | "L2" | "L3" | "L4" | "L5" | "L6" | "L7" | "L8";

export interface FractalGeometrySnapshot {
  readonly layerId: "pan.fractal-geometry.sierpinski";
  readonly layerVersion: "1.0.0";
  readonly viewLevel: ViewLadderLevel;
  readonly sourceId: string;
  readonly iterationDepth: number;
  readonly cellCount: number;
  readonly similarityDimension: number;
  readonly symmetry: ReturnType<typeof analyzeSimplexSymmetry>;
  readonly readOnly: true;
  readonly canonicalRecordsMutated: false;
}

/**
 * Produces a derived, read-only view snapshot. The caller supplies the view
 * level and provenance-bearing source ID; no canonical PAN records are changed.
 */
export function createSierpinskiViewSnapshot(args: {
  readonly simplex: Simplex;
  readonly viewLevel: ViewLadderLevel;
  readonly sourceId: string;
  readonly iterationDepth: number;
}): FractalGeometrySnapshot {
  if (!args.sourceId.trim()) throw new TypeError("sourceId is required");
  const cells = iterateSimplex(args.simplex, args.iterationDepth);
  return Object.freeze({
    layerId: "pan.fractal-geometry.sierpinski",
    layerVersion: "1.0.0",
    viewLevel: args.viewLevel,
    sourceId: args.sourceId,
    iterationDepth: args.iterationDepth,
    cellCount: cells.length,
    similarityDimension: simplexHausdorffDimension(args.simplex.vertices.length),
    symmetry: analyzeSimplexSymmetry(args.simplex),
    readOnly: true,
    canonicalRecordsMutated: false,
  });
}
