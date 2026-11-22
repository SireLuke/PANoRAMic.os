# NS–ABOM–E8–LEECH–EQBIT-002 — Valdora seat

**Status:** independent implementation of the merged preregistered ablation protocol; no run results are included in this commit.

## Purpose

This seat implements the analysis and control families in the merged preregistration using the existing PANoRAMic.os module contracts. It does not modify the frozen Navier–Stokes results or the source implementations of ABOM, E8, Leech, or flip-eqbit.

The experiment reports separate typed outputs and hashes, rather than a synthetic score that implies the modules share a common observable.

## Repository sources used

- NS-EVIDENCE-001 frozen nine-case Cosmo snapshot.
- Existing ABOM V8 sample and Fermi-channel adapter.
- Canonical exact Fraction-valued E8 root generator.
- Existing Gosset graph reconstruction and GF(2) cut-rank primitives.
- Existing Leech basis, Golay, and minimal-shell certificate.
- Merged NS–ABOM–E8–LEECH–EQBIT-002 preregistration.
- Supporting contracts in pan-fractal-kernel and the FGHCL/Azabith repository reinforce the V8 coordinate order (h,R,u,d,tau,chi,s,f), typed state/normalization boundaries, and the distinction between V8 and E8.

## Controls implemented

1. Ten or more fixed seeds with raw GF(2) cut-rank samples for random antipodal transversals and arbitrary balanced 120|120 partitions. Defaults are 10 seeds by 1,000 samples per family.
2. Fixed-point-free antipodal involution and graph-automorphism checks before the antipodal split is accepted.
3. Vertex-relabeling invariance check.
4. Degree-preserving double-edge-switch graph null, explicitly not assumed to preserve spectrum or Gosset incidence.
5. Module-removal configurations: full, minus ABOM, minus E8 comparison, minus Leech, minus flip-eqbit, and NS-only. These are output-availability ablations; no shared measurable observable currently links all modules.
6. ABOM input controls: frozen dimensionless ET probe sequence, zero probe, seeded permutation, independent seeded shuffle, and range-matched uniform random sequence. Outputs are retained channel-by-channel.
7. Exact E8 root-set hash equality between the canonical Fraction implementation and ABOM's floating compatibility view; explicit E8-root/Gosset-vertex bijection rather than count equality alone.
8. Full Leech basis/Golay/minimal-shell audit called through the existing implementation.
9. Provenance: repository commit, source-file SHA-256 hashes, Python/platform/NumPy metadata, UTC time, run parameters, and module-output hashes.

## Run

From the repository root:

    python -m unittest tests.test_ns_abom_e8_leech_eqbit_002_valdora -v
    python -m experiments.ns_abom_e8_leech_eqbit_002_valdora.runner --samples-per-seed 1000 --seed-count 10 --seed 20261121 --rewire-attempts 25000 --output experiments/ns_abom_e8_leech_eqbit_002_valdora/results.json

The default randomized partition stage stores 20,000 raw cut-rank samples. The Leech audit explicitly checks the 24-dimensional basis and all 196,560 minimal vectors; runtime should be measured and recorded rather than guessed.

## Interpretation fences

- The nine NS cases remain smooth finite-time benchmarks; no regularity or blow-up inference is made.
- ET enters ABOM as a dimensionless probe. No physical energy units or coupling are inferred.
- V8 state coordinates are not E8 root coordinates. E8 rank 8 and Leech rank 24 remain distinct mathematical objects.
- The E8/Gosset correspondence is an explicit coordinate-set bijection; it does not identify the Leech lattice with either object.
- The flip-eqbit cut rank is an exact graph-state invariant for the declared graph and bipartition, not physical quantum dynamics or hardware.
- NS_EQBIT remains NOT_COUPLED.
- Passing software checks is not physical validation.

## Evidence state

Implementation and tests are provided here. A repository checkout and the actual commands above must run before a result file or validation claim is added. Cosmo's phase-two results, once their immutable artifact/commit is identified, should be compared only after this seat's outputs are frozen.

Authored-by: OpenAI (ChatGPT bench)
