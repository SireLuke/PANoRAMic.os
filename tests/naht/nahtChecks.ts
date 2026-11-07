import {
  QuaternionSU2Backend,
  transportHistory,
  validateTopology,
  type NAHTState,
  type TopologyGraph,
  type TransportStep,
} from "../../modules/naht/src/index.ts";

function assert(condition: boolean, message: string): void {
  if (!condition) throw new Error(message);
}

function close(actual: number, expected: number, tolerance = 1e-9): boolean {
  return Math.abs(actual - expected) <= tolerance;
}

export function runNahtChecks(): void {
  const initial: NAHTState = { frameId: "test", channels: [1, 0, 0] };
  const step: TransportStep = {
    id: "z-quarter-turn",
    pathLength: 1,
    rotationAxis: [0, 0, 1],
    angleRadians: Math.PI / 2,
  };

  const result = transportHistory(initial, [step], new QuaternionSU2Backend());
  assert(close(result.finalState.channels[0], 0), "SU(2) rotation x component");
  assert(close(result.finalState.channels[1], 1), "SU(2) rotation y component");
  assert(close(result.finalState.channels[2], 0), "SU(2) rotation z component");
  assert(close(result.history[0].normBefore, result.history[0].normAfterTransport),
    "unit-quaternion transport should preserve vector norm");
  assert(result.history.length === 1, "one history record per path step");

  const coupled = transportHistory(
    initial,
    [step],
    new QuaternionSU2Backend(),
    (state) => [state.channels[0] * 2, state.channels[1], state.channels[2]],
  );
  assert(!close(coupled.history[0].normAfterCoupling,
    coupled.history[0].normAfterTransport), "coupling norm change must be recorded");

  const graph: TopologyGraph = {
    directed: false,
    nodes: [{ id: "a" }, { id: "junction", kind: "junction" }, { id: "b" }],
    edges: [{ from: "a", to: "junction" }, { from: "junction", to: "b" }],
  };
  assert(validateTopology(graph).valid, "valid junction graph");
  assert(!validateTopology({
    directed: false,
    nodes: [{ id: "a" }],
    edges: [{ from: "a", to: "missing" }],
  }).valid, "unknown graph endpoint must fail");

  let rejected = false;
  try {
    transportHistory(initial, [{
      ...step,
      id: "invalid-axis",
      rotationAxis: [0, 0, 0],
    }], new QuaternionSU2Backend());
  } catch {
    rejected = true;
  }
  assert(rejected, "non-zero rotation with zero axis must fail");
}

runNahtChecks();
console.log("NAHT checks passed.");
