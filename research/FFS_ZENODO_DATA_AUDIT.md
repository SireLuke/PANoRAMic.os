# FFS-002: provenance-checked experimental-data audit

## Dataset

The Zenodo record 10.5281/zenodo.18697242 publishes figure data for Zeng et al.,
*Realization of fractional Fermi seas*. This audit fetches, but does not vendor,
the CSVs for figures 3A, 3B and 3C. Each download is checked against the MD5
digest shown on the Zenodo record before parsing.

| File | Figure | Published MD5 |
|---|---|---|
| figure3A_data.csv | Momentum distributions | 068240a2069550d96d0d302c40cab666 |
| figure3B_data.csv | First-order correlations, linear scale | 2319b4d9cf9114466addc103525cd92d |
| figure3C_data.csv | First-order correlations, log absolute scale | b98af0284338f88a4fb39e8ea82972b4 |

## What the audit computes

- Confirms all three source files match the record's checksums.
- Records row counts and column names.
- Extracts experimental first-order correlation series for ell=0, 2, 4.
- Linearly interpolates measured zero crossings.
- Finds the first negative trough between the first two zero crossings.
- Computes an effective homogeneous-sinc kF from the first zero for ell=2,4:
  `kF_eff = pi / (ell * x_zero)`.

The effective kF is only a diagnostic. The experiment averages over nonuniform
harmonic tubes; the paper explicitly notes that trap and tube averaging smooth
the ideal box profile. Therefore the measured correlations should not be
expected to equal the ideal homogeneous sinc exactly.

## Source-grounded physical context

The experimental paper reports an ideal homogeneous profile:
- ell=2: n(k)=1/2 for |k|<2 kF;
- ell=4: n(k)=1/4 for |k|<4 kF.

The Fourier transform is a cardinal-sine correlation. The actual experiment
uses cesium atoms in an array of 1D tubes, with harmonic confinement and
tube averaging. Its GHD simulation includes the trap, time-dependent
interactions and finite-temperature effects. The published figure CSVs include
experimental points and GHD/analytical curves.

## Boundaries

This script is a reproducible data-provenance and feature-extraction audit.
It does not reconstruct the GHD solver, re-fit the experimental model, process
raw time-of-flight absorption images, or infer V8 coordinates. Supplied
uncertainties are preserved in source files but not propagated into a fitted
parameter confidence interval.

## Reproduction

`python -m unittest tests.test_ffs_zenodo_audit -v`
`python experiments/fractional_fermi_sea/zenodo_dataset_audit.py`

Source: https://zenodo.org/records/18697242
Paper: https://arxiv.org/abs/2602.17657
