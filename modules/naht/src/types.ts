/** Standalone NAHT contracts. No PAN-specific types or imports belong here. */

export type ChannelVector = readonly [number, number, number];
export type Vec3 = readonly [number, number, number];

export interface NAHTState {
  readonly frameId: string;
  readonly channels: ChannelVector;
}

export interface TransportStep {
  readonly id: string;
  readonly pathLength: number;
  readonly rotationAxis: Vec3;
  readonly angleRadians: number;
  readonly metadata?: Readonly<Record<string, string | number | boolean>>;
}

export interface TransportBackend {
  readonly id: string;
  apply(state: NAHTState, step: TransportStep): NAHTState;
}

export type CouplingFunction = (
  state: NAHTState,
  step: TransportStep,
) => ChannelVector;

export interface ProvenanceRecord {
  readonly source: string;
  readonly sourceVersion: string;
  readonly projectionId?: string;
  readonly capturedAt?: string;
  readonly attributes?: Readonly<Record<string, string | number | boolean>>;
}

export interface HistoryRecord {
  readonly stepId: string;
  readonly pathLength: number;
  readonly stateBefore: NAHTState;
  readonly stateAfterTransport: NAHTState;
  readonly stateAfterCoupling: NAHTState;
  readonly normBefore: number;
  readonly normAfterTransport: number;
  readonly normAfterCoupling: number;
  readonly couplingNormDelta: number;
}

export interface TransportResult {
  readonly backendId: string;
  readonly initialState: NAHTState;
  readonly finalState: NAHTState;
  readonly history: readonly HistoryRecord[];
  readonly provenance?: ProvenanceRecord;
}
