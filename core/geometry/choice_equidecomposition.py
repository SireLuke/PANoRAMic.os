"""Finite choice and equidecomposition research primitives.

Executable finite mathematics is kept separate from nonconstructive existence
principles such as full AC and Banach-Tarski. No nonmeasurable sets or physical
matter duplication are constructed here.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Hashable, Iterable, Mapping, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)


class SelectionKind(str, Enum):
    CONSTRUCTIVE = "constructive"
    EXISTENCE_ONLY = "existence_only"


@dataclass(frozen=True)
class SelectionRecord:
    family_key: str
    selected_repr: str
    method: str
    alternatives_preserved: bool = True


def finite_choice(family: Mapping[str, Sequence[T]],
                  selector: Callable[[str, Sequence[T]], T] | None = None
                  ) -> tuple[dict[str, T], tuple[SelectionRecord, ...]]:
    """Choose one member from each finite nonempty family member.

    Default ordering by type name and repr is deterministic, not semantically
    privileged. Supply a domain selector when the application has criteria.
    The input family is never mutated; alternatives remain available.
    """
    chosen: dict[str, T] = {}
    records: list[SelectionRecord] = []
    for key in sorted(family):
        candidates = tuple(family[key])
        if not candidates:
            raise ValueError(f"choice family member {key!r} is empty")
        if selector is None:
            value = sorted(candidates, key=lambda item: (type(item).__name__, repr(item)))[0]
            method = "deterministic_repr_order"
        else:
            value = selector(key, candidates)
            method = getattr(selector, "__name__", "caller_selector")
        if value not in candidates:
            raise ValueError(f"selector returned an element outside {key!r}")
        chosen[key] = value
        records.append(SelectionRecord(key, repr(value), method, True))
    return chosen, tuple(records)


@dataclass(frozen=True)
class ChoiceExistenceClaim:
    """Symbolic marker for full AC; this is not an algorithm."""
    family_description: str
    assumptions: tuple[str, ...] = ("every family member is nonempty",)
    selection_kind: SelectionKind = SelectionKind.EXISTENCE_ONLY

    def __post_init__(self) -> None:
        if not self.family_description.strip():
            raise ValueError("family_description must be nonempty")
        if self.selection_kind is not SelectionKind.EXISTENCE_ONLY:
            raise ValueError("full AC claims are existence-only in this module")


@dataclass(frozen=True)
class FiniteGroupAction:
    """Finite group represented by permutations of a finite carrier."""
    carrier: tuple[Hashable, ...]
    elements: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        n = len(self.carrier)
        identity = tuple(range(n))
        if len(set(self.carrier)) != n:
            raise ValueError("carrier elements must be unique")
        if identity not in self.elements or len(set(self.elements)) != len(self.elements):
            raise ValueError("group must contain a unique identity and unique elements")
        for p in self.elements:
            if len(p) != n or set(p) != set(range(n)):
                raise ValueError("each group element must be a carrier permutation")
        element_set = set(self.elements)
        for left in self.elements:
            if not any(all(left[right[i]] == i for i in range(n)) for right in self.elements):
                raise ValueError("group element has no inverse")
            for right in self.elements:
                if tuple(left[right[i]] for i in range(n)) not in element_set:
                    raise ValueError("permutation set is not closed")

    def apply(self, permutation: tuple[int, ...],
              subset: Iterable[Hashable]) -> frozenset[Hashable]:
        if permutation not in self.elements:
            raise ValueError("transformation is not in this group")
        index = {value: i for i, value in enumerate(self.carrier)}
        values = frozenset(subset)
        if not values.issubset(index):
            raise ValueError("subset contains values outside the carrier")
        return frozenset(self.carrier[permutation[index[value]]] for value in values)


@dataclass(frozen=True)
class PieceMove:
    piece_id: str
    target_id: str
    transformation: tuple[int, ...]


@dataclass(frozen=True)
class FiniteEquidecompositionCertificate:
    """Check a finite source partition moved onto two target sets.

    This finite certificate is not a Banach-Tarski construction.
    """
    source: frozenset[Hashable]
    target_a: frozenset[Hashable]
    target_b: frozenset[Hashable]
    pieces: Mapping[str, frozenset[Hashable]]
    moves: tuple[PieceMove, ...]
    group: FiniteGroupAction

    def validate(self) -> bool:
        if not self.source.issubset(self.group.carrier):
            raise ValueError("source outside group carrier")
        if not self.target_a.issubset(self.group.carrier) or not self.target_b.issubset(self.group.carrier):
            raise ValueError("targets outside group carrier")
        if not self.pieces or any(not piece for piece in self.pieces.values()):
            raise ValueError("certificate requires nonempty pieces")
        union: set[Hashable] = set()
        for piece in self.pieces.values():
            if union.intersection(piece):
                raise ValueError("source pieces overlap")
            union.update(piece)
        if frozenset(union) != self.source:
            raise ValueError("source pieces do not partition source")
        if len(self.moves) != len(self.pieces) or {m.piece_id for m in self.moves} != set(self.pieces):
            raise ValueError("each piece must have exactly one move")
        moved: dict[str, list[frozenset[Hashable]]] = {"A": [], "B": []}
        targets = {"A": self.target_a, "B": self.target_b}
        for move in self.moves:
            if move.target_id not in targets:
                raise ValueError("target_id must be A or B")
            moved[move.target_id].append(
                self.group.apply(move.transformation, self.pieces[move.piece_id]))
        for target_id, target in targets.items():
            combined: set[Hashable] = set()
            for piece in moved[target_id]:
                if combined.intersection(piece):
                    raise ValueError(f"moved pieces overlap in target {target_id}")
                combined.update(piece)
            if frozenset(combined) != target:
                raise ValueError(f"moved pieces do not partition target {target_id}")
        return True


class MeasureStatus(str, Enum):
    MEASURABLE = "measurable"
    NONMEASURABLE = "nonmeasurable"
    UNASSIGNED = "unassigned"


@dataclass(frozen=True)
class MeasureLedger:
    """Refuse ordinary scalar measure for nonmeasurable/unassigned objects."""
    object_id: str
    status: MeasureStatus
    measure_value: float | None = None
    note: str = ""

    def __post_init__(self) -> None:
        if not self.object_id.strip():
            raise ValueError("object_id must be nonempty")
        if self.status is MeasureStatus.MEASURABLE and self.measure_value is None:
            raise ValueError("measurable objects require a measure value")
        if self.status is not MeasureStatus.MEASURABLE and self.measure_value is not None:
            raise ValueError("do not assign scalar measure to nonmeasurable/unassigned objects")


def banach_tarski_scope_note() -> dict[str, str]:
    """State the theorem boundary; deliberately no geometric construction."""
    return {
        "status": "abstract_existence_theorem",
        "depends_on": "Axiom of Choice (in standard proofs)",
        "domain": "three-dimensional Euclidean ball under rigid motions",
        "pieces": "finite partition into nonmeasurable subsets",
        "measure": "ordinary Lebesgue volume is not defined for the pieces",
        "physical_interpretation": "no matter duplication and no executable physical process",
        "implementation": "not constructed by this finite certificate module",
    }
