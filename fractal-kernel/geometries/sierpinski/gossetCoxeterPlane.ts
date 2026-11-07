import type { GossetProjection2D } from "./types.ts";

/**
 * Optional Coxeter-plane preset for the E8 simple-root convention documented
 * in GOSSET_COXETER_EXPERIMENT.md. This is not a default/canonical view.
 */
export const E8_COXETER_PLANE_PROJECTION_V1: GossetProjection2D = Object.freeze({
  projectionId: "e8-coxeter-plane-c30-simple-roots-v1",
  matrix: Object.freeze([
    Object.freeze([0, -0.096899068700, -0.119117702264, -0.463505659945, -0.192736490926, -0.236930326056, -0.217638871657, 0]),
    Object.freeze([-0.192736490926, 0.236930326056, -0.119117702264, 0.463505659945, 0, 0.669823572348, -0.921933054885, 0]),
  ]) as unknown as readonly [readonly number[], readonly number[]],
});
