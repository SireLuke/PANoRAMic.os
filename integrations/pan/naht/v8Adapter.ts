import type {
  NAHTState,
  ProvenanceRecord,
} from "../../../modules/naht/src/types.ts";
import { validateState } from "../../../modules/naht/src/core.ts";

/** Canonical PAN V8 coordinate names; u is Unified Field Potential. */
export interface V8Vector {
  readonly h: number;
  readonly R: number;
  readonly u: number;
  readonly d: number;
  readonly tau: number;
  readonly chi: number;
  readonly s: number;
  readonly f: number;
}

/**
 * The 8D-to-3-channel projection is intentionally supplied by the caller.
 * No default mapping is declared canonical by this adapter.
 */
export interface V8Projection {
  readonly id: string;
  readonly version: string;
  project(vector: V8Vector): NAHTState;
}

export interface AdaptedV8State {
  readonly state: NAHTState;
  readonly provenance: ProvenanceRecord;
}

const V8_AXES: readonly (keyof V8Vector)[] = [
  "h", "R", "u", "d", "tau", "chi", "s", "f",
];

export function validateV8Vector(vector: V8Vector): void {
  for (const axis of V8_AXES) {
    if (!Number.isFinite(vector[axis])) {
      throw new TypeError(`V8 coordinate ${axis} must be finite`);
    }
  }
}

export function adaptV8ToNAHT(
  vector: V8Vector,
  projection: V8Projection,
  sourceVersion = "PAN-V8",
): AdaptedV8State {
  validateV8Vector(vector);
  if (!projection || !projection.id || !projection.version ||
      typeof projection.project !== "function") {
    throw new TypeError("A named, versioned V8 projection is required");
  }

  // Copy the input to prevent an adapter from mutating canonical caller state.
  const snapshot: V8Vector = Object.freeze({
    h: vector.h, R: vector.R, u: vector.u, d: vector.d,
    tau: vector.tau, chi: vector.chi, s: vector.s, f: vector.f,
  });
  const projected = projection.project(snapshot);
  validateState(projected);

  const state: NAHTState = Object.freeze({
    frameId: projected.frameId,
    channels: Object.freeze([...projected.channels]) as unknown as readonly [number, number, number],
  });
  const provenance: ProvenanceRecord = Object.freeze({
    source: "PAN-V8",
    sourceVersion,
    projectionId: `${projection.id}@${projection.version}`,
    attributes: Object.freeze({ readOnly: true, axisCount: 8, channelCount: 3 }),
  });

  return Object.freeze({ state, provenance });
}
