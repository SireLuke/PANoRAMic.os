import { E8_COXETER_PLANE_PROJECTION_V1 as PROJECTION } from "../../fractal-kernel/geometries/sierpinski/gossetCoxeterPlane.ts";

type V8 = readonly number[];
type Face = readonly [number, number, number];

function assert(ok: boolean, message: string): void {
  if (!ok) throw new Error(message);
}
function dot(a: V8, b: V8): number {
  let value = 0;
  for (let i = 0; i < 8; i++) value += a[i] * b[i];
  return value;
}
function key(v: V8): string {
  return v.map((x) => Math.round(x * 1e8) / 1e8).join(",");
}
function faceKey(face: Face): string {
  return [...face].sort((a, b) => a - b).join(":");
}
function project(v: V8): readonly [number, number] {
  const [x, y] = PROJECTION.matrix;
  return [
    x.reduce((sum, a, i) => sum + a * v[i], 0),
    y.reduce((sum, a, i) => sum + a * v[i], 0),
  ];
}
function relSideSpread(a: V8, b: V8, c: V8): number {
  const p = [a, b, c].map(project);
  const d = [
    Math.hypot(p[0][0] - p[1][0], p[0][1] - p[1][1]),
    Math.hypot(p[1][0] - p[2][0], p[1][1] - p[2][1]),
    Math.hypot(p[2][0] - p[0][0], p[2][1] - p[0][1]),
  ];
  const mean = (d[0] + d[1] + d[2]) / 3;
  return mean === 0 ? Infinity : (Math.max(...d) - Math.min(...d)) / mean;
}

function generateE8Roots(): V8[] {
  const roots: V8[] = [];
  for (let i = 0; i < 8; i++) {
    for (let j = i + 1; j < 8; j++) {
      for (const si of [-1, 1]) for (const sj of [-1, 1]) {
        const v = Array(8).fill(0);
        v[i] = si;
        v[j] = sj;
        roots.push(v);
      }
    }
  }
  for (let mask = 0; mask < 256; mask++) {
    let minusCount = 0;
    const v = Array.from({ length: 8 }, (_, i) => {
      const negative = ((mask >> i) & 1) === 1;
      if (negative) minusCount++;
      return negative ? -0.5 : 0.5;
    });
    if (minusCount % 2 === 0) roots.push(v);
  }
  return roots;
}

const SIMPLE_ROOTS: readonly V8[] = [
  [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5],
  [1, 1, 0, 0, 0, 0, 0, 0],
  [-1, 1, 0, 0, 0, 0, 0, 0],
  [0, -1, 1, 0, 0, 0, 0, 0],
  [0, 0, -1, 1, 0, 0, 0, 0],
  [0, 0, 0, -1, 1, 0, 0, 0],
  [0, 0, 0, 0, -1, 1, 0, 0],
  [0, 0, 0, 0, 0, -1, 1, 0],
];

function reflect(v: V8, alpha: V8): V8 {
  const coefficient = dot(v, alpha);
  return v.map((x, i) => x - coefficient * alpha[i]);
}

