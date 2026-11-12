# Gaussian-splat representation of hydrogenic orbitals (Library of Alexandria "matter" track, step 1)

**Status:** reference generator and data; a rendering aid for an accurate density, not a physical claim.
**Adds:** `experiments/matter_splats/orbital_splats.py`, `orbital_splats.json`, `tests/test_matter_orbital_splats.py`, a workflow, this note. Stacked on `research/qwave-hydrogen-baseline`. No existing module is changed.

## What it does

For real hydrogen orbitals (1s, 2s, 2p_z, 3s, 3p_z, 3d_z2, 3d_xz, 3d_x2-y2; atomic units, infinite nuclear mass) the exact density |psi|^2 is sampled on a 72^3 grid and fitted with a weighted Gaussian mixture (EM, full covariances, lobes of opposite sign fitted separately). Each splat is `{mean, cov, weight, sign}`: weights sum to 1 (probability), sign is the lobe sign for display hue. The exact radial functions come from `core/abom_v8/hydrogen_baseline.py`; the vectorised copies used here are tested against it to 1e-12.

## Fit quality against the exact density

| State | Splats | Relative L2 error | Mean-radius error | Density at radial nodes / max |
|---|---|---|---|---|
| 1s | 12 | 7.2% | 0.09% | none |
| 2s | 29 | 8.6% | 0.03% | 0.025 |
| 2p_z | 24 | 6.9% | 0.06% | none |
| 3s | 28 | 17.8% | 0.36% | 0.41, 0.033 |
| 3p_z | 24 | 8.3% | 0.04% | 0.013 |
| 3d_z2 | 24 | 13.0% | 0.03% | none |
| 3d_xz | 24 | 11.0% | 0.07% | none |
| 3d_x2-y2 | 24 | 10.5% | 0.08% | none |

Dropped tail mass is below 3e-5 per state and weights are renormalised to sum to 1 exactly. Mean radius tracks the exact value 3/2 n^2 - l(l+1)/2 to under 0.4%.

## Limits (read before using it in a renderer)

- **Radial nodes are smeared.** Gaussians cannot make a sharp nodal sphere; the fitted density at a node is 1 to 3% of its maximum for most states and **41% for the inner node of 3s**. A viewer should not present these as exact node surfaces. More splats or a shell-aware basis would be needed.
- The density is accurate; the electron is a probability cloud, not a particle with a trajectory. Real orbital sign is shown as hue, which is a display choice.
- Hydrogenic orbitals only. Multi-electron atoms need orbitals from a many-body or Hartree-Fock calculation, not this closed form.
- No V8 coordinate mapping is imposed. Any mapping of V8 coordinates to splat colour, opacity or size must be declared as a display choice, not a physical identification.

## Reproduce

`python experiments/matter_splats/orbital_splats.py experiments/matter_splats/orbital_splats.json` (about a minute); `python -m unittest tests.test_matter_orbital_splats -v`.

## Next steps (matter track)

1. `MatterNode` schema in `core/library/types.ts` and a NIST-sourced element table with provenance and validation.
2. Shell-aware splat basis to resolve radial nodes; Hartree-Fock-quality densities for multi-electron atoms.
3. Molecular splats for a small curated set with geometry checks, then the WebGL viewer.
