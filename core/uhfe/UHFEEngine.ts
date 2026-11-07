// core/uhfe/UHFEEngine.ts

export interface UHFEInputs {
  E_F: number;
  phi: number;      // φ
  Phi: number;      // Φ
  n: number;
  m: number;
  D: number;        // D < 0
  L_d: number;
  // you can later add Θₚ, Δμ, etc. as matrices/vectors
}

export interface UHFESignals {
  Rc: number;   // Core Resonance Index
  Sc: number;   // Core Divergence Index
  Cc: number;   // Chaos / Void Harmonic
  Hc: number;   // Crystalline Harmonic
}

export function computeUHFE(inputs: UHFEInputs): UHFESignals {
  const { E_F, phi, Phi, n, m, D, L_d } = inputs;

  // Input contract: all values finite; the bases of the golden-power scalings
  // must be positive (otherwise fractional exponents give NaN).
  for (const [name, value] of Object.entries({ E_F, phi, Phi, n, m, D, L_d })) {
    if (!Number.isFinite(value)) throw new RangeError(`UHFE input ${name} must be finite`);
  }
  if (phi <= 0 || Phi <= 0) throw new RangeError("UHFE inputs phi and Phi must be positive");

  // For now: discrete approximations instead of integrals.
  // NOTE: Rc * Sc = E_F^2 identically (phi^n * phi^-n = 1), so Sc is a
  // reciprocal of Rc, not an independent signal. The appendix integrals
  // (with psi(t), chi(t), ...) are replaced here by the constant 1.
  const Rc = (E_F / Math.pow(phi, n));        // ∫ ψ(t) dt ≈ 1
  const Sc = (E_F / Math.pow(phi, -n));       // ∫ χ(t) dt ≈ 1
  const Cc = (E_F / Math.pow(phi, D));        // ∫ ω(t) dt ≈ 1
  const Hc = (E_F * L_d) / Math.pow(Phi, m);  // ∫ ζ(t) dt ≈ 1

  return { Rc, Sc, Cc, Hc };
}
