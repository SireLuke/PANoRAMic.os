# Motion-to-Form: classical wave geometry baseline

Status: isolated research module. This milestone establishes reproducible
classical mathematics for wave interference and standing-wave mode formation.
It does not implement Walter Russell's Light Wave Mechanics as established
physics or unify classical waves, quantum mechanics, general relativity, and
string theory.

Implemented: complex scalar plane waves; phase-preserving superposition;
general two-wave intensity; equal-amplitude constructive/destructive limits;
path-difference/phase conversion; small-angle Young fringe spacing; normalized
Dirichlet sine modes; normalized Neumann cosine modes including the zero mode;
numerical inner-product checks; and 1D interval mode-frequency scaling.

Run from the repository root:
    python -m unittest tests.test_wave_geometry -v
    PYTHONPATH=. python experiments/wave_geometry_audit.py

QWAVE v0 remains SI photon relations and temporal measurement metadata, not a
wave dynamics solver. The hydrogen baseline remains a separate stationary
Schrodinger reference. This classical module does not merge those models.
ABOM V8 remains a modular mathematical composition, not a validated unified
physical law. V8 coordinates and Janus Hydra semantics are untouched.

Explicit exclusions: no claim that interference destroys energy; no inference
from classical modes to particle identity; no identification of Russell's
paired-tone vocabulary with established field variables; no Schwarzschild/
Kruskal implementation; no string-theory quantization; no E8/Gosset projection
imposed on the wave equations; no GPU optimization before profiling.
