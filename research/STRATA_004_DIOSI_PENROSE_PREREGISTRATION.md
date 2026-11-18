# STRATA-004: Diósi–Penrose mass-density audit (pre-registration)

Status: protocol proposal; no calculation or empirical result is claimed. Protocol STRATA-0.1. Claim class: bounded model-consistency and constraint audit, not evidence that objective collapse occurs.

## Model layers and evidence grades

| Layer | Core statement | Grade |
|---|---|---|
| GRW/CSL | Stochastic modifications of quantum dynamics with localization/noise kernels | Established research model family; not established as nature |
| Diósi–Penrose | Distinct mass distributions have gravitational self-energy scale E_G and characteristic tau approximately hbar/E_G | Hypothesis/model estimate; smearing and conventions must be declared |
| Oppenheim programme | Classical spacetime coupled to quantum matter with stochasticity and consistency constraints | Theoretical programme; not equivalent to DP |
| Clock/time-fuzziness bounds | Bounds depend on a specified noise model and operational clock assumptions | Model-specific constraints, not universal observations |

## Computable core

Define the signed density difference first: delta_rho(x) = rho_1(x) - rho_2(x).

E_G = (G/2) integral d^3x d^3y delta_rho(x) delta_rho(y) / |x-y|.

This is the positive Newtonian self-energy functional of the difference distribution. Do not replace delta_rho with (rho_1+rho_2)/2, and do not compute two self-energies separately and call their sum the DP difference energy. State kernel, boundary conditions, units, smearing, and numerical method. tau_DP = hbar/E_G only after E_G is finite, positive, and converged. Identical configurations give E_G=0 and tau=infinity.

## Smearing and exclusion rule

An unsmeared point-particle, parameter-free implementation is an excluded comparison model, not an acceptable candidate. Every finite calculation declares its smearing kernel and length r_C (or equivalent cutoff), normalization, and sensitivity sweep. Do not add a cutoff after seeing the result. Donadi et al. underground-radiation constraints must be applied to the relevant parameter-free/unsmeared model; do not claim all smeared DP/CSL variants are excluded.

## Preregistered experiments

### A. Displaced uniform sphere

Use a uniform sphere of mass M and radius R, with branch densities displaced by d=R. Compute the overlap-aware double integral using the same signed difference density. Compare with an analytic overlap result and an independent Fourier-space integral. For the sharp uniform sphere, the reference coefficient for this convention is E_G = 0.5 G M^2/R at d=R. For an unsmeared uniform sphere, I_self=6 M^2/(5R) and I_cross=7 M^2/(10R), hence E_G=G(I_self-I_cross)=G M^2/(2R). This coefficient is an analytic overlap result for this exact geometry and convention, not a universal constant. Repeat with declared smearing and sweep r_C/R. Require analytic/numerical agreement, grid convergence, dimensional consistency, and correct limiting behavior.

### B. Taijitu occupancy difference

Only after A passes, define explicit normalized lobe densities rho_1(x;N) and rho_2(x;N), then delta_rho=rho_1-rho_2. N must change physical mass allocation under a stated conservation rule; it cannot merely relabel colour or pixels. Evaluate E_G(N), tau(N), justified N↔1-N symmetry, and the N=1/2 identical-configuration limit. The Fermi disk area identity does not itself define a DP mass density.

### C. Gosset-shell configurations

Only after A and B are independently validated, construct densities on explicitly defined Gosset 4_21/E8-associated shell locations. E8 supplies geometry, not a mass law. Compare against matched randomized and structure-preserving controls with equal total mass, radial profile, smearing, and pair-distance statistics where feasible. Record geometry construction/version; hyperoctahedral geometry is auxiliary only.

## STRATA controls and evidence

- Provenance: DOI/version, license, retrieval timestamp, SHA-256, inclusion/exclusion, units, and preprocessing for empirical inputs.
- Scales: at least three meaningful spatial resolutions and an r_C sensitivity sweep.
- Representations: direct real-space quadrature and independent Fourier-space evaluation.
- Controls: zero-difference identity; equal translated configurations; randomized mass placements; structure-preserving permutations; matched non-Gosset geometry as auxiliary control.
- Baselines: analytic uniform-sphere solution, Newtonian self-energy cross-check, and numerical convergence baseline.
- Leakage: freeze geometry, mass, smearing, tolerances, and parameter grid before target/control comparison.
- Uncertainty: propagate M, R, d, r_C and measured density uncertainty; report discretization error separately.
- Held-out: reserve a displacement ratio and smearing setting from calibration.
- Independent review: second implementation or reviewer checks density difference and integral convention.

Every dimension gets pass/fail/inconclusive/not_tested. A passing software test validates implementation only. A calibration pass does not establish collapse physics. Excluded parameter regions remain reported.

## Architecture boundaries

PAN V8 remains (h,R,u,d,tau,chi,s,f), with chi in [-1,1] and other coordinates in [0,1]. Do not map DP lifetime into tau without a separately declared observable and units. Janus Hydra is a translator, never validation authority. UHFE and UDFE remain distinct. No result is promoted into V8, UHFE/UDFE, or production runtime. STRATA stays outside boot. Gosset 4_21/E8 is primary only for the shell subexperiment.

## Execution order

1. Implement analytic sphere calibration and independent real/Fourier numerical formulations.
2. Add tests for density-difference sign, zero difference, positivity, dimensional scaling, and convergence.
3. Validate smearing kernels and Donadi-constrained parameter regions.
4. Freeze Taijitu density definitions and occupancy conservation before calculating tau(N).
5. Add Gosset-shell configurations and matched controls.

## References to verify at execution time

- Diósi, Models for universal reduction of macroscopic quantum fluctuations, Phys. Rev. A 40 (1989), DOI 10.1103/PhysRevA.40.1165.
- Penrose, On gravity's role in quantum state reduction, Gen. Rel. Grav. 28 (1996), DOI 10.1023/A:101888261697331.
- Donadi et al., Underground test of gravity-related wave function collapse, Nat. Phys. 17 (2021), DOI 10.1038/s41567-020-1008-4.
- Oppenheim, A postquantum theory of classical gravity?, Phys. Rev. X 13 (2023), DOI 10.1103/PhysRevX.13.041040.

Bibliographic inclusion is not a claim that every model variant or experimental bound has been independently rederived here. Confirm assumptions, versions, and exclusions in the execution record.