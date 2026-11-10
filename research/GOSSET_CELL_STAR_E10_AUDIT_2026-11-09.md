# Gosset local cell-star and E10 exact audit

**Branch:** research/gosset-cell-star-e10-audit-2026-11-09  
**Status:** reproducible standard-library research scripts and tests added; GitHub Actions result pending at initial report creation.  
**No changes to main.**

## A. E8 / Gosset 4_21 local cell star

The calculation starts with the 240 standard E8 roots in exact rational coordinates. It builds the eight simple-root reflections, solves the Cartan/Gram linear systems for fundamental weights, identifies supporting facets at two nodes, and enumerates their Weyl orbits.

| Gosset facet orbit | Facet vertices | Orbit size |
|---|---:|---:|
| 7-orthoplex | 14 | 2,160 |
| 7-simplex | 8 | 17,280 |

The cells incident to the chosen origin are reconstructed as follows:

- Each 7-simplex facet plus the origin gives an 8-simplex cell with 9 vertices. All 36 vertex-pair squared distances equal 2.
- Each 7-orthoplex facet plus the origin and its antipode gives an 8-orthoplex cell with 16 vertices. The centroid of the 14-neighbor facet is c_F=(1/14) sum(v), and the opposite vertex is 2c_F. Its 120 vertex-pair distances consist of 112 squared distances 2 and 8 squared distances 4.

The centroid construction produces 2,160 distinct opposite vertices. An independent enumeration of the E8 lattice vectors of squared norm 4 produces exactly 2,160 vectors, and the sets are equal.

### New local facet-pairing result

For every reconstructed cell incident to the origin, enumerate every 7-dimensional facet that contains the origin.

- 17,280 simplex cells contribute 138,240 origin-containing facets (8 each).
- 2,160 orthoplex cells contribute 276,480 origin-containing facets (128 each).
- There are 207,360 distinct origin-containing facets.
- Every distinct facet occurs exactly twice.

This is an exact local incidence check around one vertex. It is stronger than merely reconstructing the cell star, but it is not a proof of global space-filling, completeness, or absence of nonlocal overlaps. A global proof still requires propagating the cell/facet construction across neighboring vertices and proving the resulting incidence complex is complete and locally finite.

## B. Hyperbolic E10 / 6_21 Coxeter diagnostics

For the rank-10 simply-laced Coxeter diagram with arms (6,2,1), the exact Gram matrix has:

- determinant -1/1024;
- signature (9 positive, 1 negative);
- 10 involution relations;
- 9 adjacent generator order-three relations;
- 36 nonadjacent commutation relations;
- 10 exact Gram-preservation checks.

The 55 defining Coxeter relations pass.

The inverse Gram matrix is the Gram matrix of the dual basis. Its diagonal entries, in the script's declared node order, are:

[-84, -60, -40, -24, -12, -4, 0, -36, -8, -20].

Thus nine dual vertices are timelike (finite vertices in the hyperboloid model) and one is null (an ideal vertex), at node 6. This agrees with the principal-subdiagram analysis: deleting node 6 leaves the affine E9 diagram. All 511 nonempty principal minors of that rank-nine Gram matrix are nonnegative: 510 positive and one zero.

This supplies an exact algebraic ideal-vertex diagnostic. It does not yet construct normalized hyperboloid coordinates, neighboring chambers, a face-paired quotient, or a complete global 6_21 honeycomb.

## C. View Ladder import patch

In the isolated branch only, the import in integrations/pan/view-ladder/fractalGeometryLayer.ts is corrected from:

../../fractal-kernel/geometries/sierpinski/index.ts

to:

../../../fractal-kernel/geometries/sierpinski/index.ts

The path depth follows the file's actual directory: integrations/pan/view-ladder/ to repository root requires three parent traversals. This patch is not applied to main.

## D. Files and execution

- experiments/gosset_local_cell_star_audit.py
- experiments/e10_coxeter_relations_audit.py
- tests/test_gosset_local_cell_star_audit.py
- tests/test_e10_coxeter_relations_audit.py
- .github/workflows/gosset-e10-research-audit.yml
- isolated View Ladder import correction

Run locally:

python -m unittest discover -s tests -p 'test_*_audit.py' -v

All experiment arithmetic uses Python's standard-library fractions.Fraction; no NumPy/SciPy dependencies.

## E. Interpretation boundaries

- Gosset 4_21 remains the finite E8-derived vertex figure.
- The Euclidean 5_21 honeycomb and hyperbolic 6_21 honeycomb remain different constructions.
- The E10 Coxeter diagnostic is not evidence that 5_21 is hyperbolic.
- Janus Hydra remains a translator, not UHFE or UDFE.
- PAN V8 coordinates and UHFE/UDFE semantics are not changed.
- No physical interpretation or new-physics claim follows from these finite geometric and algebraic results.
