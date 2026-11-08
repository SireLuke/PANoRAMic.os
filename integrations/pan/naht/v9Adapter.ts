import type {
  NAHTState,
  ProvenanceRecord,
} from "../../../modules/naht/src/types.ts";
import { validateState } from "../../../modules/naht/src/core.ts";
import { validateV8Vector, type V8Vector } from "./v8Adapter.ts";

/** V9 adds one finite evolution/scale coordinate to the unchanged V8 axes. */
export interface V9Vector extends V8Vector {
  readonly xi: number;
}

export interface V9Projection {
  readonly id: string;
  readonly version: string;
  /** Caller-defined meaning, such as normalized phase or simulation trajectory. */
  readonly xiSemantics: string;
  /** Caller-declared units or the literal value "1" for a dimensionless xi. */
  readonly xiUnits: string;
  project(vector: V9Vector): NAHTState;
}

export interface AdaptedV9State {
  readonly state: NAHTState;
  readonly provenance: ProvenanceRecord;
}

export function validateV9Vector(vector: V9Vector): void {
  validateV8Vector(vector);
  if (!Number.isFinite(vector.xi)) {
    throw new TypeError("V9 coordinate xi must be finite");
  }
}

function validateProjection(projection: V9Projection): void {
  if (!projection || typeof projection.id !== "string" || !projection.id.trim() ||
      typeof projection.version !== "string" || !projection.version.trim() ||
      typeof projection.xiSemantics !== "string" || !projection.xiSemantics.trim() ||
      typeof projection.xiUnits !== "string" || !projection.xiUnits.trim() ||
      typeof projection.project !== "function") {
    throw new TypeError("V9 projection requires an id, version, xi semantics, units, and project function");
  }
}

export function adaptV9ToNAHT(
  vector: V9Vector,
  projection: V9Projection,
  sourceVersion = "PAN-V9",
): AdaptedV9State {
  validateV9Vector(vector);
  validateProjection(projection);

  const snapshot: V9Vector = Object.freeze({
    h: vector.h,
    R: vector.R,
    u: vector.u,
    d: vector.d,
    tau: vector.tau,
    chi: vector.chi,
    s: vector.s,
    f: vector.f,
    xi: vector.xi,
  });
  const projected = projection.project(snapshot);
  validateState(projected);

  const state: NAHTState = Object.freeze({
    frameId: projected.frameId,
    channels: Object.freeze([...projected.channels]) as unknown as readonly [number, number, number],
  });
  const provenance: ProvenanceRecord = Object.freeze({
    source: "PAN-V9",
    sourceVersion,
    projectionId: projection.id + "@" + projection.version,
    attributes: Object.freeze({
      readOnly: true,
      axisCount: 9,
      channelCount: 3,
      xiSemantics: projection.xiSemantics,
      xiUnits: projection.xiUnits,
    }),
  });
  return Object.freeze({ state, provenance });
}
