"""Small, dependency-free STRATA reporting primitives."""
from dataclasses import dataclass, asdict
from typing import Dict, Iterable
import json

STATUSES = {"pass", "fail", "inconclusive", "not_tested"}

@dataclass(frozen=True)
class DimensionResult:
    dimension: str
    status: str
    detail: str

    def __post_init__(self):
        if self.status not in STATUSES:
            raise ValueError(f"invalid status: {self.status}")

@dataclass
class StrataReport:
    claim_id: str
    hypothesis: str
    evidence_level: str
    seed: int
    dimensions: list
    limitations: list

    def validate(self):
        names = [item.dimension for item in self.dimensions]
        if len(names) != len(set(names)):
            raise ValueError("dimension names must be unique")
        return self

    def to_dict(self):
        self.validate()
        return {
            "protocol": "STRATA-0.1",
            "claim_id": self.claim_id,
            "hypothesis": self.hypothesis,
            "evidence_level": self.evidence_level,
            "seed": self.seed,
            "dimensions": [asdict(x) for x in self.dimensions],
            "limitations": self.limitations,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

def retention(reference: Iterable, transformed: Iterable) -> float:
    """Jaccard retention for discrete feature sets; undefined empty/empty is 1."""
    a, b = set(reference), set(transformed)
    union = a | b
    return 1.0 if not union else len(a & b) / len(union)

def permutation_control(values, seed=20261109):
    """Deterministic shuffled control; caller must choose a meaningful statistic."""
    import random
    result = list(values)
    random.Random(seed).shuffle(result)
    return result
