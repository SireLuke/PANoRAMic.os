/** Standalone simplex-fractal contracts. No PAN or Gosset dependency. */
export type Point = readonly number[];

export interface Simplex {
  /** n + 1 affinely independent vertices in R^d. */
  readonly vertices: readonly Point[];
}

export interface SimplexCell {
  /** Vertices of one contracted copy of the seed simplex. */
  readonly vertices: readonly Point[];
  readonly address: readonly number[];
}

export interface EquilateralTriple {
  readonly indices: readonly [number, number, number];
  readonly sideLength: number;
  readonly relativeSpread: number;
}

export interface GossetProjection2D {
  /** Explicit 2 x 8 linear projection matrix; caller owns its provenance. */
  readonly matrix: readonly [Point, Point];
  readonly projectionId: string;
}

export interface SymmetryProfile {
  readonly simplexDimension: number;
  readonly vertexCount: number;
  readonly group: string;
  readonly groupOrder: number;
  readonly trianglePointGroup?: "D3";
  readonly generators?: readonly (readonly number[])[];
  readonly recursiveEquivariance: true;
  readonly explanation: string;
}
