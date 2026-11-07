# Gosset 4_21 × Sierpiński: Coxeter-plane experiment

Status: computational geometry experiment; reproducible construction, not a claim
that Gosset 4_21 itself is a Sierpiński fractal.

## Input geometry

Use the standard 240 E8 roots in R^8, all with squared norm 2:

1. 112 integer roots: all permutations of (±1, ±1, 0, 0, 0, 0, 0, 0).
2. 128 half-integer roots: all vectors (±1/2, ..., ±1/2) with an even number
   of minus signs.

The Gosset polytope 4_21 is the convex hull of these roots. Join two roots by
an edge exactly when their inner product is 1. This gives 56 neighbors per
vertex and 6,720 edges.

## Exact 8D face audit

Enumerate unordered triples (a,b,c) of distinct roots satisfying

\[
a\cdot b=b\cdot c=c\cdot a=1.
\]

Every side then has squared length

\[
\|a-b\|^2=\|a\|^2+\|b\|^2-2a\cdot b=2,
\]

so these are genuinely equilateral triangles in the original 8D metric, with
side length sqrt(2). The enumeration returns **60,480** triangles,
matching the published 2-face count of Gosset 4_21.

A breadth-first orbit traversal using the eight simple-root reflections
listed below reaches all 60,480 triangles from one seed. Thus the Weyl group
acts transitively on these triangular faces. With
|W(E8)|=696,729,600, the setwise stabilizer of one triangle has order

\[
696,729,600/60,480=11,520.
\]

This stabilizer is for the full 8D Weyl action on an unordered face, not the
six-element planar point group of an isolated equilateral triangle.

## Coxeter-plane projection

Choose the simple roots (coordinates in the standard orthonormal basis):

\[
\begin{aligned}
\alpha_0&=\tfrac12(1,-1,-1,-1,-1,-1,-1,1),\\
\alpha_1&=(1,1,0,0,0,0,0,0),\\
\alpha_2&=(-1,1,0,0,0,0,0,0),\\
\alpha_3&=(0,-1,1,0,0,0,0,0),\\
\alpha_4&=(0,0,-1,1,0,0,0,0),\\
\alpha_5&=(0,0,0,-1,1,0,0,0),\\
\alpha_6&=(0,0,0,0,-1,1,0,0),\\
\alpha_7&=(0,0,0,0,0,-1,1,0).
\end{aligned}
\]

For each simple root, form the reflection
s_i(x)=x-(x·alpha_i)alpha_i. Form the Coxeter element
c=s_0 s_1 ... s_7. Its eigenvalues include exp(±2 pi i/30), since the E8
Coxeter number is 30. The real and imaginary parts of a normalized eigenvector
for exp(2 pi i/30) give an orthonormal basis for the selected Coxeter plane.

The corresponding explicit 2×8 projection matrix is exported as
E8_COXETER_PLANE_PROJECTION_V1 in gossetCoxeterPlane.ts. Its rows are:

\[
\begin{pmatrix}
0 & -0.096899068700 & -0.119117702264 & -0.463505659945 &
-0.192736490926 & -0.236930326056 & -0.217638871657 & 0\\
-0.192736490926 & 0.236930326056 & -0.119117702264 & 0.463505659945 &
0 & 0.669823572348 & -0.921933054885 & 0
\end{pmatrix}.
\]

The matrix is tied to the simple-root and Coxeter-element convention above.
An eigenvector phase change rotates the plane coordinates; a different
convention may produce a symmetry-equivalent matrix.

## Results

| Measurement | Result |
|---|---:|
| E8 roots / Gosset vertices | 240 |
| 8D edges | 6,720 |
| 8D equilateral triangular faces | 60,480 |
| Weyl orbit size of one triangular face | 60,480 |
| Setwise face stabilizer order | 11,520 |
| Coxeter-plane projected rings | 8 |
| Vertices per projected ring | 30 |
| 8D faces whose Coxeter-plane images are equilateral | **2,160** |
| Orbits of those 2,160 faces under the Coxeter cyclic subgroup C30 | **72**, each of size 30 |
| Equilateral projected faces in one seeded random orthonormal 2-plane control | 0 (at relative side-spread tolerance 1e-8) |

The eight projected ring radii, and the eight distinct projected side lengths
of the equilateral projected-face subset, agree numerically:

- 0.238235404529
- 0.385472981851
- 0.473860652112
- 0.572924503648
- 0.704294183228
- 0.766722641048
- 0.927011319890
- 1.139571926542

The full-precision values depend on the chosen eigenvector phase and numerical
normalization; the checked-in projection matrix is the reproducible preset.
The key result is the combinatorial count 2,160 under the stated projection
and tolerance, not the rounded radii.

## Interpretation for Sierpiński

This is a meaningful bridge:

- The 8D Gosset geometry contains 60,480 actual equilateral triangular faces.
- In the selected Coxeter plane, 2,160 of those faces remain equilateral.
- Those 2,160 candidates form 72 cyclic orbits under the order-30 Coxeter
  rotation.
- Any one of these projected equilateral triangles can seed the standard
  Sierpiński IFS after normalization.

However, the recursive Sierpiński descendants are not additional Gosset
vertices. For adjacent E8 roots a,b with a·b=1, their midpoint
m=(a+b)/2 has squared norm 3/2, whereas every Gosset vertex has squared norm 2.
The IFS therefore generates a new, scale-recursive geometry overlaid on a
Gosset-derived triangular seed; it does not reveal a pre-existing Sierpiński
sub-polytope inside the finite 240-vertex set.

## Controls and limitations

- A random orthonormal 2D projection was used as a control and did not preserve
  any of the 60,480 triangular faces as equilateral at relative spread
  tolerance 1e-8. This is one control projection, not a universal theorem.
- Coxeter-plane projection preserves a distinguished 30-fold cyclic symmetry,
  but it does not preserve all 8D distances.
- The 72 orbit count is under the Coxeter cyclic subgroup C30 only. No claim is
  made here about orbits under the full planar dihedral normalizer.
- The full Weyl-group face orbit was computed separately in 8D using the
  simple reflections; its transitivity result does not imply that the
  2,160-member projected subset is invariant under all of W(E8).
- Numerical projection tests use relative side-length spread at 1e-8.
- This is pure finite-dimensional geometry; it does not imply a physical
  fractal, field dynamics, or new physics.

## Recommended next test

Use one representative from each of the 72 C30 orbits as a normalized seed
for the Sierpiński IFS. Compare recursion depth, address symmetry, and
projection overlays while keeping the seed's Gosset face ID, Coxeter orbit,
projection ID, and coordinate provenance attached to every generated result.
