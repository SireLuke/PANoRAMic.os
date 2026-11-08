# 6_21 / E10 Coxeter diagnostic

## What is being tested

The (6_{21}) honeycomb is the hyperbolic member of the Gosset (k_{21})
sequence. Its ambient geometry is 9-dimensional hyperbolic space
\(\mathbb H^9\), its vertex figure is the Euclidean \(5_{21}\) honeycomb,
and its cells are alternating 9-simplexes and 9-orthoplexes. The associated
Coxeter diagram is \([3^{6,2,1}]\), also denoted \(\bar T_9\) / E10 in
the cited nomenclature.

This must remain distinct from the Euclidean \(5_{21}\) honeycomb:
\(5_{21}\) tessellates \(\mathbb E^8\), while \(6_{21}\) tessellates
\(\mathbb H^9\). The \(5_{21}\) vertex figure is the local geometry
around each \(6_{21}\) vertex.

## Exact diagnostic performed

Run:

```bash
python experiments/e10_6_21_coxeter_diagnostic.py
```

The script builds the rank-10 simply-laced Coxeter Gram matrix for the
trivalent tree with arms of 6, 2, and 1 edges. Each diagonal entry is 1;
each adjacent-node entry is \(-1/2\); all other entries are zero.

An exact rational LDLᵀ factorization gives:
- inertia: \((9,1)\), i.e. nine positive and one negative direction;
- determinant: \(-1/1024\).

That is the expected Lorentzian signature for a hyperbolic rank-10
Coxeter simplex in \(\mathbb H^9\). The computation is exact over
\(\mathbb Q\), not a floating-point eigenvalue approximation.

## What this does not establish

This diagnostic does **not**:
- generate or render the infinite \(6_{21}\) honeycomb;
- enumerate its vertices, cells, or incidence relations;
- prove discreteness, completeness, or finite covolume by itself;
- establish a physical ninth dimension or connect the tessellation to
  empirical physics;
- make \(5_{21}\) or \(4_{21}\) disappear from the PAN V8/V9 architecture.

A next-stage implementation should independently validate the Coxeter
diagram convention, enumerate a bounded patch using hyperbolic reflections,
check face-pairing and vertex-figure structure, and compare the local
vertex figure against the existing \(5_{21}\)/E8 layer.

## PAN integration boundary

Treat this as an experimental geometry adapter, not a change to canonical
V8 coordinates. Keep:
- V8 / Gosset \(4_{21}\): the existing finite 8D geometry layer;
- \(5_{21}\): the Euclidean E8 honeycomb layer in \(\mathbb E^8\);
- \(6_{21}\): a separate hyperbolic \(\mathbb H^9\) experimental layer;
- V9 coordinate \(\xi\): a PAN state/model coordinate, not an assertion
  that the underlying \(5_{21}\) honeycomb is 9-dimensional.

The geometry layer must label metric signature and ambient space explicitly
so Euclidean and hyperbolic objects cannot be silently mixed.
