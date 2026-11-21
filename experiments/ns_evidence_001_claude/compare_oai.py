#!/usr/bin/env python3
"""Compare the Claude-bench NS-EVIDENCE-001 results with the OpenAI-bench report (PR #130).

Reads
    outputs/results.json                    (this directory; independent solver)
    outputs/oai_ns_evidence_001_results.json (verbatim copy of the JSON at PR #130 head 1992c65)
Writes
    outputs/comparison_vs_oai.json

Sign convention note: the OpenAI report defines the balance residual as
E(0) - E(T) - trapz(eps); this repo's solver uses E(T) - E(0) + D(T). The
comparison below uses the *trapezoid* variant of mine with the sign flipped, so
both sides measure the same quantity.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")


def main():
    mine = json.load(open(os.path.join(OUT, "results.json")))["cases"]
    oai = json.load(open(os.path.join(OUT, "oai_ns_evidence_001_results.json")))

    def cid(d, N, T, dt):
        return "%dD_N%d_T%g_dt%g_convective" % (d, N, T, dt)

    rows = []
    for c in oai["cases"]:
        d, N, dt = c["dimension"], c["n"], c["dt"]
        m = mine[cid(d, N, 0.1, dt)]
        row = dict(
            id=m["id"],
            E_final=(c["energy_final"], m["E_T"]),
            enstrophy_final=(c["enstrophy_final"], m["Omega_T"]),
            dissipation_final=(c["dissipation_final"], m["eps_T"]),
            energy_drop=(c["energy_drop"], m["E0"] - m["E_T"]),
            integrated_dissipation_trapezoid=(c["integrated_dissipation_trapezoid"], m["D_int_trapezoid"]),
            integrated_dissipation_rk4_stages_mine_only=(None, m["D_int"]),
            balance_residual_trapezoid=(c["energy_balance_residual"], -m["resid_abs_trapezoid"]),
            enstrophy_initial=(c["enstrophy_initial"], m["Omega0"]),
            max_div_final=(c["max_divergence_final"], m["maxdiv_final"]),
        )
        if "exact_relative_rms_error" in c:
            row["exact_relative_rms_error"] = (c["exact_relative_rms_error"], m["exact2d_l2_rel_error"])
        rows.append(row)
    for t in oai["temporal_sensitivity_3d_n16_t05"]:
        m = mine[cid(3, 16, 0.5, t["dt"])]
        rows.append(
            dict(
                id=m["id"],
                E_final=(t["energy_final"], m["E_T"]),
                balance_residual_trapezoid=(t["energy_balance_residual"], -m["resid_abs_trapezoid"]),
            )
        )

    out = []
    for r in rows:
        rec = {"id": r["id"]}
        for k, v in r.items():
            if k == "id":
                continue
            theirs, ours = v
            rec[k] = dict(
                openai=theirs, claude=ours,
                abs_diff=None if theirs is None else abs(theirs - ours),
                rel_diff=None if theirs in (None, 0) else abs(theirs - ours) / abs(theirs),
            )
        out.append(rec)
    with open(os.path.join(OUT, "comparison_vs_oai.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    hdr = "%-30s %-34s %-22s %-22s %-10s %-10s"
    print(hdr % ("case", "quantity", "openai", "claude", "abs diff", "rel diff"))
    for rec in out:
        for k, v in rec.items():
            if k == "id" or v["openai"] is None:
                continue
            print("%-30s %-34s %-22.15g %-22.15g %-10.2e %-10.2e" % (rec["id"], k, v["openai"], v["claude"], v["abs_diff"], v["rel_diff"] or 0.0))


if __name__ == "__main__":
    main()
