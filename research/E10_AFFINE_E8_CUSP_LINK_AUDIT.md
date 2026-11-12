# E10 ideal-link to affine E8 root realization

## Research objective

Make the affine E8 vertex link explicit in Euclidean root coordinates, rather than relying only on the semidefinite rank-nine Gram matrix and its null vector.

## Exact construction

- The E10 ideal vertex is node 6.
- Deleting node 6 leaves the nine-node affine E8 diagram with edges:
  `(0,1), (1,2), (2,3), (3,4), (4,5), (0,7), (7,8), (0,9)`.
- Primitive null-root marks in node order `(0,1,2,3,4,5,7,8,9)` are `(6,5,4,3,2,1,4,2,3)`.
- The finite E8 subdiagram is obtained by deleting affine node 5. Its highest-root coefficients in the selected simple-root basis are `(2,3,4,6,5,4,3,2)`.
- The affine simple root is the negative highest root. The nine exact root vectors must reproduce the E10 link Gram matrix after scaling the Coxeter Gram by 2.
- The affine reflection at node 5 uses the shifted hyperplane; composing it with the finite highest-root reflection produces translation by the highest root. The finite Weyl orbit of that root is checked against all 240 E8 roots, and conjugation witnesses translations by every root. Since the chosen simple-root basis has covolume one, these translations generate the E8 root lattice. The affine Wythoff seed at the origin therefore has the E8 lattice as its orbit.

## Wythoffian ladder

The affine E8 group is the symmetry group underlying the Euclidean 5_21 honeycomb. Its local Delaunay star at the origin consists of 8-simplex and 8-orthoplex cells; the 240 norm-two E8 roots form the 4_21 root-polytope vertex figure. The hyperbolic 6_21 honeycomb has 5_21 as its vertex figure. This identifies the geometric ladder, but the local certificates in this repository are not by themselves a global completeness proof.

## Validation boundary

This verifies the exact affine E8 root/reflector algebra and a translation witness. It is not yet a construction of the `5_21` Wythoffian, its incidence structure, or the global hyperbolic `6_21` honeycomb.
