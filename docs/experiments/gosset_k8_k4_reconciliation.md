# Gosset 8-Simplex / K8 and K4 Local-to-Global Reconciliation

**Status:** Isolated exact combinatorial experiment; no production wiring.

## Question

Do the 8-vertex facets generated as the simplex-cell orbit in the exact E8
Delaunay vertex star coincide with the 8-cliques of the Gosset graph on the
240 E8 roots? If so, how do their 4-clique incidences reconcile?

## Independent constructions

The geometric construction reproduces the established Weyl-reflection orbit
of the simplex facet seed, yielding 17,280 eight-vertex sets.

The graph construction independently builds the 240-vertex Gosset graph
using the exact root inner-product rule dot(x, y) = 1, then enumerates
cliques by ordered common-neighbor intersections. It separately enumerates
all graph K4s and K8s.

No floating-point arithmetic, SciPy, GPU computation, or full Weyl-group
enumeration is used.

## Required equalities

The audit requires exact set equality between:
- the 17,280 Weyl-orbit simplex facets; and
- the independently enumerated 17,280 graph K8 cliques.

It then requires every graph K4 to occur in the simplex-cell family, with
exactly five simplex cells containing each K4.

The incidence counts are:

- 17,280 simplex cells, each containing 8 vertices, 28 edges, and 70 K4s;
- 576 simplex cells per root vertex;
- 72 simplex cells per Gosset graph edge;
- 241,920 global K4s;
- 4,032 K4s per root vertex;
- 216 K4s per graph edge;
- 5 simplex cells per global K4.

The central double count is:

    17,280 * C(8, 4) = 241,920 * 5
    1,209,600 = 1,209,600

This is a local-to-global incidence reconciliation between two distinct
constructions: a Weyl-orbit cell-facet construction and exact graph-clique
enumeration. The equality is checked at the set level, not merely by matching
cardinalities.

## Reproduction

    python -m unittest tests.test_gosset_k8_k4_reconciliation -v
    PYTHONPATH=. python experiments/gosset_k8_k4_reconciliation.py

## Scope

A passing result establishes these finite combinatorial equalities for the
declared E8 root model. It does not certify the 8-orthoplex orbit, prove a
global Delaunay tessellation or non-overlap theorem, formalize the result in
Lean, or validate a physical interpretation.
