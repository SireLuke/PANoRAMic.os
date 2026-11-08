import {
  applySU9,
  complex9NormSquared,
  validateSU9Matrix,
  type Complex9Vector,
  type SU9Matrix,
} from "../../modules/naht/src/backends/su9.ts";
import { QuaternionSU2Backend } from "../../modules/naht/src/backends/quaternion.ts";
import { transportHistory } from "../../modules/naht/src/core.ts";
import {
  adaptV9ToNAHT,
  type V9Projection,
  type V9Vector,
} from "../../integrations/pan/naht/v9Adapter.ts";
import {
  adaptV9ThroughSU9ToNAHT,
  type SU9NAHTProjection,
  type V9ComplexEncoder,
} from "../../integrations/pan/naht/su9Adapter.ts";

function assert(condition: boolean, message: string): void {
  if (!condition) throw new Error(message);
}

function close(a: number, b: number, tolerance = 1e-9): boolean {
  return Math.abs(a - b) <= tolerance;
}

function throws(action: () => unknown, message: string): void {
  let rejected = false;
  try { action(); } catch { rejected = true; }
  assert(rejected, message);
}

function identitySU9(): ComplexNumber[][] {
  return Array.from({ length: 9 }, (_, i) =>
    Array.from({ length: 9 }, (_, j) => ({ re: Number(i === j), im: 0 }))
  );
}

interface ComplexNumber { re: number; im: number; }

function phaseSU9(angle: number): SU9Matrix {
  const matrix = identitySU9();
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  matrix[0][0] = { re: c, im: s };
  matrix[1][1] = { re: c, im: -s };
  return matrix;
}

export function runPanV9NahtChecks(): void {
  const vector: V9Vector = {
    h: 0.8, R: 0.7, u: 0.75, d: 0.25,
    tau: 0.65, chi: 0.6, s: 0.72, f: 0.55, xi: 0.125,
  };
  const projection: V9Projection = {
    id: "test-v9-to-naht",
    version: "1",
    xiSemantics: "normalized evolution parameter",
    xiUnits: "1",
    project: (v) => ({ frameId: "v9-test", channels: [v.xi, v.h, v.d] }),
  };
  const adapted = adaptV9ToNAHT(vector, projection);
  assert(adapted.state.channels[0] === vector.xi, "xi must reach the explicit NAHT projection");
  assert(adapted.provenance.attributes?.axisCount === 9, "V9 provenance records nine axes");
  assert(adapted.provenance.attributes?.xiUnits === "1", "V9 provenance records xi units");

  const matrix = phaseSU9(0.37);
  validateSU9Matrix(matrix);
  const amplitudes: Complex9Vector = Array.from({ length: 9 }, (_, i) => ({
    re: i / 10,
    im: (8 - i) / 20,
  }));
  const transformed = applySU9(matrix, amplitudes);
  assert(close(complex9NormSquared(amplitudes), complex9NormSquared(transformed)),
    "SU(9) action preserves the C^9 Hermitian norm");

  const encoder: V9ComplexEncoder = {
    id: "test-real-coordinate-encoding",
    version: "1",
    meaning: "test-only embedding of each real V9 coordinate as a real C9 amplitude",
    xiSemantics: "normalized evolution parameter",
    xiUnits: "1",
    encode: (v) => [v.h, v.R, v.u, v.d, v.tau, v.chi, v.s, v.f, v.xi]
      .map((re) => ({ re, im: 0 })),
  };
  const outputProjection: SU9NAHTProjection = {
    id: "test-amplitudes-to-naht",
    version: "1",
    meaning: "test-only projection to three real channels",
    project: (z) => ({
      frameId: "v9-su9-test",
      channels: [z[0].re, z[1].re, z[8].re],
    }),
  };
  const coupled = adaptV9ThroughSU9ToNAHT(
    vector, matrix, encoder, outputProjection,
  );
  assert(coupled.state.channels.length === 3, "SU(9) output is explicitly projected to NAHT's three channels");
  assert(coupled.provenance.attributes?.group === "SU(9)", "SU(9) action is recorded in provenance");
  assert(coupled.provenance.attributes?.axisCount === 9, "SU(9) route retains V9 dimensional provenance");

  const transported = transportHistory(
    coupled.state,
    [{
      id: "test-path",
      pathLength: 1,
      rotationAxis: [0, 0, 1],
      angleRadians: Math.PI / 4,
    }],
    new QuaternionSU2Backend(),
    undefined,
    coupled.provenance,
  );
  assert(transported.history.length === 1, "V9/SU(9)-projected state enters NAHT history transport");
  assert(transported.provenance?.attributes?.group === "SU(9)",
    "NAHT history retains source group provenance");

  throws(() => adaptV9ToNAHT({ ...vector, xi: Number.NaN }, projection),
    "non-finite xi must be rejected");
  const invalid = identitySU9();
  invalid[0][0] = { re: 2, im: 0 };
  throws(() => validateSU9Matrix(invalid), "non-unitary matrices must be rejected");
  throws(() => adaptV9ToNAHT(vector, { ...projection, xiUnits: "" }),
    "projection must declare xi units");
}

runPanV9NahtChecks();
console.log("PAN V9 / NAHT / SU(9) checks passed.");
