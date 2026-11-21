# NS-EVIDENCE-001 runner time-grid guard

The Cosmo reference runner now validates that requested final time T is
an integer multiple of fixed step dt (within floating-point roundoff). It
rejects incompatible pairs rather than rounding T / dt and silently
stopping early or late.

For example, T=0.1 and dt=0.008 is rejected: 12 steps would end at 0.096.
The frozen NS-EVIDENCE-001 cases are unchanged because each published
T / dt pair is integral.

Run regression tests from this directory:

    python -m unittest -v test_cosmo_ns_time_grid.py

This is input/runner robustness validation only. It does not extend the
benchmark scientific claim class or establish Navier–Stokes regularity
or blow-up.