export function runGossetSierpinskiExperimentChecks(): void {
  const roots = generateE8Roots();
  assert(roots.length === 240, "E8 root system must contain 240 roots");
  const rootIndex = new Map(roots.map((root, i) => [key(root), i]));
  assert(rootIndex.size === 240, "E8 roots must be distinct");
  assert(roots.every((root) => Math.abs(dot(root, root) - 2) < 1e-10),
    "all E8 roots must have squared norm 2");

  const adjacency: Set<number>[] = roots.map(() => new Set<number>());
  let edgeCount = 0;
  for (let i = 0; i < roots.length; i++) {
    for (let j = i + 1; j < roots.length; j++) {
      if (Math.abs(dot(roots[i], roots[j]) - 1) < 1e-10) {
        adjacency[i].add(j);
        adjacency[j].add(i);
        edgeCount++;
      }
    }
  }
  assert(edgeCount === 6720, "Gosset 4_21 must have 6,720 edges");
  assert(adjacency.every((neighbors) => neighbors.size === 56),
    "every E8 root must have 56 edge-neighbors");

  const faces: Face[] = [];
  for (let i = 0; i < roots.length; i++) {
    for (const j of adjacency[i]) {
      if (j <= i) continue;
      for (const k of adjacency[i]) {
        if (k <= j || !adjacency[j].has(k)) continue;
        faces.push([i, j, k]);
      }
    }
  }
  assert(faces.length === 60480, "Gosset 4_21 must have 60,480 triangular 2-faces");
  assert(faces.every(([i, j, k]) =>
    Math.abs(dot(roots[i], roots[j]) - 1) < 1e-10 &&
    Math.abs(dot(roots[j], roots[k]) - 1) < 1e-10 &&
    Math.abs(dot(roots[k], roots[i]) - 1) < 1e-10),
  "each enumerated triangular face must be equilateral in the original 8D metric");

  // Build each simple reflection as a permutation of the 240 roots.
  const reflectionPermutations = SIMPLE_ROOTS.map((alpha) => {
    const permutation = roots.map((root) => {
      const target = rootIndex.get(key(reflect(root, alpha)));
      if (target === undefined) throw new Error("Simple reflection left the E8 root set");
      return target;
    });
    return permutation;
  });

  // Verify transitivity of the W(E8) action on unordered triangular faces.
  const faceByKey = new Map(faces.map((face) => [faceKey(face), face]));
  const seenFaces = new Set<string>();
  const queue: Face[] = [faces[0]];
  seenFaces.add(faceKey(faces[0]));
  for (let cursor = 0; cursor < queue.length; cursor++) {
    const face = queue[cursor];
    for (const permutation of reflectionPermutations) {
      const image = [
        permutation[face[0]], permutation[face[1]], permutation[face[2]],
      ].sort((a, b) => a - b) as unknown as Face;
      const imageKey = faceKey(image);
      if (!faceByKey.has(imageKey)) throw new Error("W(E8) reflection did not preserve triangular faces");
      if (!seenFaces.has(imageKey)) {
        seenFaces.add(imageKey);
        queue.push(image);
      }
    }
  }
  assert(seenFaces.size === 60480, "W(E8) must act transitively on triangular faces");

  const projectedEquilateralFaces = faces.filter(([i, j, k]) =>
    relSideSpread(roots[i], roots[j], roots[k]) <= 1e-8
  );
  assert(projectedEquilateralFaces.length === 2160,
    "selected Coxeter-plane projection must preserve 2,160 triangular faces as equilateral");

  // Coxeter element c = s0 s1 ... s7; apply rightmost reflection first.
  const coxeterPermutation = roots.map((root) => {
    let image = root;
    for (let i = SIMPLE_ROOTS.length - 1; i >= 0; i--) {
      image = reflect(image, SIMPLE_ROOTS[i]);
    }
    const target = rootIndex.get(key(image));
    if (target === undefined) throw new Error("Coxeter element left E8 root set");
    return target;
  });

  const projectedSet = new Set(projectedEquilateralFaces.map(faceKey));
  const visitedProjected = new Set<string>();
  let cyclicOrbitCount = 0;
  const orbitSizes: number[] = [];
  for (const seed of projectedEquilateralFaces) {
    const seedKey = faceKey(seed);
    if (visitedProjected.has(seedKey)) continue;
    let current: Face = seed;
    const orbit = new Set<string>();
    for (let step = 0; step < 30; step++) {
      const currentKey = faceKey(current);
      orbit.add(currentKey);
      const next = [
        coxeterPermutation[current[0]],
        coxeterPermutation[current[1]],
        coxeterPermutation[current[2]],
      ].sort((a, b) => a - b) as unknown as Face;
      current = next;
    }
    assert(current.every((index, i) => index === [...seed].sort((a, b) => a - b)[i]),
      "Coxeter element must return each face after 30 steps");
    assert(orbit.size === 30, "each projected face must have a 30-element C30 orbit");
    assert([...orbit].every((face) => projectedSet.has(face)),
      "C30 must preserve the projected-equilateral face subset");
    for (const face of orbit) visitedProjected.add(face);
    cyclicOrbitCount++;
    orbitSizes.push(orbit.size);
  }
  assert(visitedProjected.size === 2160, "C30 orbits must partition all projected-equilateral faces");
  assert(cyclicOrbitCount === 72 && orbitSizes.every((size) => size === 30),
    "2,160 projected faces must form 72 C30 orbits of size 30");
}

runGossetSierpinskiExperimentChecks();
console.log("Gosset × Sierpinski Coxeter-plane experiment checks passed.");
