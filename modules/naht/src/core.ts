import type {
  ChannelVector,
  CouplingFunction,
  HistoryRecord,
  NAHTState,
  ProvenanceRecord,
  TransportBackend,
  TransportResult,
  TransportStep,
} from "./types.ts";

const EPSILON = 1e-12;

function assertFinite(value: number, label: string): void {
  if (!Number.isFinite(value)) {
    throw new TypeError(`${label} must be a finite number`);
  }
}

export function validateChannels(channels: ChannelVector): void {
  if (!Array.isArray(channels) || channels.length !== 3) {
    throw new TypeError("NAHT channels must contain exactly three values");
  }
  channels.forEach((value, index) => assertFinite(value, `channels[${index}]`));
}

export function validateState(state: NAHTState): void {
  if (!state || typeof state.frameId !== "string" || state.frameId.length === 0) {
    throw new TypeError("NAHT state requires a non-empty frameId");
  }
  validateChannels(state.channels);
}

export function validateStep(step: TransportStep): void {
  if (!step || typeof step.id !== "string" || step.id.length === 0) {
    throw new TypeError("Transport step requires a non-empty id");
  }
  assertFinite(step.pathLength, "pathLength");
  assertFinite(step.angleRadians, "angleRadians");
  if (step.pathLength < 0) throw new RangeError("pathLength cannot be negative");
  if (!Array.isArray(step.rotationAxis) || step.rotationAxis.length !== 3) {
    throw new TypeError("rotationAxis must contain exactly three values");
  }
  step.rotationAxis.forEach((value, index) =>
    assertFinite(value, `rotationAxis[${index}]`)
  );
  const axisNorm = Math.hypot(...step.rotationAxis);
  if (Math.abs(step.angleRadians) > EPSILON && axisNorm <= EPSILON) {
    throw new RangeError("A non-zero rotation requires a non-zero axis");
  }
}

export function channelNorm(channels: ChannelVector): number {
  validateChannels(channels);
  return Math.hypot(channels[0], channels[1], channels[2]);
}

function immutableState(frameId: string, channels: ChannelVector): NAHTState {
  validateChannels(channels);
  return Object.freeze({
    frameId,
    channels: Object.freeze([...channels]) as unknown as ChannelVector,
  });
}

/**
 * Applies path steps in their supplied order and retains each intermediate state.
 * Coupling is optional and may change the norm; the norm delta is recorded rather
 * than silently assuming conservation.
 */
export function transportHistory(
  initialState: NAHTState,
  steps: readonly TransportStep[],
  backend: TransportBackend,
  coupling?: CouplingFunction,
  provenance?: ProvenanceRecord,
): TransportResult {
  validateState(initialState);
  if (!backend || typeof backend.id !== "string" || backend.id.length === 0) {
    throw new TypeError("A named transport backend is required");
  }
  if (!Array.isArray(steps)) throw new TypeError("steps must be an array");

  const initial = immutableState(initialState.frameId, initialState.channels);
  let current = initial;
  const history: HistoryRecord[] = [];

  for (const step of steps) {
    validateStep(step);
    const before = current;
    const transported = backend.apply(before, step);
    validateState(transported);
    const afterTransport = immutableState(
      transported.frameId,
      transported.channels,
    );
    const coupledChannels = coupling
      ? coupling(afterTransport, step)
      : afterTransport.channels;
    const afterCoupling = immutableState(afterTransport.frameId, coupledChannels);

    const normBefore = channelNorm(before.channels);
    const normAfterTransport = channelNorm(afterTransport.channels);
    const normAfterCoupling = channelNorm(afterCoupling.channels);

    history.push(Object.freeze({
      stepId: step.id,
      pathLength: step.pathLength,
      stateBefore: before,
      stateAfterTransport: afterTransport,
      stateAfterCoupling: afterCoupling,
      normBefore,
      normAfterTransport,
      normAfterCoupling,
      couplingNormDelta: normAfterCoupling - normAfterTransport,
    }));
    current = afterCoupling;
  }

  return Object.freeze({
    backendId: backend.id,
    initialState: initial,
    finalState: current,
    history: Object.freeze(history),
    provenance: provenance ? Object.freeze({ ...provenance }) : undefined,
  });
}
