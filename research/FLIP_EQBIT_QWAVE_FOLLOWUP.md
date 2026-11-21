# Flip-eqbit follow-up: cut-rank distribution and QWAVE boundary

**Status:** proposed independent follow-up to merged PR #117. The first-pass
112-ebit antipodal-cut result is preserved as the baseline, not rewritten.
This packet adds a reproducible distributional audit and clarifies where QWAVE
can and cannot contribute.

## 1. Why two control families?

The first pass compared the antipodal cut (rank 112) with one seeded arbitrary
balanced cut (rank 95). One draw cannot establish typicality, extremality, or
a tail probability.

This follow-up compares the fixed antipodal cut against two controls:

1. **Random transversals:** choose exactly one member of every antipodal pair
   for the left side, with its opposite on the right. This preserves the
   pair-splitting condition and tests whether the chosen orientation matters.
2. **Arbitrary balanced cuts:** choose any 120 of the 240 vertices for the
   left side. This tests whether the antipodal-pair structure itself is
   associated with a different cut-rank distribution.

The script reconstructs E8 roots and the Gosset graph from exact integer
coordinates, checks 240 vertices / degree 56 / 6,720 edges / 120 antipodal
pairs, and computes cut ranks over GF(2). The default is 1,000 samples per
control with a fixed seed. Output reports min, 5th percentile, median, 95th
percentile, max, mean, and empirical comparison fractions.

A sampled maximum is not a proof of a global maximum. Empirical fractions
are not exact tail probabilities. The script does not claim that the
antipodal cut is extremal or that the random controls represent a uniform
physical ensemble.

## 2. What QWAVE contributes — and what it does not

The repository's QWAVE v0 module is explicitly an SI photon-relations and
temporal-measurement-metadata module, not a quantum solver. It provides
frequency/wavelength/energy conversions and metadata comparisons to derived
Planck reference scales. It deliberately does not impose Planck time as a
measurement floor.

The flip-eqbit graph-state phase is currently the discrete CZ/stabilizer
phase in a mathematical graph-state construction. The E5 non-commutation
count is an operator-algebra result. Neither supplies a calibrated energy,
Hamiltonian, angular frequency, detector, or physical time evolution.
Therefore QWAVE cannot currently turn E5 into a physical oscillation rate or
a time-evolution prediction. Calling the adjacency contribution "phase"
does not make it the same object as the time-dependent complex phase of a
Schrodinger wavefunction.

The existing hydrogen baseline is useful as a separate reference: it stores
complex wavefunction, amplitude, phase, density, and probability current as
distinct fields and checks stationary-state phase evolution. It does not
impose E8/Gosset structure on hydrogen, and its documentation reports that
prior projected-E8 hydrogen comparisons found no geometric advantage.
It should remain a control/reference, not evidence for the flip-eqbit
construction.

## 3. A defensible future QWAVE bridge

QWAVE becomes relevant to a dynamical extension only after an independently
specified Hamiltonian or calibrated interaction energy is supplied. Then a
dimensionless evolution phase can be connected to time through an explicit
model, for example theta = E * t / hbar for a stated energy scale E. The
energy source, units, uncertainty, Hamiltonian, and measured observable must
be declared before fitting. QWAVE may then handle SI conversion and temporal
acquisition metadata; it must not invent E, infer a physical Hamiltonian
from graph adjacency, or treat Planck time as a sampling limit.

Until those prerequisites exist, keep the graph-state calculation static
and exact. No synthetic time axis, Planck-scale sampling, or hydrogen/E8
coupling is justified by the current evidence.

## 4. Run

From the repository root:

    python -m experiments.flip_qubit.cut_rank_audit --samples 1000 --seed 20261121
    python -m unittest tests.test_flip_qubit_cut_rank -v

The script writes flip-eqbit-cut-rank-audit.json in the working directory.
It has no third-party runtime dependencies.

## 5. Evidence grading and fences

- E8/Gosset contract and GF(2) cut ranks: exact finite computation, subject
  to independent implementation/rerun.
- Distribution summaries: reproducible sampled statistics, conditional on
  the declared seed and sampling scheme.
- Any claim about a useful physical qubit, physical dynamics, quantum
  hardware, universality, or new physics: not tested and not promoted.
- V8 remains cartography; QWAVE remains measurement metadata / SI relations;
  the hydrogen baseline remains a separate stationary-state reference.
