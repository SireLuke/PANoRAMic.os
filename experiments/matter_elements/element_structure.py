"""Rule-derived structure of the periodic table (no measured data), plus a validator for sourced data.

What is DERIVED here (and tested): period lengths, blocks, subshell capacities and the Madelung
(n + l, then n) predicted ground-state configurations for Z = 1..118, and a 18-column / f-row layout.
What is NOT here: atomic masses, radii, electronegativities, ionisation energies, observed ground-state
configurations. Those are measured data and must be loaded from a sourced file (NIST / IUPAC CIAAW /
PubChem) via ``validate_table``; this module records no numbers from memory.

Symbols and names are definitional (IUPAC); they are checked for internal consistency only.
Convention notes: He is shown in group 18 although its last subshell is 1s; La and Ac head the f-rows and
Lu, Lr are placed in group 3 (the IUPAC 2021 provisional recommendation); other layouts are possible.
The Madelung rule is an empirical filling order and is wrong for about 20 elements (e.g. Cr, Cu, Pd, Ag, Au);
``madelung_config`` therefore returns a *prediction* and never an observed configuration.
"""
from __future__ import annotations

import csv
import re
from typing import Iterable

SYMBOLS = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr "
           "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb "
           "Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr "
           "Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og").split()
NAMES = ("Hydrogen Helium Lithium Beryllium Boron Carbon Nitrogen Oxygen Fluorine Neon Sodium Magnesium Aluminium "
         "Silicon Phosphorus Sulfur Chlorine Argon Potassium Calcium Scandium Titanium Vanadium Chromium Manganese "
         "Iron Cobalt Nickel Copper Zinc Gallium Germanium Arsenic Selenium Bromine Krypton Rubidium Strontium "
         "Yttrium Zirconium Niobium Molybdenum Technetium Ruthenium Rhodium Palladium Silver Cadmium Indium Tin "
         "Antimony Tellurium Iodine Xenon Caesium Barium Lanthanum Cerium Praseodymium Neodymium Promethium Samarium "
         "Europium Gadolinium Terbium Dysprosium Holmium Erbium Thulium Ytterbium Lutetium Hafnium Tantalum Tungsten "
         "Rhenium Osmium Iridium Platinum Gold Mercury Thallium Lead Bismuth Polonium Astatine Radon Francium Radium "
         "Actinium Thorium Protactinium Uranium Neptunium Plutonium Americium Curium Berkelium Californium Einsteinium "
         "Fermium Mendelevium Nobelium Lawrencium Rutherfordium Dubnium Seaborgium Bohrium Hassium Meitnerium "
         "Darmstadtium Roentgenium Copernicium Nihonium Flerovium Moscovium Livermorium Tennessine Oganesson").split()

SUBSHELL_LETTER = "spdf"
NOBLE_Z = (2, 10, 18, 36, 54, 86, 118)


def madelung_order(max_n: int = 8):
    """Subshells (n, l) sorted by n + l, then n, restricted to l <= 3 (s, p, d, f)."""
    cells = [(n, l) for n in range(1, max_n + 1) for l in range(0, min(n, 4))]
    return sorted(cells, key=lambda c: (c[0] + c[1], c[0]))


def capacity(l: int) -> int:
    return 2 * (2 * l + 1)


def madelung_config(z: int) -> list:
    """Predicted occupation [(n, l, electrons), ...] for atomic number z (1..118)."""
    if isinstance(z, bool) or not isinstance(z, int) or not 1 <= z <= 118:
        raise ValueError("z must be an integer in 1..118")
    left, out = z, []
    for n, l in madelung_order():
        if left == 0:
            break
        take = min(left, capacity(l))
        out.append((n, l, take))
        left -= take
    if left:
        raise ValueError("ran out of subshells")        # unreachable for z <= 118 with n <= 8
    return out


def config_string(config) -> str:
    return " ".join(f"{n}{SUBSHELL_LETTER[l]}{e}" for n, l, e in sorted(config, key=lambda c: (c[0], c[1])))


def period_of(z: int) -> int:
    """Period = principal quantum number of the outermost occupied shell (He, H -> 1)."""
    return max(n for n, _, _ in madelung_config(z))


def block_of(z: int) -> str:
    """Block from the last-filled subshell in Madelung order (He is 's' by filling)."""
    n, l, _ = madelung_config(z)[-1]
    return SUBSHELL_LETTER[l]


def layout(z: int) -> dict:
    """(row, column) on the 18-column long form; f-block elements go on two extra rows below.
    Convention: He in column 18; La/Ac start the f-rows; Lu/Lr sit in group 3."""
    if not 1 <= z <= 118:
        raise ValueError("z must be an integer in 1..118")
    period = period_of(z)
    block = block_of(z)
    if z == 2:
        return {"period": 1, "block": "s", "group": 18, "row": 1, "col": 18}
    cfg = madelung_config(z)
    if block == "f":
        idx = [zz for zz in range(1, 119) if block_of(zz) == "f"]
        rank = idx.index(z)
        # Madelung fills 4f then 5d, so the 14 f-block elements are La..Yb (57..70) and Ac..No (89..102);
        # Lu (5d1) and Lr (6d1) then fall in the d-block, group 3.
        row_f = 8 if z < 80 else 9
        return {"period": period, "block": "f", "group": None, "row": row_f, "col": 3 + (rank % 14)}
    last_n, last_l, e = cfg[-1]
    if block == "s":
        group = e if z != 2 else 18
    elif block == "d":
        group = 2 + e
        # a d-subshell filled over a full f-subshell + s^2 keeps its group; Lu/Lr (d^1 after f14) -> group 3
    else:
        group = 12 + e
    return {"period": period, "block": block, "group": group, "row": period, "col": group}


def period_lengths() -> list:
    return [NOBLE_Z[0]] + [NOBLE_Z[i] - NOBLE_Z[i - 1] for i in range(1, len(NOBLE_Z))]


def validate_table(rows: Iterable[dict], mass_key: str = "AtomicMass", z_key: str = "AtomicNumber",
                   symbol_key: str = "Symbol") -> dict:
    """Consistency report for a SOURCED element table (list of dicts). Returns findings; never edits data."""
    rows = list(rows)
    findings = {"errors": [], "mass_order_inversions": [], "rows": len(rows)}
    zs = []
    for r in rows:
        try:
            z = int(r[z_key])
        except (KeyError, ValueError, TypeError):
            findings["errors"].append(f"bad atomic number: {r.get(z_key)!r}")
            continue
        zs.append(z)
        if 1 <= z <= 118 and r.get(symbol_key) != SYMBOLS[z - 1]:
            findings["errors"].append(f"Z={z}: symbol {r.get(symbol_key)!r} != {SYMBOLS[z - 1]!r}")
    if sorted(zs) != list(range(1, 119)):
        findings["errors"].append("atomic numbers are not exactly 1..118 once each")
    by_z = {}
    for r in rows:
        try:
            by_z[int(r[z_key])] = r
        except (KeyError, ValueError, TypeError):
            pass
    prev = None
    for z in sorted(by_z):
        try:
            m = float(str(by_z[z][mass_key]).split("(")[0].strip("[] "))
        except (KeyError, ValueError):
            continue
        if m <= 0:
            findings["errors"].append(f"Z={z}: non-positive mass")
        if prev and m < prev[1]:
            findings["mass_order_inversions"].append([prev[0], z])
        prev = (z, m)
    return findings


def load_csv(path: str) -> list:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))
