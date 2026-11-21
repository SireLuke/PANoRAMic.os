# NS-EVIDENCE-001 — periodic incompressible Navier–Stokes baseline

**Status:** computational benchmark only. Not a proof of global regularity or a claim about the Clay Millennium problem.

## Question and claim class

Can an inspectable Fourier pseudospectral implementation recover a known exact incompressible flow and produce auditable 3D Taylor–Green energy, enstrophy, divergence, and dissipation diagnostics? Claim class: numerical experiment plus software tests. No physical experiment, theorem, blow-up test, or global smoothness inference is made.

## Model and numerical method

Unforced incompressible equations on periodic box [0, 2π)^d:

∂t u + (u · ∇)u = −∇p + ν Δu,   ∇ · u = 0.

Parameters: ν=0.01; d=2,3. Fourier pseudospectral derivatives, 2/3 dealiasing, Leray projection, classical RK4. Taylor–Green initial fields. The 2D case has exact solution u(t)=exp(−2νt)u(0); 3D is a finite-time benchmark, not an exact-solution comparison.

Diagnostics: kinetic energy E=1/2⟨|u|²⟩; viscous dissipation D=ν⟨|∇u|²⟩; enstrophy Ω=1/2⟨|ω|²⟩; max absolute spectral divergence; energy-balance residual E(0)−E(T)−trapz(D). The residual includes trapezoidal quadrature error and is not a solver-error certificate.

## Results at T=0.1

| d | N | dt | steps | E(0) | E(T) | Ω(T) | max div(T) | balance residual |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 16 | .002 | 50 | .25 | .24900199733599987 | .49800399467199963 | 1.48e−15 | −5.34e−13 |
| 2 | 24 | .002 | 50 | .25 | .24900199733599238 | .49800399467198464 | 3.16e−15 | −5.27e−13 |
| 2 | 32 | .002 | 50 | .25 | .24900199733599893 | .49800399467199796 | 3.99e−15 | −5.33e−13 |
| 3 | 16 | .001 | 100 | .125 | .12425198808087563 | .3731414453839292 | 1.51e−15 | −1.30e−11 |
| 3 | 24 | .001 | 100 | .125 | .12425198808086467 | .3731414453838998 | 3.84e−15 | −1.29e−11 |
| 3 | 32 | .001 | 100 | .125 | .12425198808087455 | .3731414453839298 | 4.53e−15 | −1.30e−11 |

2D relative RMS error against the exact solution: 4.26e−15, 1.19e−14, 2.64e−15 for N=16,24,32. This is near roundoff for an exactly resolved low-mode field; it does not establish general convergence.

At 3D N=16, T=.5, halving dt .004→.002→.001 gave E(T)=.12127471447955145, .12127471447955157, .1212747144795577; energy residual −9.72e−10, −2.43e−10, −6.08e−11. This is a temporal sensitivity check for a smooth finite-time case, not a singularity study.

## Reproduction

From repository root: python -m experiments.navier_stokes.ns_spectral --output experiments/navier_stokes/ns_evidence_001_results.json

Tests: python -m unittest tests.test_ns_spectral -v

Requires NumPy. JSON records parameters and diagnostics. Timing is not an accuracy metric.

## Limitations and next gates

The 2D exact solution is the within-domain recovery gate. 3D decay, divergence, enstrophy, and energy balance are diagnostics, not regularity bounds. Initial data are smooth, low-mode, periodic, and finite-time; no boundary layer, high-Reynolds-number, turbulent, or near-singular regime is tested. N=16/24/32 demonstrates consistency for this resolved low-mode case, not asymptotic convergence for general data. Independent implementation/review remains outstanding. Before coupling to Menger, Gosset/E8, V8, Janus Hydra, or Fermi-sea descriptors, freeze this baseline, add higher-mode/manufactured cases, compare a second solver, and preregister appropriate nulls under GL-001. Any theorem-level claim requires a separate rigorous-analysis track. No numerical run here proves global 3D existence, uniqueness, or smoothness.

## Provenance

Source: experiments/navier_stokes/ns_spectral.py; tests: tests/test_ns_spectral.py; output: experiments/navier_stokes/ns_evidence_001_results.json. Preserve commit SHA, environment, and failures.

Authored-by: OpenAI (ChatGPT bench)
