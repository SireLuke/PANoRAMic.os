"""Declared element -> V8 map, v0 (numpy only). Declared hypothesis, NOT canonical, NOT a physical identity.

Schema: the eight-coordinate state (h, R, u, d, tau, chi, s, f) of docs/PAN_V8_DYNAMIC_PHASE_LAYER.md
(convention: chi in [-1, 1], all others in [0, 1]). Contract: the "named channel, declared source and transform,
no derived physical identity" wording of core/abom_v8/physics_adapters.map_scalar_to_v8, extended to several
channels. Unassigned channels stay None (never 0: a zero would read as a measurement).

STRUCTURAL channels (exact functions of the Madelung configuration; they PLACE elements on the grid and are
NOT tested for group recovery, because they largely determine group and block, so a test would be circular):
  R   = (period - 1) / 6
  h   = position within the period / period length   (closed shell, i.e. a noble gas, gives exactly 1;
        theta = 2*pi*h wraps there)
  u   = occupancy of the last-filled subshell / its capacity 2(2l+1)

MEASURED channels (PubChem table; the only channels the null test may use):
  chi = (Electronegativity - median) / max|deviation|, in [-1, 1]
  s   = min-max of log10(Density)
  d   = min-max of IonizationEnergy
UNASSIGNED: tau (atomic number is an ordering, not time), f.

PRE-REGISTERED before the first run (2026-11-12). Same question and metrics as similarity_layout.py, but the
feature vector is the measured V8 channels only.
  Primary:   (chi, s, d), complete cases, no imputation.
  Secondary: (s, d), every element with both values (includes noble gases whose electronegativity is missing).
  Metrics:   A = mean fraction of each element's 3 nearest neighbours sharing its GroupBlock;
             C = for s/p-block elements (H excluded) the fraction of 1-nearest-neighbours sharing the layout group.
  Null:      labels shuffled over the same elements, 5000 permutations, seed 20261112.
  PASS:      A and C each exceed the null 99th percentile.
  Reported, not required: comparison with the six-property baseline (A=0.69, C=0.57).
Non-claims: the map does not show V8 explains elements, does not use E8 roots, and the V9 view layer is not
used here.
"""
from __future__ import annotations

import math

import numpy as np

try:
    from . import element_structure as E
    from . import similarity_layout as S
except ImportError:
    import element_structure as E
    import similarity_layout as S

COORDS = ("h", "R", "u", "d", "tau", "chi", "s", "f")
UNASSIGNED = ("tau", "f")
MAPPING_KIND = "declared multi-channel projection; not a derived physical identity"
SOURCES = {
    "R": "structural: period of Madelung configuration",
    "h": "structural: position in period / period length",
    "u": "structural: last-filled subshell occupancy / capacity",
    "chi": "measured: Electronegativity, centred at table median, scaled by max |deviation|",
    "s": "measured: log10 Density, min-max",
    "d": "measured: IonizationEnergy, min-max",
    "tau": "unassigned", "f": "unassigned",
}


def structural(z: int) -> dict:
    """Exact structural channels for atomic number z (1..118)."""
    period = E.period_of(z)
    prev = 0 if period == 1 else E.NOBLE_Z[period - 2]
    length = E.NOBLE_Z[period - 1] - prev
    _, l, e = E.madelung_config(z)[-1]
    return {"R": (period - 1) / 6.0, "h": (z - prev) / length, "u": e / E.capacity(l)}


def phase_angle(z: int) -> float:
    """theta = 2*pi*h; equals 2*pi (a full wrap) exactly at each noble-gas closure."""
    return 2.0 * math.pi * structural(z)["h"]


def _val(row, key):
    return None if row[key] == "" else float(row[key])


def normalization(rows) -> dict:
    """Table-fit constants for the measured channels (computed from every row that has the value)."""
    en = [float(r["Electronegativity"]) for r in rows if r["Electronegativity"] != ""]
    rho = [math.log10(float(r["Density"])) for r in rows if r["Density"] != ""]
    ie = [float(r["IonizationEnergy"]) for r in rows if r["IonizationEnergy"] != ""]
    med = float(np.median(en))
    return {"en_median": med, "en_scale": max(abs(v - med) for v in en),
            "logrho_min": min(rho), "logrho_max": max(rho), "ie_min": min(ie), "ie_max": max(ie)}


def v8_state(row: dict, norm: dict) -> dict:
    """Declared V8 state for one table row. Channels without a source value are None."""
    z = int(row["AtomicNumber"])
    out = {k: None for k in COORDS}
    out.update(structural(z))
    en, rho, ie = _val(row, "Electronegativity"), _val(row, "Density"), _val(row, "IonizationEnergy")
    if en is not None:
        out["chi"] = max(-1.0, min(1.0, (en - norm["en_median"]) / norm["en_scale"]))
    if rho is not None:
        out["s"] = (math.log10(rho) - norm["logrho_min"]) / (norm["logrho_max"] - norm["logrho_min"])
    if ie is not None:
        out["d"] = (ie - norm["ie_min"]) / (norm["ie_max"] - norm["ie_min"])
    return {"V8": out, "mapping_kind": MAPPING_KIND, "sources": SOURCES, "Z": z, "Symbol": row["Symbol"]}


def build_states(rows) -> list:
    norm = normalization(rows)
    return [v8_state(r, norm) for r in rows]


def _test(rows_states, channels, permutations, seed):
    rng = np.random.default_rng(seed)
    keep = [s for s in rows_states if all(s["V8"][c] is not None for c in channels)]
    X = np.array([[s["V8"][c] for c in channels] for s in keep], dtype=float)
    X = (X - X.mean(0)) / X.std(0)
    blocks = [S_row["GroupBlock"] for S_row in (s["row"] for s in keep)]
    nb3 = S.knn(X, 3)
    A = S.purity(nb3, blocks)
    nullA = S._null(lambda l: S.purity(nb3, l), blocks, permutations, rng)
    sel, groups = [], []
    for i, s in enumerate(keep):
        L = E.layout(s["Z"])
        if s["Z"] != 1 and L["block"] in ("s", "p"):
            sel.append(i)
            groups.append(L["group"])
    nb1 = S.knn(X[sel], 1)
    C = S.purity(nb1, groups)
    nullC = S._null(lambda l: S.purity(nb1, l), groups, permutations, rng)
    return {"channels": list(channels), "complete_cases": len(keep), "A": A,
            "A_null_p99": float(np.percentile(nullA, 99)), "A_null_ge_obs": int((nullA >= A).sum()),
            "C": C, "C_n": len(sel), "C_null_p99": float(np.percentile(nullC, 99)),
            "C_null_ge_obs": int((nullC >= C).sum()),
            "passes": bool(A > np.percentile(nullA, 99) and C > np.percentile(nullC, 99)),
            "missing": sorted(s["Symbol"] for s in rows_states if s not in keep)}


def run(rows, permutations=5000, seed=S.SEED):
    states = build_states(rows)
    for s, r in zip(states, rows):
        s["row"] = r
    primary = _test(states, ("chi", "s", "d"), permutations, seed)
    secondary = _test(states, ("s", "d"), permutations, seed)
    return {"primary": primary, "secondary": secondary, "baseline": {"A": 0.69, "C": 0.57}}
