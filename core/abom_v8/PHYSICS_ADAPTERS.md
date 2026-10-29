# ABOM-v8 physics adapter notes

## Marie Curie / radioactivity
The standard exponential decay law is:

```math
N(t) = N0 exp(-lambda t)
A(t) = A0 exp(-lambda t)
lambda = ln(2) / t_half
```

Here lambda has inverse-time units and t must use matching time units. Curie's historical work on radioactivity helped establish the field, but there is no single unique “Marie Curie formula”; this adapter implements the general radioactive decay law. The half-life example is an illustrative normalized test, not a measurement of a specific isotope.

## Bose-Einstein condensate (BEC)
The full mean-field Gross-Pitaevskii equation is:

```math
i hbar d(psi)/dt = [-hbar^2/(2m) nabla^2 + V(r) + g |psi|^2] psi
```

The module currently tests only a homogeneous stationary special case with V=0, repulsive interaction g>0, and chemical potential mu>0:

```math
|psi| = sqrt(mu/g)
residual = -mu psi + g |psi|^2 psi = 0
```

This is an analytic check, not a numerical spatial solver for the full PDE. A full solver needs a domain, boundary conditions, physical units, particle mass, interaction parameter, and numerical discretization.

## Bob Lazar claims
No validated, reproducible propulsion equation from Bob Lazar is available in the scientific record that can be responsibly plugged in as an established law. Do not invent one. If a particular equation or diagram is provided, it can be encoded as a hypothesis, with assumptions and provenance marked, then tested for dimensional consistency and numerical behavior. Such a test would not establish the claimed propulsion mechanism as real.

## V8 projection
The map_scalar_to_v8 function is deliberately just a named-channel projection. It does not pretend a scalar equation naturally fills all eight coordinates. Before a model is expanded across V8, define each coordinate's semantics, units, transformations, and invariants.

## Validation status
The adapters and tests are committed on the abom-v8-integrated-field branch. Test files are included but have not yet been executed here; no passing test status is claimed.
