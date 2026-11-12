"""Second element table (user-supplied) mapped into the PubChem row schema, plus cross-source checks.

PRE-REGISTERED before the first run (2026-11-12). Same questions, features, transforms, metrics, null and pass rule as
similarity_layout.py and v8_element_map.py; only the data source changes.
  Mapping: FirstIonization -> IonizationEnergy, Type -> GroupBlock (labels used exactly as given; no corrections),
           other measured columns keep their names. Blank cells stay blank (no imputation).
  Tests:   (1) six-property test (similarity_layout.run); (2) V8-map primary (chi, s, d) and secondary (s, d).
  Reported, not required: noble-gas and halogen recall in the secondary test (fraction of each such element's 3
           nearest neighbours carrying the same label), label errors vs the Madelung layout, cross-source agreement.
Non-claims: the second table is NOT independent of PubChem (shared-property Spearman >= 0.99), so agreement shows
consistency, not independent confirmation; its origin is unverified.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

try:
    from . import element_structure as E
    from . import similarity_layout as S
    from . import v8_element_map as M
except ImportError:
    import element_structure as E
    import similarity_layout as S
    import v8_element_map as M

DATA = Path(__file__).resolve().parent / "data" / "SecondTable_user_supplied.csv"
RENAME = {"FirstIonization": "IonizationEnergy", "Type": "GroupBlock"}
EXPECTED_TYPE = {1: "Alkali Metal", 2: "Alkaline Earth Metal", 17: "Halogen", 18: "Noble Gas"}


def load(path=DATA):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r = {k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
            for old, new in RENAME.items():
                r[new] = r.pop(old)
            rows.append(r)
    return rows


def label_errors(rows):
    """s/p-block elements whose Type disagrees with the group-defined family (H excluded)."""
    out = []
    for r in rows:
        z = int(r["AtomicNumber"])
        L = E.layout(z)
        want = EXPECTED_TYPE.get(L["group"]) if (z != 1 and L["block"] in ("s", "p")) else None
        if want and r["GroupBlock"] != want:
            out.append((z, r["Symbol"], r["GroupBlock"], want))
    return out


def class_recall(keep_symbols, X, labels, target, k=3):
    lab = np.asarray(labels)
    nb = S.knn(X, k)
    idx = [i for i, l in enumerate(lab) if l == target]
    if not idx:
        return None, 0
    return float(np.mean([(lab[nb[i]] == target).mean() for i in idx])), len(idx)


def run(rows, permutations=5000, seed=S.SEED):
    six = S.run(rows, permutations, seed)
    v8 = M.run(rows, permutations, seed)
    # class recall in the secondary (s, d) space
    states = M.build_states(rows)
    keep = [(s, r) for s, r in zip(states, rows) if s["V8"]["s"] is not None and s["V8"]["d"] is not None]
    X = np.array([[s["V8"]["s"], s["V8"]["d"]] for s, _ in keep])
    X = (X - X.mean(0)) / X.std(0)
    labels = [r["GroupBlock"] for _, r in keep]
    recall = {t: class_recall(None, X, labels, t) for t in ("Noble Gas", "Halogen", "Alkali Metal", "Alkaline Earth Metal")}
    return {"six": {k: v for k, v in six.items() if k not in ("symbols", "blocks", "X")}, "v8": v8,
            "secondary_class_recall": recall, "label_errors": label_errors(rows)}
