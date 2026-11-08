# Six experiments: 6_21 / E10 geometry

Run:
```bash
python experiments/e10_6_21_six_experiment_suite.py
```

Optional bounds: `--root-depth 12 --chamber-depth 3 --sierpinski-level 4`.

## A — Reflection growth
Enumerate real roots from ten simple roots using exact integer coefficients and simple reflections. Verify norm 1 and coefficient integrality. Depth 12 cumulative distinct-root counts: 10, 29, 47, 65, 83, 101, 120, 140, 160, 180, 201, 223, 246. This is a bounded orbit, not the full infinite root system.

## B — Hyperbolic chamber patch
Represent simple reflections as integer matrices and breadth-first enumerate distinct Coxeter group elements by bounded generator-word length. This yields a finite chamber adjacency patch, not a coordinate embedding or full honeycomb renderer.

## C — Chamber adjacency
Check generator-labelled chamber edges and involution/reversal within the finite patch; count edges leaving its boundary. This is Coxeter chamber adjacency, not yet incidence among the larger (6_{21}) honeycomb cells.

## D — Vertex-figure / parabolic diagnostic
Exact principal star diagrams give:
- (4,2,1), rank 8: finite E8; Gram inertia (8,0,0), determinant 1/256.
- (5,2,1), rank 9: affine E9; Gram inertia (8,0,1), determinant 0.
- (6,2,1), rank 10: hyperbolic E10; Gram inertia (9,1,0), determinant -1/1024.

The finite E8 parabolic is an algebraic consistency check, not by itself proof that the full (6_{21}) honeycomb vertex figure is the (5_{21}) tessellation. That requires a geometric stabilizer and incidence construction.

## E — Recursive simplex comparison
For the corner-subdivision Sierpiński gasket in dimension d, retain d+1 corner copies scaled by 1/2. At level k there are (d+1)^k retained pieces and similarity dimension log_2(d+1). Compare d=8 and d=9 as recursion models; do not claim this gasket equals or tiles the Gosset honeycomb.

## F — Dimensional ladder
Vary star diagrams (m,2,1), m=4..8; rank is m+4. Exact inertia distinguishes finite E8, affine E9, hyperbolic E10, and higher-rank indefinite extensions. Do not assume m>=7 gives valid hyperbolic honeycombs; each Coxeter simplex and its proper parabolics need separate checks.

## Separate geometry catalogue
Möbius strip, Reuleaux triangle, Gömböc, hyperbolic pair of pants, mucube, oloid, lemniscates, and Penrose/aperiodic tilings are tracked in issue #23. Treat them as independent geometry families unless an explicit structure-preserving map is demonstrated.

## Scope limits
This suite does not yet provide hyperbolic coordinates, enumerate all simplex/orthoplex cells, prove global face-pairing/completeness/discreteness/finite covolume, or establish physical meaning for an additional dimension. Next stage: hyperboloid-model embedding, identify the correct cell orbit and stabilizers, then independently verify face incidence and the (5_{21}) vertex figure.
