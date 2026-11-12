"""Research reference implementation for additive, memory-preserving seed sharing.

This module is deliberately not wired into the production world lifecycle.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


class SeedContractError(ValueError):
    """Base error for malformed or conflicting seed envelopes."""


class SeedIdentityCollision(SeedContractError):
    """Raised when one seed ID is reused for different canonical content."""


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise SeedContractError("seed content must be finite JSON data") from exc


@dataclass(frozen=True)
class SeedEnvelope:
    seed_id: str
    source_id: str
    version: str
    payload: Mapping[str, Any]
    parent_seed_ids: tuple[str, ...] = ()

    def canonical_record(self) -> dict[str, Any]:
        if not self.seed_id.strip() or not self.source_id.strip() or not self.version.strip():
            raise SeedContractError("seed_id, source_id, and version must be non-empty")
        if self.seed_id in self.parent_seed_ids:
            raise SeedContractError("a seed cannot name itself as a parent")
        record = {
            "seed_id": self.seed_id,
            "source_id": self.source_id,
            "version": self.version,
            "parent_seed_ids": list(self.parent_seed_ids),
            "payload": deepcopy(dict(self.payload)),
        }
        _canonical_json(record)
        return record

    def to_record(self) -> dict[str, Any]:
        record = self.canonical_record()
        record["content_sha256"] = sha256(_canonical_json(record).encode("utf-8")).hexdigest()
        return record


@dataclass
class ReceiverState:
    base_memory: dict[str, Any] = field(default_factory=dict)
    seed_ledger: dict[str, dict[str, Any]] = field(default_factory=dict)


def share_seed(receiver: ReceiverState, envelope: SeedEnvelope) -> ReceiverState:
    """Return a new receiver with an additive seed ledger entry.

    The receiver's base_memory is copied unchanged. Existing ledger entries are
    preserved. Repeated identical shares are idempotent; conflicting reuse of
    a seed ID is rejected rather than overwritten.
    """
    record = envelope.to_record()
    seed_id = record["seed_id"]
    existing = receiver.seed_ledger.get(seed_id)
    if existing is not None:
        if _canonical_json(existing) != _canonical_json(record):
            raise SeedIdentityCollision(
                f"seed ID {seed_id!r} already exists with different content"
            )
        return deepcopy(receiver)

    updated = deepcopy(receiver)
    updated.seed_ledger[seed_id] = record
    return updated
