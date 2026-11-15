# Gosset 7-Orthoplex Facet Orbit from the 240-Root Graph

**Status:** Isolated exact-arithmetic experiment. No production wiring.

## Question

Can the 2,160 facets in the 7-orthoplex facet orbit of the Gosset 4_21
vertex figure be reconstructed without using the Weyl-reflection seed orbit?

## Independent graph construction

The 240 E8 roots define the Gosset graph by the exact adjacency condition
\(x\cdot y=1\). The graph has degree 56 and 6,720 edges.

Construct a second graph whose vertices are unordered orthogonal root pairs
\(\{x,y\}\) with \(x\cdot y=0\). There are 15,120 such pair-vertices.
Two pair-vertices \(\{x,y\}\) and \(\{u,v\}\) are compatible when all four
cross inner products equal 1. A 7-clique in this compatibility graph
therefore selects seven disjoint orthogonal pairs, with every cross-pair
adjacent in the Gosset graph.

The union of the seven pairs is a 14-root set whose induced Gosset graph is
\(K_{14}\) minus a perfect matching: 84 edges and 7 nonedges. This is the
combinatorial signature of a 7-orthoplex facet.

The graph-derived 14-sets are compared by exact set equality with the
independent 2,160-member Weyl-reflection orbit. The Weyl construction is
used only as the comparison target, not to generate graph candidates.

## Formalized arithmetic

The dependency-free Lean 4 module proves the finite count identities:
seven opposite pairs give fourteen vertices; there are 84 cross-pair
edges; the seven missing edges are the matching; and
\(\binom{14}{2}-7=84\).

These Lean lemmas formalize the counting invariant, not the enumeration of
all E8 roots or the orbit equality. The latter is checked by the exact
Python experiment and CI.

## Reproduction

\`\`\`sh
python -m unittest tests.test_gosset_orthoplex_graph_orbit -v
PYTHONPATH=. python experiments/gosset_orthoplex_graph_orbit.py
cd lean && lake build
\`\`\`

## Scope

A pass establishes exact finite combinatorial reconstruction for the
declared 240-root E8 model. It does not by itself prove a global Delaunay
tiling, non-overlap beyond the established Delaunay argument, or any
physical interpretation.
