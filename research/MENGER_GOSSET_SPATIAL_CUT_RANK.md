# Menger spatial cut-rank experiment — v0.1

**Status:** exploratory finite-graph result; not physical validation.

## Question

Does a coordinate-aligned spatial partition of the finite 3D Menger
retained-cell face-adjacency graph have a different GF(2) cut-rank profile
from random partitions with the same cardinality?

## Construction

The retained cells use the existing Fractal Kernel rule: at each ternary
digit position, at most one coordinate may equal 1. The graph joins cells
sharing a face, with no wrap-around. A spatial partition places cells with
x-coordinate below half the grid side on the left. Each random control samples
exactly the same number of vertices for its left side.

The cut rank is computed exactly over GF(2). For a graph state defined by
placing CZ gates on graph edges, this rank equals the graph-state entanglement
across that cut. Here it is used strictly as a graph invariant/comparator;
no physical qubits or state preparation are claimed.

## Preliminary results

Using 1,000 random controls per level and seed 20261121 + level:

| Level | Vertices | Edges | Spatial cut sizes | Spatial rank | Random rank min / median / max |
|---|---:|---:|---:|---:|---:|
| 1 | 20 | 24 | 8 / 12 | 4 | 4 / 7 / 8 |
| 2 | 400 | 672 | 192 / 208 | 16 | 139 / 153 / 166 |

At level 1, 3/1,000 random cuts had rank <= the spatial cut. At level 2,
0/1,000 did. These are empirical frequencies under the stated sampling
scheme, not exact tail probabilities or universal claims.

The low spatial cut rank is consistent with a coordinate cut having a
comparatively constrained graph boundary. It is not evidence of quantum
advantage, physical entanglement, or a unique Menger signature. A random
partition is deliberately a weak geometric control because it destroys
locality; follow-up controls must preserve additional properties.

## Required next controls

1. Compare coordinate planes on all three axes and multiple offsets.
2. Add connected, approximately balanced graph partitions and boundary-size
   matched controls, not only unrestricted random subsets.
3. Compare retained-cell, void-cell, and interface/boundary graphs separately.
4. Repeat at level 3 only after profiling memory/runtime and preregistering
   sampling; level 3 has 8,000 vertices.
5. Compare distributions, not just a single observed cut, and report all
   seeds and failed runs.
6. Keep Gosset's 240-vertex antipodal cut result as a separate baseline. Do
   not compare raw rank magnitudes across different graph sizes as though
   they were normalized observables.

## Reproduction

    python -m experiments.menger_gosset.cut_rank_audit --levels 1 2 --samples 1000 --seed 20261121
    python -m unittest tests.test_menger_spatial_cut_rank -v

The experiment is a new independent implementation of the finite Menger
cell/face graph for this audit. Its level-1 counts are checked against the
existing Menger hand-count. No production V8, QWAVE, or Fractal Kernel
implementation is modified.
