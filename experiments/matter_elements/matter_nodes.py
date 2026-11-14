"""Build the MatterNode catalog (JSON matching core/library/types.ts) from the element grid and molecule tables.

Elements carry the declared V8 state (v8_element_map v0). Molecules and ions carry an all-null V8 state and no mapping:
no V8 map is declared for them. Units of the PubChem table are recorded as unverified. Nothing here is a physical claim.
"""
from __future__ import annotations

import json
from pathlib import Path

try:
    from . import grid_layout as G
    from . import pubchem_elements as P
    from . import v8_element_map as M
except ImportError:
    import grid_layout as G
    import pubchem_elements as P
    import v8_element_map as M

_HERE = Path(__file__).resolve().parent
_MOL = _HERE.parent / "matter_molecules" / "data" / "molecules_starter.json"
OUT = _HERE / "matter_nodes.json"
ORBITALS = "experiments/matter_splats/orbital_splats.json"
UNITS = {"Electronegativity": None, "AtomicRadius": "pm", "IonizationEnergy": "eV", "MeltingPoint": "K",
         "BoilingPoint": "K", "Density": "g/cm3"}


def _sha(path):
    return json.loads(Path(path).read_text())["sha256"]


def sources():
    d = _HERE / "data"
    mol_prov = json.loads(_MOL.read_text())["provenance"]["supplied_by_user"]
    return [
        {"id": "pubchem-elements", "file": "experiments/matter_elements/data/PubChemElements_all.csv",
         "sha256": _sha(d / "PubChemElements_all.provenance.json"),
         "origin": "PubChem periodic table CSV export, as supplied by the repository owner", "verified": False},
        {"id": "reference-pdf", "file": "experiments/matter_molecules/data/molecules_starter.json",
         "sha256": mol_prov.split("sha256 ")[1].split(",")[0],
         "origin": "user-supplied one-page PDF; H3+ added from Wikipedia", "verified": False},
    ]


def _mapping_ref():
    return {"id": "matter-element-v8-map", "version": "v0", "claimLevel": "declared-hypothesis",
            "schemaOwner": "pan-fractal-kernel", "channelSources": dict(M.SOURCES),
            "researchNote": "research/MATTER_ELEMENT_V8_MAP.md"}


def element_nodes(rows):
    nodes = []
    for rec, row in zip(G.records(rows), rows):
        measured = [{"name": k, "value": (float(row[k]) if row[k] != "" else None), "unit": u,
                     "unitVerified": False, "sourceId": "pubchem-elements"} for k, u in UNITS.items()]
        views = [{"kind": "grid", "status": "available", "ref": "experiments/matter_elements/grid_elements.json"},
                 {"kind": "orbitals", "status": "available" if rec["Symbol"] == "H" else "planned",
                  "ref": ORBITALS if rec["Symbol"] == "H" else None},
                 {"kind": "nucleus", "status": "planned", "ref": None}]
        nodes.append({"id": f"matter:element:{rec['Symbol']}", "kind": "element", "title": rec["Name"],
                      "libraryNodeId": None,
                      "element": {"atomicNumber": rec["Z"], "symbol": rec["Symbol"], "name": rec["Name"],
                                  "grid": {"row": rec["row"], "col": rec["col"], "period": rec["period"],
                                           "group": rec["group"], "block": rec["block"]}},
                      "molecule": None, "v8": rec["V8"], "v8Mapping": _mapping_ref(), "measured": measured,
                      "views": views, "sourceIds": ["pubchem-elements"], "claimLevel": "declared-hypothesis"})
    return nodes


def molecule_nodes():
    nodes = []
    for m in json.loads(_MOL.read_text())["molecules"]:
        ion = m["charge"] != 0
        label = m["formula"] + ("+" if m["charge"] > 0 else "-" if m["charge"] < 0 else "")
        nodes.append({"id": f"matter:{'ion' if ion else 'molecule'}:{label}", "kind": "ion" if ion else "molecule",
                      "title": m["name"], "libraryNodeId": None, "element": None,
                      "molecule": {"formula": m["formula"], "smiles": m["smiles"], "charge": m["charge"],
                                   "bondName": m["bond_name"], "bondLengthAngstrom": m["bond_length_A"],
                                   "angleName": m["angle_name"], "bondAngleDegrees": m["bond_angle_deg"],
                                   "sourceId": "reference-pdf"},
                      "v8": {k: None for k in M.COORDS}, "v8Mapping": None, "measured": [],
                      "views": [{"kind": "molecule", "status": "planned", "ref": None}],
                      "sourceIds": ["reference-pdf"], "claimLevel": "declared-hypothesis"})
    return nodes


def build(rows=None):
    rows = rows if rows is not None else P.load()
    return {"schema": "MatterCatalog v0 (core/library/types.ts); declared, non-canonical",
            "sources": sources(), "nodes": element_nodes(rows) + molecule_nodes()}


def export(path=OUT):
    Path(path).write_text(json.dumps(build(), indent=1))


if __name__ == "__main__":
    export()
