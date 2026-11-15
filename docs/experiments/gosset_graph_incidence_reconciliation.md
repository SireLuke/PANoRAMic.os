# Gosset Graph-to-Cell Incidence Reconciliation

**Status:** Isolated exact-rational experiment; no production wiring.

## Objective

Continue the independent 7-orthoplex graph reconstruction by lifting its
2,160 graph-derived 14-root facets into 8-orthoplex Delaunay cells, then
reconcile their origin-containing codimension-one facets against the
8-simplex local-star orbit.

## Construction

1. Build the 240-vertex Gosset graph using the exact E8 root inner-product
   rule and reconstruct all 2,160 7-orthoplex facets through the compatible
   orthogonal-pair graph.
2. For each graph-derived 14-root facet, compute its exact centroid c.
   The candidate opposite vertex is 2c. Verify it belongs to the even E8
   lattice, has norm squared 4, and yields a 16-vertex regular
   8-orthoplex with edge-length squared 2 and unit circumradius.
3. Generate the 8-simplex orbit separately from the other fundamental
   weight. This is a comparator, not a source of orthoplex candidates.
4. Enumerate every origin-containing 7-face of each 8-orthoplex and
   8-simplex using exact vertex tuples.
5. Reconcile exact face sets, owner multiplicities, common vertex sets,
   supporting hyperplanes, and opposite interior halfspaces.

## Expected exact incidence signature

| Quantity | Count |
|---|---:|
| Graph-derived 8-orthoplex cells | 2,160 |
| 8-simplex cells | 17,280 |
| Simplex origin-face incidences | 138,240 |
| Orthoplex origin-face incidences | 276,480 |
| Unique origin-containing facets | 207,360 |
| Simplex/orthoplex shared facets | 138,240 |
| Orthoplex/orthoplex shared facets | 69,120 |
| Simplex/simplex shared facets | 0 |

Every unique origin-containing facet must have exactly two incident cells.
For each shared facet, both cells must have precisely that 8-vertex set in
common; their exact outward normals must have negative dot product, placing
their interiors on opposite sides of the shared supporting hyperplane.

The orthoplex-only face multiplicity profile is 138,240 singleton faces
(shared with one simplex) and 69,120 double-owned faces (shared by two
orthoplexes). Thus the simplex face set is a subset of the orthoplex face
set; it is not equal to the full orthoplex face set.

## Lean scope

The Lean 4 module formalizes the finite incidence arithmetic, including
138,240 + 69,120 = 207,360 and the two-to-one total incidence count.
It does not formalize the E8 graph enumeration, geometric halfspace tests,
or exact equality of the computed face sets; those remain executable
exact-rational Python checks.

## Reproduction

\`\`\`sh
python -m unittest tests.test_gosset_graph_incidence_reconciliation -v
PYTHONPATH=. python experiments/gosset_graph_incidence_reconciliation.py
cd lean && lake build
\`\`\`

## Validation boundary

A pass establishes the specified finite local incidence and shared-face
geometry for the declared E8 construction. It does not independently prove
global Euclidean coverage or non-overlap outside the existing finite-star
and Delaunay arguments, and it makes no physical claim.
