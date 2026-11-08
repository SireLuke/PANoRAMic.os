# Sierpiński simplex geometry

Status: experimental, standalone Fractal Kernel primitive.

This module implements the classical Sierpiński triangle and its regular-simplex
generalization. It has no dependency on PAN V8, Janus Hydra, NAHT, UHFE/UDFE,
Chronos, or Gosset 4_21. Host integrations are optional adapters.

## Construction

For a regular (n)-simplex with vertices (v_0,ldots,v_n), define

[
F_i(x)=\frac{x+v_i}{2},\qquad i=0,\ldots,n.
]

At each iteration, replace every cell with its (n+1) contracted copies.
For the triangle, each copy has half the side length and one quarter the area.
After depth (k):

- cell count: (3^k);
- side scale: (2^{-k});
- retained area fraction: ((3/4)^k);
- Hausdorff dimension: (log(3)/log(2)\approx1.5849625).

For a regular (n)-simplex, the equal-ratio IFS has (n+1) maps of ratio
(1/2), giving similarity dimension (log(n+1)/log 2). Its retained
(n)-dimensional measure fraction per iteration is ((n+1)/2^n), when the
sub-simplex interiors are disjoint (as for the standard regular-simplex
construction).

## Recursion symmetry

A regular triangle has dihedral point group (D_3\cong S_3), of order six:
three rotations (including identity) and three reflections. A 120-degree
rotation cycles the three seed vertices; a reflection swaps two vertices.
These generate the full symmetry group.

The IFS is equivariant under this group: a symmetry (g) maps each contraction
(F_i) to the contraction associated with the permuted vertex,
(g\circ F_i=F_{\sigma(i)}\circ g). Therefore every finite iteration and
the limiting attractor retain the seed triangle's D3 symmetry. The recursive
address labels are permuted consistently; the geometry is not merely visually
similar from one iteration to the next.

For a regular (n)-simplex, the corresponding vertex-permutation group is
(S_{n+1}). This is the symmetry of the simplex construction, not a claim that
an arbitrary embedding or projection preserves every symmetry.

## Gosset 4_21 comparison adapter

The optional adapter accepts caller-supplied 8D vertices and an explicit
2-by-8 projection matrix. It then:

1. projects the supplied points into a chosen 2D view;
2. searches for approximately equilateral triples;
3. allows a selected triple to seed the Sierpiński IFS.

No canonical Gosset coordinate table, projection, preferred triangular face,
or V8 mapping is assumed by this package. A projection can collapse distances
or break symmetries. Candidate triples are geometric observations in that
projection, not proof that Gosset 4_21 contains a Sierpiński fractal.

A stronger Gosset relationship would require comparing the stabilizer of the
selected triangle under the actual Gosset symmetry action, checking orbit
structure across equivalent triples, and measuring which symmetries survive
the projection. Record coordinate source, normalization, projection matrix,
tolerance, and algorithm version with every experiment.

## View Ladder proposal

Treat this as a cross-level **Fractal Geometry Layer**, not a new geographic
scope rung. It can be enabled as a visualization/analysis lens at appropriate
L0-L8 views while preserving the View Ladder's existing scope semantics.
Adapters are read-only and must not mutate canonical records or V8 values.

## Validation

The conformance checks cover recursive cell counts, contraction scale,
measure fraction, similarity dimension, D3 generators, 8D embedding,
projection, and equilateral-triple detection. These are mathematical
construction checks; they do not establish a physical model or new physics.
