# Gosset local cell-star and E10 exact audit

**Branch:** research/gosset-cell-star-e10-audit-2026-11-09  
**Status:** reproducible standard-library research scripts and tests added; focused GitHub Actions suite passed on 2026-11-10.  
**No changes to main.**

## A. E8 / Gosset 4_21 local cell star

The calculation starts with the 240 standard E8 roots in exact rational coordinates. It builds the eight simple-root reflections, solves the Cartan/Gram linear systems for fundamental weights, identifies supporting facets at two nodes, and enumerates their Weyl orbits.

| Gosset facet orbit | Facet vertices | Orbit size |
|---|---:|---:|
| 7-orthoplex | 14 | 2,160 |
| 7-simplex | 8 | 17,280 |

The cells incident to the chosen origin are reconstructed as follows:

- Each 7-simplex facet plus the origin gives an 8-simplex cell with 9 vertices. All 36 vertex-pair squared distances equal 2.
- Each 7-orthoplex facet plus the origin and its antipode gives an 8-orthoplex cell with 16 vertices. The centroid of the 14-neighbor facet is c_F=(1/14) sum(v), and the opposite vertex is 2c_F. Its 120 vertex-pair distances consist of 112 squared distances 2 and 8 squared distances 4. All eight antipodal pairs have the same midpoint, the cell has a common center, and every vertex is exactly unit distance from that center.

The centroid construction produces 2,160 distinct opposite vertices. An independent enumeration of the E8 lattice vectors of squared norm 4 produces exactly 2,160 vectors, and the sets are equal.

### New local facet-pairing result

For every reconstructed cell incident to the origin, enumerate every 7-dimensional facet that contains the origin.

- 17,280 simplex cells contribute 138,240 origin-containing facets (8 each).
- 2,160 orthoplex cells contribute 276,480 origin-containing facets (128 each).
- There are 207,360 distinct origin-containing facets.
- Every distinct facet occurs exactly twice.
- 138,240 facets are shared by one simplex cell and one orthoplex cell.
- 69,120 facets are shared by two orthoplex cells.
- No simplex-simplex shared facet occurs in this local star.

The orthoplex-side facet incidence has 138,240 facets occurring once in the orthoplex list (the other incidence comes from a simplex cell) and 69,120 facets occurring twice in the orthoplex list. This makes the local pairing pattern explicit: 138,240 simplex/orthoplex pairs and 69,120 orthoplex/orthoplex pairs.

### Cell-facet adjacency graph

A facet-indexed adjacency pass now enumerates every codimension-one facet of every cell in the 19,440-cell origin star. Simplex cells contribute 9 facets each; orthoplex cells contribute 256 facets each, for 708,480 total cell-facet incidences.

Each facet is keyed by its exact sorted E8 vertex coordinates. The audit records one- or two-cell ownership and builds the shared-facet adjacency graph. For each facet, exact centroid-normal calculations establish its supporting hyperplane and the side occupied by each incident cell. The vector from a cell centroid to a facet centroid must be perpendicular to every facet edge; all off-facet vertices must lie strictly on the interior side. The two cells incident to a shared facet must have outward normals with a strictly negative exact dot product, placing their interiors on opposite sides. Together with the exact common-vertex-set check, this proves that the convex intersection of each facet-adjacent cell pair is exactly that shared facet. It also checks that no cell pair shares more than one facet and that every origin-containing facet is paired inside the origin star.

Singleton facets not containing the origin are boundary facets only relative to this finite star; they may be paired by cells outside it. This is why the audit does not yet assert global completeness or a globally closed adjacency graph.

### Neighboring-star re-root closure

The audit now also re-roots each origin-star cell at each of its non-origin vertices. Every translated cell is required to match an existing cell in the original star. This is a strong overlap-consistency check: any cell shared by the origin star and one of these neighboring stars has the same translated vertex set from both descriptions.

The unique non-origin vertices encountered are exactly 2,400: 240 norm-two roots and 2,160 norm-four vectors. All cell re-root checks pass with zero failures.

The cell-vertex incidence degrees in the origin star are uniform by shell: each of the 240 norm-two root neighbors occurs in exactly 702 origin-star cells, while each of the 2,160 norm-four opposite vertices occurs in exactly one origin-star cell. The first number also counts the cells shared by the origin star and the star centered at an adjacent root vertex; the latter identifies the unique orthoplex cell in which an opposite pair of vertices is separated by squared distance four.

This establishes closure for all cells incident to the origin and every vertex in those cells. It is not yet an independent construction of every cell incident to each neighboring vertex: it verifies the shared cells by translation, while a full neighboring-star comparison must independently regenerate each neighboring star from its own vertex figure and compare the complete cell sets.

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

The neighboring-star re-root closure is implemented in the Gosset experiment and included in its focused unit test.

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

## F. Validation record

The first CI attempts caught two implementation defects before acceptance:

1. The initial fundamental-weight solve incorrectly used the simple-root Gram matrix as though its solution were already expressed in orthonormal coordinates. It was corrected to solve the simple-root row matrix directly for alpha_i dot omega_j = delta_ij.
2. The initial incidence assertion confused the number of orthoplex facet incidences (276,480) with the number of distinct orthoplex-side facets (207,360). The final audit now separately verifies the 138,240 simplex/orthoplex shared facets and 69,120 orthoplex/orthoplex shared facets.

