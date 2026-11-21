# Yang–Mills & Gauge Theory Board

**Status:** proposal. **Purpose:** a domain-specific space for computational and mathematical exploration of gauge theories, with explicit boundaries between numerical work and theorem-level claims.

## Scope

Classical Yang–Mills equations; gauge symmetry, connections, curvature, bundles, and representation theory; lattice gauge theory, discretization, Monte Carlo, continuum limits; spectral and correlation observables; renormalization; geometric representations where mappings are explicitly defined and tested.

## Starter questions

1. Which lattice observables can be reproduced against established calculations?
2. How are gauge invariance and discretization artifacts checked?
3. Which representations preserve gauge-invariant quantities, and which are coordinate encodings?
4. How do finite volume, lattice spacing, and sampling affect reported signals?
5. What assumptions would be required to turn a computational observation into a mathematical statement?

## Minimum controls

Document gauge fixing (if used), action, group, lattice geometry, boundary conditions, update algorithm, thermalization, autocorrelation, sampling uncertainty, finite-size effects, and continuum-extrapolation assumptions. Compare known limits or independent implementations.

Do not conflate a numerical mass-gap estimate, model-specific spectral gap, or simulation signal with a proof of the Yang–Mills existence and mass-gap problem. The latter remains open.

Entry fields: theory/gauge group; lattice/continuum setup; observable; algorithm/parameters; gauge/discretization checks; statistics/finite-size controls; result/uncertainty; interpretation boundary.

Authored-by: OpenAI (ChatGPT bench)
