"""Cosmo's independent benchmark of NS-ABOM-E8-LEECH-EQBIT-001.

Re-derives each gate of the composition protocol with Cosmo's own code
and compares against the #142 harness output (harness_reference.json,
produced by running the repo's own integration.compose with the harness
defaults: eqbit samples 128, seed 20261121).

Fences (inherited, unchanged): software composition only. No common
metric, no 9D fluid domain, no E8-to-Leech embedding, no physical
coupling, no quantum claim, no NS regularity claim. Navier-Stokes
remains not_tested. Passing means the interface checks pass — nothing
more.

Blindness is partial: targets are published (the spec records this).
Implementation is independent; no bench's code or result files were
read beyond the repo modules this bench explicitly compares against.

Gate 6 adapter mapping was written in the spec BEFORE running:
  probe = E(T)/E(0) from the frozen 3D N=32 T=0.1 case
        = 0.124251988080873 / 0.125 = 0.9940159046469843 (dimensionless).
The harness instead feeds ET itself (0.12425198808087304) as the probe
energy; both are dimensionless interface probes and the difference is
recorded, not hidden.
"""
import hashlib
import itertools
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE / "repo"
WORKSPACE_NS = Path("/home/hatch/workspace/goals/panoramic-os-and-pan-fractal-kernel-review/"
                    "hidden_files/ns-evidence-cosmo/cosmo_results.json")
REPO_NS = REPO / "experiments/ns_evidence_001_cosmo/cosmo_results.json"
HARNESS_REF = HERE / "harness_reference.json"
OUT = HERE / "cosmo_composition_results.json"

sys.path.insert(0, str(REPO))
from core.geometry import e8_root_system as e8mod  # noqa: E402
from core.abom_v8 import abom_v8_model as abommod  # noqa: E402
from experiments.flip_qubit import cut_rank_audit as eqbitmod  # noqa: E402
from experiments.moonshine_sierpinski import leech_unimodular_basis as leechmod  # noqa: E402

RESULTS = {"bench": "cosmo_composition_bench.py",
           "composition": "NS-ABOM-E8-LEECH-EQBIT-001",
           "harness_reference": "harness_reference.json (repo integration.compose, "
                                "eqbit samples 128, seed 20261121)",
           "gates": {}}


def gate(name):
    def deco(fn):
        out = fn()
        RESULTS["gates"][name] = out
        print(f"[{name}] {'PASS' if out.get('pass') else 'FAIL'} — "
              f"{out.get('summary', '')}")
        return out
    return deco


# ---------------------------------------------------------------- Gate 1: NS
@gate("gate1_ns_provenance")
def _g1():
    repo_bytes = REPO_NS.read_bytes()
    ws_bytes = WORKSPACE_NS.read_bytes()
    repo = json.loads(repo_bytes)
    ws = json.loads(ws_bytes)
    cases = repo["cases"]
    required = ("n", "d", "nu", "T", "dt", "steps", "ET", "OmT", "max_div_T")
    checks = {
        "byte_identical": repo_bytes == ws_bytes,
        "sha256_repo": hashlib.sha256(repo_bytes).hexdigest(),
        "sha256_workspace": hashlib.sha256(ws_bytes).hexdigest(),
        "value_identical": repo == ws,
        "nine_cases": len(cases) == 9,
        "all_required_keys": all(all(k in c for k in required) for c in cases),
        "dimensions_2d_3d": sorted({c["d"] for c in cases}) == [2, 3],
        "steps_dt_lands_on_T": all(
            abs(c["steps"] * c["dt"] - c["T"]) <= max(1e-14, abs(c["T"]) * 1e-12)
            for c in cases),
    }
    # Internal agreement inside the frozen data (not a re-run of the solver).
    et_3d_t01 = [c["ET"] for c in cases if c["d"] == 3 and c["T"] == 0.1]
    et_3d_t05 = [c["ET"] for c in cases if c["d"] == 3 and c["T"] == 0.5]
    checks["et_3d_T0.1_spread"] = max(et_3d_t01) - min(et_3d_t01)
    checks["et_3d_T0.5_spread"] = max(et_3d_t05) - min(et_3d_t05)
    checks["max_div_T_all"] = max(c["max_div_T"] for c in cases)
    checks["cases"] = [{k: c[k] for k in required} for c in cases]
    checks["three_seat_headline"] = (
        "Cross-seat agreement established at merge time (PRs #130/#131/#133): "
        "Klaus blind replication agrees to <=3e-14, Cosmo third seat to "
        "<=~1.3e-14; not recomputed here — the other seats' files are outside "
        "this bench's scope. This gate checks the frozen Cosmo file itself.")
    ok = (checks["byte_identical"] and checks["value_identical"]
          and checks["nine_cases"] and checks["all_required_keys"]
          and checks["dimensions_2d_3d"] and checks["steps_dt_lands_on_T"])
    return {"pass": bool(ok), "summary":
            "repo copy == workspace original byte-identical; 9 cases, "
            f"3D T=0.1 ET spread {checks['et_3d_T0.1_spread']:.2e}, "
            f"T=0.5 ET spread {checks['et_3d_T0.5_spread']:.2e}",
            "checks": checks}


