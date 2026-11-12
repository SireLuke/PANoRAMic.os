# QWAVE hydrogen stationary-state baseline

**Status:** isolated, standard-library-only reference module; not a physical claim.
**Adds:** `core/abom_v8/hydrogen_baseline.py`, `tests/test_hydrogen_baseline.py`, a focused workflow, this note. `qwave.py` and every existing module are unchanged.

## Why

`docs/QWAVE_PLANCK_SCALE_ROADMAP.md` defers "independently validated Schrodinger / stationary-state baselines before any V8 or Gosset-derived projection is compared" (item 4) and asks that amplitude, phase, probability density and probability current be stored as distinct fields (item 2). This module is that baseline for hydrogen. It was developed alongside the `pan-fractal-kernel` hydrogen experiments (`hydrogen_shell_modes.py`), whose exact radial and harmonic functions it mirrors without numpy.

## What it provides (atomic units, infinite nuclear mass)

- Normalised radial functions R_nl for n <= 3 and (4, 2); exact radial node radii (count n - l - 1; includes the 12 a0 node of 4d).
- Complex spherical harmonics (Condon-Shortley) for l <= 2 and the stationary state psi_nlm(r, theta, phi, t) = R_nl Y_l^m exp(-i E_n t), E_n = -1/(2 n^2) hartree.
- `fields(...)`: psi, amplitude, phase, density, and the azimuthal current J_phi = m |psi|^2 / (r sin theta) kept as separate quantities.
- An H-alpha consistency check through `qwave.photon_from_frequency`.

## Validation (all in `tests/test_hydrogen_baseline.py`)

Radial normalisation to 1e-7; node counts and node values; orthonormality of the nine harmonics by quadrature; the 54.7356 degree conical node of Y_20; the stationary-state time phase; J_phi against a numerical finite-difference of Im(psi* grad psi); consistency among amplitude, density and psi; input validation.

## Notes and limits

- H-alpha: the Bohr-level route (hartree, infinite nuclear mass) gives 656.11 nm; the hydrogen Rydberg constant 1.096775834e7 m^-1 (reduced mass) gives 656.47 nm. They differ by the electron-to-proton mass correction (ratio 1.000545). The kernel `spectroscopy.rydberg_wavelength_m` docstring calls its default "infinite-nuclear-mass", but that constant is the reduced-mass hydrogen value.
- No spin, relativistic or QED corrections; no finite-mass reduced-mass scaling of a0.
- Nothing here imposes E8, Gosset or V8 structure on hydrogen. In `pan-fractal-kernel`, pre-registered comparisons of hydrogen on projected E8 shells found an exact isotropy property of the shells but no geometric advantage for hydrogen-matched scales or node recovery.
