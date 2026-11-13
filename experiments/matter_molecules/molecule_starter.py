"""Starter molecule set and a partial electron-affinity / Allen table (stdlib only).

Scope: load and sanity-check small user-supplied tables. Nothing here asserts physics: the values are as supplied
(or as sourced where stated), and checks compare them only against internal consistency and a short web cross-check.

Cross-check reference (fetched 2026-11-13 from the Wikipedia 'Electronegativities of the elements (data page)'
Allen column): ALLEN_REFERENCE below. The user's PDF lists Cl = 3.481, which disagrees with that reference (2.869);
the supplied value is kept as supplied and reported as a conflict, not silently corrected.
Sign convention: a negative electron affinity means the anion is unbound; the He, Ne, Ar entries are literature
estimates, not bound-state measurements.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

_DATA = Path(__file__).resolve().parent / "data" / "molecules_starter.json"
_EA = Path(__file__).resolve().parents[1] / "matter_elements" / "data" / "EA_Allen_partial_user_supplied.csv"

VALENCE = {"H": 1, "C": 4, "N": 3, "O": 2, "Cl": 1}
ALLEN_REFERENCE = {"H": 2.300, "He": 4.160, "Li": 0.912, "C": 2.544, "N": 3.066, "O": 3.610, "F": 4.193,
                   "Ne": 4.787, "Cl": 2.869, "Ar": 3.242, "Kr": 2.966, "Xe": 2.582, "Br": 2.685, "I": 2.359}
ALLEN_TOLERANCE = 0.005


def load_molecules(path=_DATA):
    return json.loads(Path(path).read_text())["molecules"]


def formula_counts(formula: str) -> dict:
    counts = {}
    for sym, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        counts[sym] = counts.get(sym, 0) + (int(n) if n else 1)
    return counts


def smiles_counts(smiles: str) -> dict:
    """Atom counts of a linear organic-subset SMILES with implicit hydrogens (atoms joined in a chain, '=' = double)."""
    tokens = re.findall(r"Cl|[A-Z]|=", smiles)
    atoms, orders, pending = [], [], 1
    for t in tokens:
        if t == "=":
            pending = 2
        else:
            if atoms:
                orders.append(pending)
            atoms.append(t)
            pending = 1
    counts = {}
    for i, a in enumerate(atoms):
        if a not in VALENCE:
            raise ValueError(f"unsupported atom {a}")
        used = (orders[i - 1] if i > 0 else 0) + (orders[i] if i < len(orders) else 0)
        h = VALENCE[a] - used
        if h < 0:
            raise ValueError("valence exceeded")
        counts[a] = counts.get(a, 0) + 1
        counts["H"] = counts.get("H", 0) + h
    return {k: v for k, v in counts.items() if v}


def load_ea_allen(path=_EA):
    with open(path, newline="") as fh:
        return [{"Z": int(r["AtomicNumber"]), "Symbol": r["Symbol"], "EA": float(r["ElectronAffinity_eV"]),
                 "Allen": float(r["AllenElectronegativity"])} for r in csv.DictReader(fh)]


def allen_conflicts(rows):
    """Rows whose Allen value differs from ALLEN_REFERENCE by more than the tolerance: (symbol, supplied, reference)."""
    return [(r["Symbol"], r["Allen"], ALLEN_REFERENCE[r["Symbol"]]) for r in rows
            if r["Symbol"] in ALLEN_REFERENCE and abs(r["Allen"] - ALLEN_REFERENCE[r["Symbol"]]) > ALLEN_TOLERANCE]
