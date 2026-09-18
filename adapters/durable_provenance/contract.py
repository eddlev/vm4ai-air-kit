"""Provider-neutral contract for AIR durable surfaced-object provenance."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Protocol, runtime_checkable

ADAPTER_IDENTITY = "AIR_DURABLE_PROVENANCE_PROVIDER_ADAPTER_V1"
POSITIVE_EXECUTION_AUTHORITY = "NONE"

STATE_AVAILABLE_VERIFIED = "AVAILABLE_VERIFIED"
STATE_UNAVAILABLE = "UNAVAILABLE"
STATE_DEGRADED_INCOMPLETE = "DEGRADED_INCOMPLETE"
STATE_FAILED_INTEGRITY = "FAILED_INTEGRITY"

ELIGIBLE = "ELIGIBLE"
INELIGIBLE_UNAVAILABLE = "INELIGIBLE_UNAVAILABLE"
INELIGIBLE_INCOMPLETE = "INELIGIBLE_INCOMPLETE"
BLOCKED_FAILED_INTEGRITY = "BLOCKED_FAILED_INTEGRITY"

RECORD_PREPARED = "PREPARED"
RECORD_COMMITTED_VISIBLE = "COMMITTED_VISIBLE"
RECORD_ORPHANED = "ORPHANED"


class DurableProvenanceError(RuntimeError):
    pass


class IntegrityError(DurableProvenanceError):
    pass


class RecordNotFound(DurableProvenanceError):
    pass


@dataclass(frozen=True)
class ProviderDescription:
    adapter_identity: str
    provider_identity: str
    provider_class: str
    provider_generation: str
    provider_instance: str
    storage_class: str
    authorization_state: str
    capabilities: tuple[str, ...]
    positive_execution_authority: str = POSITIVE_EXECUTION_AUTHORITY


@dataclass(frozen=True)
class NamespaceHandle:
    namespace_id: str
    namespace_fingerprint: str
    project_identity_hash: str


@dataclass(frozen=True)
class CoverageResult:
    state: str
    expected_count: int
    committed_count: int
    missing_refs: tuple[str, ...]
    mismatched_refs: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return self.state == STATE_AVAILABLE_VERIFIED


def normalized_eligibility(state: str) -> str:
    return {
        STATE_AVAILABLE_VERIFIED: ELIGIBLE,
        STATE_UNAVAILABLE: INELIGIBLE_UNAVAILABLE,
        STATE_DEGRADED_INCOMPLETE: INELIGIBLE_INCOMPLETE,
        STATE_FAILED_INTEGRITY: BLOCKED_FAILED_INTEGRITY,
    }[state]


def required_record_fields() -> tuple[str, ...]:
    return (
        "provenance_store_id",
        "ledger_entry_ref",
        "canonical_object_sha256",
        "canonical_object_snapshot",
        "record_state",
        "source_message_count",
        "source_state_epoch",
        "object_name",
        "object_identity",
        "persistence_provider_class",
        "write_readback_state",
    )


def validate_record_shape(record: Mapping[str, Any]) -> None:
    missing = [field for field in required_record_fields() if field not in record]
    if missing:
        raise IntegrityError(f"missing provenance record fields: {missing}")
    if record["record_state"] not in {
        RECORD_PREPARED,
        RECORD_COMMITTED_VISIBLE,
        RECORD_ORPHANED,
    }:
        raise IntegrityError(f"invalid record_state: {record['record_state']!r}")


@runtime_checkable
class DurableProvenanceProvider(Protocol):
    def describe_provider(self) -> ProviderDescription: ...
    def probe_write_readback(self) -> Mapping[str, Any]: ...
    def stable_retrieve(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]: ...
    def open_project_namespace(self, project_identity: str) -> NamespaceHandle: ...
    def prepare_snapshot(self, namespace: NamespaceHandle, record: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def read_snapshot(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]: ...
    def commit_visible(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]: ...
    def mark_orphaned(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]: ...
    def retrieve_committed_range(self, namespace: NamespaceHandle, start_sequence: int, end_sequence: int) -> list[Mapping[str, Any]]: ...
    def verify_coverage(self, namespace: NamespaceHandle, expected: Iterable[Mapping[str, Any]]) -> CoverageResult: ...
    def cleanup_orphans(self, namespace: NamespaceHandle) -> int: ...