The final focused GitHub Actions run passed on commit 476882e7226dcc27ebc15ec67a55f1f8710ae63c: [run 42754915224](https://github.com/SireLuke/PANoRAMic.os/actions/runs/42754915224). It executes both exact-arithmetic unittest modules. This is not a full-repository CI run and does not test the TypeScript import patch.

The separate PAN Geometric Depth Engine depth-four conformance workflow also passed on commit d1c12b773934fa99198f2b3b8075f0788f5448b8: [run 42753676246](https://github.com/SireLuke/pan-fractal-kernel/actions/runs/42753676246). Its conformance job includes the depth-four reference shell counts and existing independence gate.


## G. Finite-star cell adjacency extension

The cell-adjacency engine enumerates all 708,480 cell-facet incidences in the origin star and builds an exact facet-to-cell index. For every shared facet, the two owning cells are required to have precisely that facet as their full vertex-set intersection. A cell pair may not share multiple distinct facets. All origin-containing facets must have two owners within the finite origin star.

This is a finite-star adjacency certificate. It does not classify every lower-dimensional intersection between non-facet-adjacent cell pairs, nor does it prove that singleton boundary facets away from the origin are paired by cells outside the star. Those are explicit next-stage obligations.


The supporting-hyperplane side test is exact and uses rational centroid coordinates. The cell-centroid-to-facet-centroid vector is checked to be orthogonal to all facet vertices relative to the facet centroid; every off-facet vertex must have a strictly negative dot product with this outward vector. For the two cells incident to a facet, the outward normals must have a strictly negative dot product. Since the common facet is affinely independent and its normal space is one-dimensional, this establishes opposite supporting halfspaces. The two convex cells therefore intersect exactly in their shared facet. This strengthens the certificate from combinatorial adjacency to geometric face-to-face adjacency for every shared facet within the finite star.


## H. Translated boundary closure and volume balance

The next extension audits every singleton facet of the finite origin star that does not contain the origin. For each such facet, it anchors at a facet vertex, translates the facet to the origin, and searches the independently indexed origin star for cells containing the translated facet. The candidate must have that facet as one of its own codimension-one faces. Translating the candidate back gives a cell in the neighboring vertex star. The partner must be unique and its exact outward normal must point to the opposite side of the shared facet.

This checks boundary closure through the translation symmetry of the E8 lattice and the previously verified neighboring-star re-root closure. It is still a local periodic-extension test: it does not enumerate an unbounded global complex or classify every lower-dimensional intersection between arbitrary nonadjacent cells.

An exact volume balance is also calculated. The E8 simple-root basis has determinant/covolume 1. The regular 8-simplex cell has volume 3/8!, and the regular 8-orthoplex cell has volume 2^8/8!. Dividing the origin-star cell counts by their vertex counts gives 1,920 simplex translation-orbit representatives and 135 orthoplex representatives per E8 fundamental volume. Their volume contributions are respectively 1/7 and 6/7, totaling exactly one E8 fundamental volume.

The volume identity is a strong consistency check. It does not by itself prove coverage: the conclusion that the cells tile all of Euclidean space follows only after establishing that the translated cells form a locally finite face-to-face complex with pairwise disjoint interiors. The report keeps those hypotheses explicit rather than treating volume balance as a standalone tiling proof.


## I. E8 Delaunay empty-sphere certificate

The global non-overlap and coverage strategy now uses the lattice Delaunay decomposition rather than an unbounded all-pairs cell-intersection search.

For one representative from each of the two Weyl cell orbits, the exact circumcenter c has squared norm 1 and every cell vertex has squared distance 1 from c. The E8 lattice is even, so any nonzero lattice point has norm at least sqrt(2). If a lattice point x has norm at least 2, the reverse triangle inequality gives ||x-c|| >= ||x||-||c|| >= 1. Therefore a lattice point strictly inside the unit circumsphere would have to be one of the 240 norm-two roots. The script checks every root exactly and verifies that none is inside; exactly the cell's root vertices lie on the sphere.

For a norm-four lattice point, equality at distance 1 is possible only when x=2c. For the orthoplex representative, 2c is its unique norm-four opposite vertex. For the simplex representative, 2c is not in E8. Thus the complete set of lattice points on each empty circumsphere is exactly the cell's vertex set.

The Weyl group preserves the E8 lattice and Euclidean metric and acts transitively on each of the two cell orbits. The empty-sphere proof therefore applies to all 17,280 simplex cells and all 2,160 orthoplex cells in the origin star, and by E8 translation to the entire periodic family.

Consequently every generated cell is a full-dimensional E8 Delaunay cell. Distinct Delaunay cells have disjoint interiors and meet face-to-face; the Delaunay decomposition of a lattice covers Euclidean space. The exact volume balance above shows that the generated periodic family already accounts for one complete E8 fundamental volume: 1/7 from simplex cells and 6/7 from orthoplex cells. Therefore there is no room, modulo the lattice, for any additional full-dimensional Delaunay cells. This establishes that the generated family exhausts the E8 Delaunay tessellation and hence covers Euclidean 8-space without interior overlaps or gaps.

This is the strongest global argument in the current research record. Its assumptions are explicit: the E8 even-lattice characterization, the two Weyl orbit constructions, exact representative empty-sphere checks, translation closure, and the exact orbit-volume count. The script checks the finite arithmetic; the Delaunay decomposition theorem supplies the global tiling implication.
