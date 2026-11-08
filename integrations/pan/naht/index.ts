import type { NAHTState } from "../../../modules/naht/src/types.ts";
import {
  adaptV8ToNAHT,
  type V8Projection,
  type V8Vector,
} from "./v8Adapter.ts";
import {
  adaptV9ToNAHT,
  type V9Projection,
  type V9Vector,
} from "./v9Adapter.ts";
import {
  adaptV9ThroughSU9ToNAHT,
  type SU9NAHTProjection,
  type V9ComplexEncoder,
} from "./su9Adapter.ts";
import type { SU9Matrix } from "../../../modules/naht/src/backends/su9.ts";

export const PAN_NAHT_INTEGRATION_ID = "pan-naht-adapter-v1";

export interface PanNahtRegistration {
  readonly id: string;
  readonly mode: "read-only";
  readonly sourceAxes: readonly ["h", "R", "u", "d", "tau", "chi", "s", "f"];
  readonly targetChannels: readonly ["q_r", "q_e", "q_p"];
  readonly requiresExplicitProjection: true;
  readonly mayMutateCanonicalRecords: false;
}

export const PAN_NAHT_REGISTRATION: PanNahtRegistration = Object.freeze({
  id: PAN_NAHT_INTEGRATION_ID,
  mode: "read-only",
  sourceAxes: ["h", "R", "u", "d", "tau", "chi", "s", "f"] as const,
  targetChannels: ["q_r", "q_e", "q_p"] as const,
  requiresExplicitProjection: true,
  mayMutateCanonicalRecords: false,
});

export interface PanNahtV9Registration {
  readonly id: "pan-naht-v9-adapter-v1";
  readonly mode: "read-only";
  readonly sourceAxes: readonly ["h", "R", "u", "d", "tau", "chi", "s", "f", "xi"];
  readonly targetChannels: readonly ["q_r", "q_e", "q_p"];
  readonly requiresExplicitProjection: true;
  readonly requiresXiSemanticsAndUnits: true;
  readonly mayMutateCanonicalRecords: false;
}

export const PAN_NAHT_V9_REGISTRATION: PanNahtV9Registration = Object.freeze({
  id: "pan-naht-v9-adapter-v1",
  mode: "read-only",
  sourceAxes: ["h", "R", "u", "d", "tau", "chi", "s", "f", "xi"] as const,
  targetChannels: ["q_r", "q_e", "q_p"] as const,
  requiresExplicitProjection: true,
  requiresXiSemanticsAndUnits: true,
  mayMutateCanonicalRecords: false,
});

export interface PanNahtV9SU9Registration {
  readonly id: "pan-naht-v9-su9-adapter-v1";
  readonly mode: "read-only";
  readonly sourceAxes: readonly ["h", "R", "u", "d", "tau", "chi", "s", "f", "xi"];
  readonly targetChannels: readonly ["q_r", "q_e", "q_p"];
  readonly groupAction: "SU(9)";
  readonly requiresExplicitComplexEncoding: true;
  readonly requiresExplicitOutputProjection: true;
  readonly mayMutateCanonicalRecords: false;
}

export const PAN_NAHT_V9_SU9_REGISTRATION: PanNahtV9SU9Registration = Object.freeze({
  id: "pan-naht-v9-su9-adapter-v1",
  mode: "read-only",
  sourceAxes: ["h", "R", "u", "d", "tau", "chi", "s", "f", "xi"] as const,
  targetChannels: ["q_r", "q_e", "q_p"] as const,
  groupAction: "SU(9)",
  requiresExplicitComplexEncoding: true,
  requiresExplicitOutputProjection: true,
  mayMutateCanonicalRecords: false,
});

export const PAN_NAHT_REGISTRATIONS = Object.freeze([
  PAN_NAHT_REGISTRATION,
  PAN_NAHT_V9_REGISTRATION,
  PAN_NAHT_V9_SU9_REGISTRATION,
] as const);

export function createPanNahtAdapter(projection: V8Projection) {
  return Object.freeze({
    registration: PAN_NAHT_REGISTRATION,
    adaptV8(vector: V8Vector) {
      return adaptV8ToNAHT(vector, projection);
    },
    toState(vector: V8Vector): NAHTState {
      return adaptV8ToNAHT(vector, projection).state;
    },
  });
}

export function createPanNahtV9Adapter(projection: V9Projection) {
  return Object.freeze({
    registration: PAN_NAHT_V9_REGISTRATION,
    adaptV9(vector: V9Vector) {
      return adaptV9ToNAHT(vector, projection);
    },
    toState(vector: V9Vector): NAHTState {
      return adaptV9ToNAHT(vector, projection).state;
    },
  });
}

export function createPanNahtV9SU9Adapter(
  encoder: V9ComplexEncoder,
  projection: SU9NAHTProjection,
) {
  return Object.freeze({
    registration: PAN_NAHT_V9_SU9_REGISTRATION,
    transform(vector: V9Vector, matrix: SU9Matrix) {
      return adaptV9ThroughSU9ToNAHT(vector, matrix, encoder, projection);
    },
  });
}
