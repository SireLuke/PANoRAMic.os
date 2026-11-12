"""Checks of a supplied PubChem element table against the rule-derived structure.

No value is edited. Everything returned is a finding: validator output, observed-vs-Madelung
configuration differences, and GroupBlock-vs-layout conflicts. Units are not stated in the file.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

try:
    from . import element_structure as E
except ImportError:
    import element_structure as E

DATA = Path(__file__).resolve().parent / "data" / "PubChemElements_all.csv"
NOBLE = {"He": 2, "Ne": 10, "Ar": 18, "Kr": 36, "Xe": 54, "Rn": 86}


def sha256(path=DATA) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_config(text: str):
    """Observed configuration -> ({(n, l): electrons}, note). Expands a noble-gas core."""
    note = "predicted" if "predicted" in text else "calculated" if "calculated" in text else ""
    text = re.sub(r"\(.*?\)", "", text).strip()
    occ, m = {}, re.match(r"\[(\w+)\]", text)
    if m:
        for n, l, e in E.madelung_config(NOBLE[m.group(1)]):
            occ[(n, l)] = e
        text = text[m.end():]
    for tok in text.split():
        t = re.fullmatch(r"(\d)([spdf])(\d+)", tok)
        if not t:
            raise ValueError(f"bad subshell token {tok!r}")
        occ[(int(t.group(1)), "spdf".index(t.group(2)))] = int(t.group(3))
    return occ, note


def config_differences(rows):
    """[(Z, symbol, note, {subshell: (madelung, observed)})] for rows whose configuration differs from the rule."""
    out = []
    for r in rows:
        z = int(r["AtomicNumber"])
        occ, note = parse_config(r["ElectronConfiguration"])
        pred = {(n, l): e for n, l, e in E.madelung_config(z)}
        if occ != pred:
            d = {f"{n}{'spdf'[l]}": (pred.get((n, l), 0), occ.get((n, l), 0))
                 for (n, l) in sorted(set(pred) | set(occ)) if pred.get((n, l), 0) != occ.get((n, l), 0)}
            out.append((z, r["Symbol"], note, d))
    return out


def configs_with_wrong_electron_count(rows):
    return [(int(r["AtomicNumber"]), r["Symbol"]) for r in rows
            if sum(parse_config(r["ElectronConfiguration"])[0].values()) != int(r["AtomicNumber"])]


def group_block_conflicts(rows):
    """Rows whose GroupBlock label disagrees with the Madelung-derived block of the layout."""
    want = {"Lanthanide": "f", "Actinide": "f", "Transition metal": "d"}
    return [(int(r["AtomicNumber"]), r["Symbol"], r["GroupBlock"], E.layout(int(r["AtomicNumber"]))["block"])
            for r in rows if r["GroupBlock"] in want and E.layout(int(r["AtomicNumber"]))["block"] != want[r["GroupBlock"]]]


def load(path=DATA):
    return E.load_csv(str(path))
