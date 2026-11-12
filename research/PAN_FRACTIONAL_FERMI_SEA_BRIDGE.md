# PAN fractional Fermi sea bridge (FFS-001)

## Why this is connected to the existing PAN work

The existing ABOM-v8 model already implements a Fermi-Dirac logistic occupation,
a complementary hole fraction, and a signed contrast. That is a meaningful
precursor: it gives us an occupation channel and a number-complementary channel.
But it is not the newly reported fractional Fermi sea.

The 2026 FFS work describes a different object: a one-dimensional Bose gas
prepared by interaction cycles through repulsive Tonks-Girardeau and attractive
super-Tonks-Girardeau regimes. At the non-interacting endpoint, ideal homogeneous
reference states have a box-like momentum occupation:

- cycle index ell=2: n(k)=1/2 for |k|<2 k_F
- cycle index ell=4: n(k)=1/4 for |k|<4 k_F

The density is conserved:
`integral dk/(2 pi) n(k) = k_F/pi`.

This means the occupied momentum interval broadens by ell while its fractional
height falls by 1/ell. The fractional occupancy is not a finite-temperature
Fermi-Dirac logistic distribution, and the atoms remain bosons. "Fermi sea"
refers to emergent quasiparticle/rapidity organization and generalized
exclusion-statistics structure.

## Implemented reference model

`core/abom_v8/fractional_fermi_sea.py` implements:
- ideal homogeneous ell=2 and ell=4 box profiles;
- number-density normalization;
- Fourier transform to normalized one-body correlation
  `g1(x)=sin(ell*k_F*x)/(ell*k_F*x)`;
- first correlation zero `x0=pi/(ell*k_F)`;
- a side-by-side conventional Fermi-Dirac comparator;
- explicitly tentative V8 observable suggestions without filling V8 values.

The code is an analytic endpoint reference, not a generalized-hydrodynamics
simulation, Bethe-ansatz solver, trap average, or experimental data fit.

## Relationship to existing UHFE/UDFE and V8

The current `fermi_occupation` and `fermi_channels` in
`core/abom_v8/abom_v8_model.py` implement a conventional Fermi-Dirac
occupation `n=1/(exp((E-mu)/kT)+1)`, hole complement `1-n`, and signed
contrast `n-(1-n)`. These can remain useful baseline channels.

The new FFS model adds a separate, explicitly named fractional rapidity/
momentum occupation profile. It must not overwrite or be mislabeled as the
Fermi-Dirac baseline. The FFS parameter ell is not itself the PAN V8
recursive-depth coordinate R.

Suggested observational interface:
- h: phase/coherence estimator from measured correlations;
- R: scale dependence of correlation structure;
- d: entropy production measured independently, not inferred as 1-n;
- tau: measured state lifetime/persistence;
- s: a declared information/occupation estimator;
- f: interaction-ramp forcing protocol and cycle count;
- u and chi: unassigned until a defensible signed observable is defined.

Janus Hydra may translate these observables into V8 representations, but it
must not invent missing observables. UHFE/UDFE remain the paired formation/
dissolution representations, not the FFS itself.

## Experimental protocol facts to preserve

The published experimental preprint reports:
- one-dimensional cesium Bose gas;
- interaction cycles through repulsive TG and attractive sTG regimes;
- ell=2 and ell=4 endpoint states;
- FFS plateaus 1/2 and 1/4, with cutoffs 2 k_F and 4 k_F;
- Friedel oscillations in first-order correlations;
- GHD modeling including trap, time-dependent interactions and finite
  temperature;
- reverse-cycle atom loss / irreversibility, including Bethe-string formation.

The PRL theory paper predicts the fractional-sea critical states. The companion
experimental realization is available as arXiv:2602.17657 and Zenodo dataset
10.5281/zenodo.18697242. Check publication status at time of citation rather
than treating preprint status as peer-reviewed.

## Next validation stage

1. Add digitized experimental momentum-distribution and correlation data from
   Zenodo with source checksums and metadata.
2. Compare ideal homogeneous box profile, trap-averaged Thomas-Fermi profile,
   and reported GHD outputs.
3. Fit ell=2 and ell=4 with held-out observables; compare against thermal Bose,
   thermal Fermi-Dirac, and ordinary Tonks-Girardeau baselines.
4. Only then add a Lieb-Liniger/GHD ramp solver or import a validated reference
   implementation. Do not fake the dynamics by interpolating ell.
5. Run STRATA controls: multiple scales, alternate representations, observer/
   extraction sensitivity, randomized profiles, and preregistered held-out
   prediction.

## References

- Bastianello et al., *Exotic Critical States as Fractional Fermi Seas in the
  One-Dimensional Bose Gas*, Physical Review Letters 136, 230402 (2026),
  DOI 10.1103/j3s5-gjpf.
- Zeng et al., *Realization of fractional Fermi seas*, arXiv:2602.17657 (2026),
  https://arxiv.org/abs/2602.17657.
- Experimental data: https://zenodo.org/records/18697242.
- Generalized Hydrodynamics: A Perspective, Physical Review X 15, 010501
  (2025), DOI 10.1103/PhysRevX.15.010501.
