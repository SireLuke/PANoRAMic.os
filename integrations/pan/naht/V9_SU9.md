# PAN V9, NAHT, and SU(9) integration contract

## V9 state

PAN V9 extends the existing eight real coordinates with one finite coordinate named xi:

(h, R, u, d, tau, chi, s, f, xi)

The eight V8 coordinates keep their existing names and values. Each V9-to-NAHT projection must declare a stable identifier, version, xi semantics, and units. xi may represent a caller-defined scale, phase, or evolution parameter; this interface does not assign it universal physical meaning or update it automatically.

The PAN adapter projects V9 to NAHT's three real channels (q_r, q_e, q_p). That reduction is explicit, versioned, read-only, and recorded in provenance.

## SU(9) action

SU(9) acts in its fundamental representation on nine complex amplitudes. A nine-component real PAN vector is not by itself a complex SU(9) state. The integration therefore requires a versioned caller-supplied encoder from V9 to C^9, validates each 9x9 matrix for unitarity and determinant one, applies the action, then requires a separately versioned projection from C^9 to NAHT's three real channels.

The checked SU(9) action preserves the complex Hermitian norm. It does not identify that norm with physical energy, nor does it establish a physical gauge-field model. NAHT's existing SU(2) quaternion backend remains a separate three-channel transport.

## Geometry and scope

NAHT topology graphs can represent explicit cell adjacency. This contract does not define an E8-derived honeycomb tessellation, a 9D metric, pressure or stress tensors, or a Navier-Stokes discretization. Those require a specified lattice, metric, state evolution law, boundary conditions, and observable map before they can be implemented or tested.
