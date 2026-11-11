# QWAVE v0 — Planck-scale and measurement metadata bridge

## Status and boundary

QWAVE v0 is a small, standard-library-only SI relations and temporal metadata
module under `core/abom_v8/qwave.py`. It is **not** a quantum dynamics engine,
wavefunction solver, or claim of new physics. The existing ABOM-v8 physics
adapters remain separate and authoritative for the equations they implement.

## Implemented in v0

- SI-defined (c) and (h), with (hbar=h/(2\pi)); measured (G) is
  recorded as a nominal constant in the module.
- Derived Planck length, time, energy, and reciprocal-time frequency.
- Vacuum photon relations from frequency or wavelength:
  (E=hf=\hbar\omega), (\lambda f=c), and (\tilde\nu=1/\lambda).
- Temporal metadata for physical timestamp, sample interval, instrument
  resolution, and optional timing uncertainty.
- Dimensionless comparisons against Planck time, explicitly labelled as
  reference-scale comparisons.

## Critical interpretation rule

Planck time is a derived natural unit,
(t_P=\sqrt{\hbar G/c^5}\). It is **not** asserted to be a demonstrated
minimum measurable interval, a universal instrument-resolution limit, or a
mandatory simulation timestep. The API deliberately accepts positive sample
intervals below (t_P) and reports the ratio without clipping or rejection.

Likewise, (G) has experimental uncertainty. The current constant is a
nominal value and does not yet propagate CODATA uncertainty. A later version
should pin a CODATA release and carry source/version/uncertainty metadata.

## Deferred QWAVE work

1. Preserve the raw complex wavefunction \(\Psi\) and its representation
   (basis/grid, normalization, boundary conditions, units, solver provenance).
2. Derive and store amplitude, phase, probability density, and probability
   current as distinct fields; never replace or overwrite raw \(\Psi\).
3. Define observation metadata separately from the underlying state:
   detector response, integration window, sampling cadence, timing calibration,
   uncertainty/covariance, and acquisition provenance.
4. Add independently validated Schrödinger / stationary-state baselines before
   any V8 or Gosset-derived projection is compared.
5. Treat V8 mappings as candidate derived features only. Do not impose E8 or
   Gosset symmetry on hydrogen/photon systems absent an empirical or
   mathematical justification.

## Validation

Run:

```bash
python -m unittest tests.test_qwave -v
```

The tests cover SI dimensional identities, reciprocal frequency/time relation,
photon energy/wavelength consistency, invalid input rejection, and the
non-enforcement of a Planck-time measurement floor.