# ---------------------------------------------------------------- Gate 2: E8
def _my_e8_scaled():
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((-2, 2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            roots.append(tuple(v))
    for signs in itertools.product((-1, 1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(tuple(signs))
    return roots


@gate("gate2_e8_roots")
def _g2():
    roots = _my_e8_scaled()
    assert len(roots) == 240 and len(set(roots)) == 240
    norms = {sum(x * x for x in r) for r in roots}
    # Neighbours: inner product 4 in scaled units (= 1 unscaled).
    deg = []
    for r in roots:
        deg.append(sum(1 for s in roots
                       if sum(a * b for a, b in zip(r, s)) == 4))
    edges = sum(deg) // 2
    # Shells by inner product with roots[0]: 8, 4, {0,-4}, -8.
    r0 = roots[0]
    shell = {8: 0, 4: 0, 0: 0, -4: 0, -8: 0}
    for s in roots:
        shell[sum(a * b for a, b in zip(r0, s))] += 1
    shells = [shell[8], shell[4], shell[0] + shell[-4], shell[-8]]
    # Compare against the module's exact rational roots, scaled x2.
    mod_roots = {tuple(int(2 * x) for x in r) for r in e8mod.e8_roots_exact()}
    simple = e8mod.e8_simple_roots_exact()
    simple_scaled = [tuple(int(2 * x) for x in r) for r in simple]
    gram_ok = True
    for i in range(8):
        for j in range(8):
            g = sum(a * b for a, b in zip(simple[i], simple[j]))
            exp = 2 if i == j else -1 if tuple(sorted((i, j))) in {
                (0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)} else 0
            gram_ok = gram_ok and (g == exp)
    checks = {"count": len(roots), "unique": len(set(roots)),
              "norms_squared_scaled": sorted(norms),
              "degree_min": min(deg), "degree_max": max(deg),
              "edges": edges, "shells_vs_root0": shells,
              "set_equals_module_x2": set(roots) == mod_roots,
              "simple_roots_in_my_set": all(r in set(roots) for r in simple_scaled),
              "simple_root_gram_matches_dynkin": gram_ok}
    ok = (len(roots) == 240 and norms == {8} and min(deg) == max(deg) == 56
          and edges == 6720 and shells == [1, 56, 182, 1]
          and checks["set_equals_module_x2"] and gram_ok)
    return {"pass": bool(ok),
            "summary": f"240 roots, norm^2 8 (scaled), 56 neighbours, "
                       f"{edges} edges, shells {shells}; set == module x2",
            "checks": checks}


# ------------------------------------------------------------ Gate 3: eqbit
def _bits_for(neighbours, right_bit):
    bits = 0
    for nb in neighbours:
        b = right_bit.get(nb)
        if b is not None:
            bits |= 1 << b
    return bits


def _gf2_rank(rows):
    pivots = {}
    for value in rows:
        row = value
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


@gate("gate3_flip_eqbit_cut_rank")
def _g3():
    roots = _my_e8_scaled()
    index = {r: i for i, r in enumerate(roots)}
    adj = [set() for _ in roots]
    for i in range(240):
        for j in range(i + 1, 240):
            if sum(a * b for a, b in zip(roots[i], roots[j])) == 4:
                adj[i].add(j)
                adj[j].add(i)
    assert all(len(a) == 56 for a in adj)
    assert sum(map(len, adj)) // 2 == 6720
    # Canonical antipodal partition: first nonzero coordinate > 0 -> left.
    left, right, pairs = [], [], []
    for i, r in enumerate(roots):
        if next(x for x in r if x) > 0:
            j = index[tuple(-x for x in r)]
            pairs.append((i, j))
            left.append(i)
            right.append(j)
    assert len(pairs) == 120
    right_bit = {v: b for b, v in enumerate(right)}
    rows = []
    for v in left:
        bits = 0
        for nb in adj[v]:
            b = right_bit.get(nb)
            if b is not None:
                bits |= 1 << b
        rows.append(bits)
    rank = _gf2_rank(rows)
    crossing = sum(len(adj[v] & set(right)) for v in left)
    # Module comparison (exact fields only; its samples are its own).
    mod = eqbitmod.run(samples=128, seed=20261121)
    # My own independent sampling (different seed, own RNG consumption).
    rng = random.Random(20261122)
    tr, bal = [], []
    verts = list(range(240))
    for _ in range(256):
        L, R = [], []
        for a, b in pairs:
            if rng.getrandbits(1):
                L.append(a); R.append(b)
            else:
                L.append(b); R.append(a)
        rb = {v: k for k, v in enumerate(R)}
        tr.append(_gf2_rank([_bits_for(adj[v], rb) for v in L]))
        arb = rng.sample(verts, 120)
        s = set(arb)
        rb2 = {v: k for k, v in enumerate([v for v in verts if v not in s])}
        bal.append(_gf2_rank([_bits_for(adj[v], rb2) for v in arb]))
    checks = {"antipodal_rank": rank, "expected_rank": 112,
              "crossing_edges": crossing, "expected_crossing": 2240,
              "module_antipodal_rank": mod["antipodal_cut"]["rank_gf2"],
              "module_crossing_edges": mod["antipodal_cut"]["crossing_edges"],
              "module_geometry": mod["geometry"],
              "my_transversal_256": {"min": min(tr), "max": max(tr),
                                     "mean": sum(tr) / len(tr)},
              "my_balanced_256": {"min": min(bal), "max": max(bal),
                                  "mean": sum(bal) / len(bal)},
              "module_transversal_128": mod["random_transversal_cuts"],
              "module_balanced_128": mod["random_balanced_cuts"]}
    ok = (rank == 112 and crossing == 2240
          and mod["antipodal_cut"]["rank_gf2"] == 112
          and mod["antipodal_cut"]["crossing_edges"] == 2240)
    return {"pass": bool(ok),
            "summary": f"antipodal cut-rank {rank} (of 120), crossing "
                       f"{crossing}; module agrees exactly; my 256-sample "
                       f"transversal range {min(tr)}-{max(tr)}, balanced "
                       f"{min(bal)}-{max(bal)}",
            "checks": checks}

# ------------------------------------------------------------ Gate 4: Leech
_GOLAY23_GENERATOR = sum(1 << i for i in (0, 1, 5, 6, 7, 9, 11))


def _my_golay_codewords():
    # Standard [23,12,7] generator polynomial, low bit = x^0 — the same
    # canonical polynomial the module uses; the code definition is shared,
    # the audit of its properties and everything built on it is mine.
    words = []
    for message in range(1 << 12):
        word = 0
        for bit in range(12):
            if (message >> bit) & 1:
                word ^= _GOLAY23_GENERATOR << bit
        if word.bit_count() & 1:
            word |= 1 << 23
        words.append(word)
    return words


def _my_is_lattice_vector(v, codeword_set):
    p = v[0] & 1
    if any((x & 1) != p for x in v):
        return False
    residue = 0
    for i, x in enumerate(v):
        if (((x - p) // 2) & 1):
            residue |= 1 << i
    return residue in codeword_set and sum(v) % 8 == (4 * p) % 8


@gate("gate4_leech_basis_certificate")
def _g4():
    import sympy as sp
    basis = leechmod._COORDINATE_BASIS  # the data; the check is mine
    B = sp.Matrix(basis)
    BtB = B.T * B
    gram_num = [[int(BtB[i, j]) for j in range(24)] for i in range(24)]
    integral = all(v % 8 == 0 for row in gram_num for v in row)
    G = sp.Matrix([[v // 8 for v in row] for row in gram_num])
    det_G = int(G.det())
    det_B = int(B.det())
    even_diag = all(int(G[i, i]) % 2 == 0 for i in range(24))
    rank = int(G.rank())
    pos_def = bool(G.is_positive_definite)
    # Golay code: my generation + my audit of its properties.
    words = _my_golay_codewords()
    codeword_set = frozenset(words)
    from collections import Counter
    weights = dict(sorted(Counter(w.bit_count() for w in words).items()))
    # Self-duality: every word orthogonal to each of the 12 generator rows.
    gen_rows = []
    for bit in range(12):
        w = _GOLAY23_GENERATOR << bit
        if w.bit_count() & 1:
            w |= 1 << 23
        gen_rows.append(w)
    self_orth = all((w & g).bit_count() % 2 == 0
                    for w in words for g in gen_rows)
    # Minimal shell: my enumeration of the three Conway families + my checks.
    octads = [w for w in words if w.bit_count() == 8]
    vecs = []
    for i, j in itertools.combinations(range(24), 2):
        for si, sj in itertools.product((-4, 4), repeat=2):
            v = [0] * 24
            v[i], v[j] = si, sj
            vecs.append(tuple(v))
    fam_a = len(vecs)
    for octad in octads:
        support = [i for i in range(24) if (octad >> i) & 1]
        for signs in itertools.product((-2, 2), repeat=8):
            if sum(1 for x in signs if x < 0) % 2:
                continue
            v = [0] * 24
            for i, value in zip(support, signs):
                v[i] = value
            vecs.append(tuple(v))
    fam_b = len(vecs) - fam_a
    for special in range(24):
        base = [1] * 24
        base[special] = -3
        for word in words:
            vecs.append(tuple(-value if (word >> i) & 1 else value
                              for i, value in enumerate(base)))
    fam_c = len(vecs) - fam_a - fam_b
    uniq = len(set(vecs))
    norms_ok = all(sum(x * x for x in v) == 32 for v in vecs)
    congr_ok = all(_my_is_lattice_vector(v, codeword_set) for v in vecs)
    href = json.loads(HARNESS_REF.read_text())["leech"]
    checks = {"basis_shape": (len(basis), len(basis[0])),
              "gram_integral": integral, "gram_even_diagonal": even_diag,
              "gram_det_sympy": det_G, "coordinate_basis_det_sympy": det_B,
              "coordinate_covolume_expected": 1 << 36,
              "gram_rank": rank, "gram_positive_definite": pos_def,
              "golay_codewords": len(words), "golay_unique": len(set(words)),
              "golay_weight_distribution": weights,
              "golay_self_dual_via_generator_rows": self_orth,
              "minimal_shell_total": len(vecs), "minimal_shell_unique": uniq,
              "family_counts": {"A": fam_a, "B": fam_b, "C": fam_c},
              "all_norm_squared_32": norms_ok,
              "all_pass_my_congruence_check": congr_ok,
              "harness_leech_minimal": href["minimal_vectors_at_minimum"],
              "harness_gram_det": href["scaled_gram_determinant"],
              "harness_coordinate_det": href["coordinate_basis_determinant"],
              "harness_minimum_norm": href["minimum_norm_attained"]}
    ok = (integral and even_diag and det_G == 1 and abs(det_B) == (1 << 36)
          and rank == 24 and pos_def and len(words) == 4096
          and weights == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
          and self_orth and len(vecs) == 196560 and uniq == 196560
          and norms_ok and congr_ok
          and href["minimal_vectors_at_minimum"] == 196560
          and href["scaled_gram_determinant"] == 1)
    return {"pass": bool(ok),
            "summary": f"Gram det {det_G}, coordinate det {det_B}, rank 24, "
                       f"even+positive-definite; minimal shell {len(vecs)} "
                       f"({fam_a}+{fam_b}+{fam_c}) independently enumerated",
            "checks": checks}


# ------------------------------------------------------------- Gate 5: ABOM
def _my_fermi_occupation(energy, mu=0.0, kT=1.0):
    q = (energy - mu) / kT
    if q >= 0:
        e = math.exp(-q)
        return e / (1.0 + e)
    e = math.exp(q)
    return 1.0 / (1.0 + e)


def _my_abom_sample(x, y, z, energy, mu=0.0, kT=1.0, root_count=240):
    r = math.sqrt(x * x + y * y + z * z)
    field = 2.0 ** r
    scale_x = math.log2(max(r, 1e-300))
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    phi_inv = phi - 1.0
    base = 2.0 ** scale_x
    n = _my_fermi_occupation(energy, mu, kT)
    hole = 1.0 - n
    return {
        "radial_field": field, "scale_coordinate": scale_x,
        "golden_branches": {"phi": phi * base, "phi_inverse": phi_inv * base,
                            "phi_negative": -phi * base,
                            "phi_inverse_negative": -phi_inv * base},
        "fermi": {"positive_occupation": n,
                  "complementary_hole_fraction": hole,
                  "signed_contrast": n - hole},
        "fermi_weighted_field": {
            "occupation_channel": field * n,
            "hole_channel": field * hole,
            "signed_contrast_channel": field * (n - hole)},
        "e8_root_count": root_count,
        "hyperoctahedral_B8_order": 2 ** 8 * math.factorial(8),
    }


def _close(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


@gate("gate5_abom_v8_sample")
def _g5():
    points = [
        ("harness_probe_point", (0.0, 0.0, 0.0, 0.12425198808087304, 0.0, 1.0)),
        ("cosmo_adapter_point", (0.0, 0.0, 0.0, 0.9940159046469843, 0.0, 1.0)),
        ("generic_point", (1.0, 2.0, -0.5, 0.7, 0.1, 0.5)),
    ]
    compared = {}
    all_ok = True
    for name, (x, y, z, e, mu, kT) in points:
        mine = _my_abom_sample(x, y, z, e, mu, kT, root_count=240)
        mod = abommod.abom_v8_sample(x, y, z, e, mu, kT)
        ok = (_close(mine["radial_field"], mod["radial_field"])
              and _close(mine["scale_coordinate"], mod["scale_coordinate"])
              and all(_close(mine["golden_branches"][k], mod["golden_branches"][k])
                      for k in mine["golden_branches"])
              and all(_close(mine["fermi"][k], mod["fermi"][k])
                      for k in mine["fermi"])
              and all(_close(mine["fermi_weighted_field"][k],
                             mod["fermi_weighted_field"][k])
                      for k in mine["fermi_weighted_field"])
              and mine["e8_root_count"] == mod["e8_root_count"] == 240
              and mine["hyperoctahedral_B8_order"]
              == mod["hyperoctahedral_B8_order"] == 2 ** 8 * math.factorial(8)
              and len(mod["octants"]) == 8)
        compared[name] = {"match": bool(ok),
                          "my_radial_field": mine["radial_field"],
                          "module_radial_field": mod["radial_field"],
                          "my_fermi_occupation": mine["fermi"]["positive_occupation"],
                          "module_fermi_occupation": mod["fermi"]["positive_occupation"]}
        all_ok = all_ok and ok
    spots = {
        "exp_scale_inverse_roundtrip": _close(
            abommod.inverse_exponential_scale(
                abommod.exponential_scale(3.7)), 3.7),
        "oscillator_level_3": abommod.oscillator_energy_level(3) == 3.5,
        "B8_order": abommod.hyperoctahedral_group_order(8) == 10321920,
        "octants_count": len(abommod.spatial_octants(1.0, -2.0, 0.5)) == 8,
        "apply_6d_identity": abommod.apply_6d_basis(
            [[1.0 if i == j else 0.0 for j in range(6)] for i in range(6)],
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]) == (1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
    }
    all_ok = all_ok and all(spots.values())
    return {"pass": bool(all_ok),
            "summary": "closed-form channels recomputed at 3 points and match "
                       "the module; root-count view 240; B8 order 10321920",
            "checks": {"points": compared, "spot_checks": spots}}


# ------------------------------------------------- Gate 6: Cosmo's adapter
@gate("gate6_ns_abom_adapter_cosmo")
def _g6():
    repo = json.loads(REPO_NS.read_text())
    case = [c for c in repo["cases"]
            if c["d"] == 3 and c["n"] == 32 and c["T"] == 0.1][0]
    probe = case["ET"] / case["E0"]
    mine = {"positive_occupation": _my_fermi_occupation(probe, 0.0, 1.0)}
    mine["complementary_hole_fraction"] = 1.0 - mine["positive_occupation"]
    mine["signed_contrast"] = (mine["positive_occupation"]
                               - mine["complementary_hole_fraction"])
    mod = abommod.fermi_channels(probe, 0.0, 1.0)
    href = json.loads(HARNESS_REF.read_text())
    harness_energy = href["ns_snapshot"]["selected_probe"]["ET"]
    harness_fermi = href["abom_probe"]["fermi"]
    my_at_harness_energy = _my_fermi_occupation(harness_energy, 0.0, 1.0)
    checks = {"case": {k: case[k] for k in
                       ("n", "d", "nu", "T", "dt", "steps", "E0", "ET")},
              "probe_ET_over_E0": probe,
              "probe_matches_spec_pinned": _close(
                  probe, 0.124251988080873 / 0.125, tol=1e-12),
              "my_fermi_at_cosmo_probe": mine,
              "module_fermi_at_cosmo_probe": mod,
              "adapter_match": all(_close(mine[k], mod[k]) for k in mine),
              "harness_probe_energy_ET": harness_energy,
              "harness_fermi_occupation": harness_fermi["positive_occupation"],
              "my_fermi_at_harness_energy": my_at_harness_energy,
              "harness_fermi_match": _close(
                  my_at_harness_energy, harness_fermi["positive_occupation"]),
              "ns_eqbit_coupled": False,
              "note": ("The harness feeds ET itself as the probe energy; "
                       "Cosmo's adapter feeds the dimensionless ratio "
                       "ET/E0. Different probe values, same interface: a "
                       "labelled dimensionless Fermi-channel probe, not a "
                       "physical energy coupling.")}
    ok = (checks["probe_matches_spec_pinned"] and checks["adapter_match"]
          and checks["harness_fermi_match"])
    return {"pass": bool(ok),
            "summary": f"Cosmo probe ET/E0 = {probe:.15f}; Fermi occupation "
                       f"{mine['positive_occupation']:.6f} (harness probe "
                       f"{harness_fermi['positive_occupation']:.6f} at ET); "
                       f"NS<->flip-eqbit NOT_COUPLED",
            "checks": checks}


# ------------------------------------------------------- Pairwise re-checks
def _pairwise():
    g = RESULTS["gates"]
    href = json.loads(HARNESS_REF.read_text())
    pw = {
        "NS_ABOM": {"status": "PASS",
                    "check": "frozen 3D NS energy accepted as a labelled "
                             "dimensionless Fermi probe (Cosmo adapter: "
                             "ET/E0); no physical coupling claimed"},
        "ABOM_E8": {"status": "PASS" if g["gate5_abom_v8_sample"]["checks"]
                    ["points"]["harness_probe_point"]["match"]
                    and g["gate2_e8_roots"]["checks"]["count"] == 240
                    else "FAIL",
                    "check": "ABOM root-count view (240) agrees with "
                             "independently constructed E8 (240)"},
        "E8_LEECH": {"status": "PASS",
                     "check": "rank-8 E8 and rank-24 Leech certificates "
                              "coexist as separate artifacts; no embedding"},
        "E8_EQBIT": {"status": "PASS" if
                     g["gate3_flip_eqbit_cut_rank"]["checks"]
                     ["antipodal_rank"] == 112
                     and g["gate2_e8_roots"]["checks"]["count"] == 240
                     else "FAIL",
                     "check": "flip-eqbit reconstructs the 240-vertex "
                              "Gosset contract from the independent E8 set"},
        "LEECH_EQBIT": {"status": "PASS",
                        "check": "lattice certificate and graph-state audit "
                                 "remain separate typed artifacts"},
        "NS_EQBIT": {"status": "NOT_COUPLED",
                     "check": "no solver-to-graph-state dynamical map is "
                              "defined in the protocol or the harness"},
    }
    return pw


def main():
    # Gates run on import via the decorators above (definition order).
    RESULTS["pairwise_gates_cosmo"] = _pairwise()
    RESULTS["harness_pairwise_gates"] = json.loads(
        HARNESS_REF.read_text())["pairwise_gates"]
    RESULTS["harness_overall_status"] = json.loads(
        HARNESS_REF.read_text())["overall_status"]
    RESULTS["overall"] = ("PASS" if all(
        v["pass"] for v in RESULTS["gates"].values())
        and all(v["status"] in ("PASS", "NOT_COUPLED")
                for v in RESULTS["pairwise_gates_cosmo"].values())
        else "FAIL")
    RESULTS["interpretation"] = [
        "Software composition and provenance exercise, not a unified "
        "physical law. Passing means the interface checks pass — nothing more.",
        "Navier-Stokes remains not_tested; no regularity or blow-up claim.",
        "E8 and Leech coordinate spaces are not embedded into one another.",
        "Flip-eqbit is static graph-state mathematics, not physical quantum "
        "dynamics or hardware.",
        "The Leech minimal-shell count 196,560 was independently enumerated "
        "here (three Conway families, own Golay code and congruence checks), "
        "not merely cross-checked.",
        "NS <-> flip-eqbit stays NOT_COUPLED: no state map, units, dynamics, "
        "or falsifiable observables are defined for such a link.",
    ]
    OUT.write_text(json.dumps(RESULTS, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(f"\nOVERALL: {RESULTS['overall']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
