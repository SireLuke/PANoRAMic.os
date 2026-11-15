# Gosset Codimension-Two Link-Cycle Audit

**Status:** Isolated exact combinatorial experiment. No production wiring.

## Question

For every origin-containing codimension-two face in the combined 8-simplex /
8-orthoplex local star, does the incident-cell link form one connected cycle?
This tests a local manifold/face-to-face condition one dimension below the
shared-facet audit.

## Construction

- A link vertex is an origin-containing codimension-one facet (an 8-vertex
  face containing the origin).
- A link edge is an incident 8-cell containing the codimension-two face.
- For an 8-simplex, choose six of its eight non-origin vertices. The two
  omitted vertices define the two facet completions and therefore one link
  edge.
- For an 8-orthoplex, choose six of its seven non-origin antipodal pairs,
  then choose one endpoint from each selected pair. The omitted antipodal
  pair supplies the two facet completions and therefore one link edge.
- Group edges by exact rational vertex-set identity of the codimension-two
  face. No floating-point geometry or precomputed facet-neighbor graph is
  used.

For every link, the audit checks degree two at every link vertex, connectedness,
equal edge/vertex counts, at least three vertices, and absence of parallel
edges. It also independently checks that each origin-containing facet has
exactly two incident cells.

## Scope

A pass establishes that every audited origin-containing codimension-two face
has a single simple cycle as its local combinatorial link in this finite star.
It does not prove that the finite star covers all of Euclidean 8-space, nor
does it establish global completeness of the Gosset Delaunay tessellation.

The Lean module records elementary cycle-count arithmetic only. The actual
root enumeration, link construction, connectedness, and degree checks are
verified by the exact Python audit and its tests.

## Reproduction

\`\`\`sh
python -m unittest tests.test_gosset_codim2_link_audit -v
PYTHONPATH=. python experiments/gosset_codim2_link_audit.py
cd lean && lake build
\`\`\`
