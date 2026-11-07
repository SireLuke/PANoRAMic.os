import type { NAHTState } from "../../../modules/naht/src/types.ts";
import {
  adaptV8ToNAHT,
  type V8Projection,
  type V8Vector,
} from "./v8Adapter.ts";

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
  sourceAxes: ["h", "R", "u", "d", "tau", "chi", "s", "f"],
  targetChannels: ["q_r", "q_e", "q_p"],
  requiresExplicitProjection: true,
  mayMutateCanonicalRecords: false,
});

export function createPanNahtAdapter(projection: V8Projection) {
  return Object.freeze({
    registration: PAN_NAHT_REGISTRATION,
    adaptV8(vector: V8Vector) {
      return adaptV8ToNAHT(vector, projection);
    },
    /**
     * Explicitly returns a state for downstream NAHT processing. This adapter
     * does not write results into V8, UHFE/UDFE, Janus Hydra, PAR, or RAMS.
     */
    toState(vector: V8Vector): NAHTState {
      return adaptV8ToNAHT(vector, projection).state;
    },
  });
}
