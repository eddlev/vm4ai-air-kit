"""Filesystem implementation of AIR durable provenance adapter V1."""
from __future__ import annotations

import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import Any, Iterable, Mapping

from .canonical_json import canonical_json_bytes, sha256_bytes
from .contract import (
    ADAPTER_IDENTITY,
    CoverageResult,
    IntegrityError,
    NamespaceHandle,
    ProviderDescription,
    RecordNotFound,
    RECORD_COMMITTED_VISIBLE,
    RECORD_ORPHANED,
    RECORD_PREPARED,
    STATE_AVAILABLE_VERIFIED,
    STATE_DEGRADED_INCOMPLETE,
    STATE_FAILED_INTEGRITY,
    validate_record_shape,
)


class FilesystemDurableProvenanceProvider:
    provider_class = "FILESYSTEM"
    storage_class = "LOCAL_DURABLE_FILESYSTEM"

    def __init__(self, root: str | os.PathLike[str], *, authorization_state: str = "AUTHORIZED_LOCAL") -> None:
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.authorization_state = authorization_state
        self._provider_meta = self.root / "provider.json"
        self._ensure_provider_metadata()

    def _ensure_provider_metadata(self) -> None:
        if self._provider_meta.exists():
            data = json.loads(self._provider_meta.read_text(encoding="utf-8"))
            if data.get("adapter_identity") != ADAPTER_IDENTITY:
                raise IntegrityError("provider metadata adapter identity mismatch")
            return
        data = {
            "adapter_identity": ADAPTER_IDENTITY,
            "provider_generation": str(uuid.uuid4()),
            "provider_instance": str(uuid.uuid4()),
            "provider_class": self.provider_class,
        }
        self._atomic_write(self._provider_meta, canonical_json_bytes(data))

    def _meta(self) -> Mapping[str, Any]:
        return json.loads(self._provider_meta.read_text(encoding="utf-8"))

    @staticmethod
    def _atomic_write(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".air-prov-", dir=str(path.parent))
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    def describe_provider(self) -> ProviderDescription:
        meta = self._meta()
        identity = sha256_bytes(str(self.root).encode("utf-8"))
        return ProviderDescription(
            adapter_identity=ADAPTER_IDENTITY,
            provider_identity=f"filesystem:{identity}",
            provider_class=self.provider_class,
            provider_generation=meta["provider_generation"],
            provider_instance=meta["provider_instance"],
            storage_class=self.storage_class,
            authorization_state=self.authorization_state,
            capabilities=(
                "WRITE_EXACT_CANONICAL_BYTES",
                "READBACK_EXACT_BYTES",
                "STABLE_RETRIEVE_BY_PROVENANCE_IDENTITY",
                "PROJECT_NAMESPACE_ISOLATION",
                "COMMITTED_RANGE_RETRIEVAL",
                "COVERAGE_VERIFICATION",
            ),
        )

    def probe_write_readback(self) -> Mapping[str, Any]:
        probe_dir = self.root / ".probe"
        probe_dir.mkdir(exist_ok=True)
        payload = canonical_json_bytes({"probe": str(uuid.uuid4()), "adapter": ADAPTER_IDENTITY})
        path = probe_dir / f"{uuid.uuid4().hex}.json"
        self._atomic_write(path, payload)
        readback = path.read_bytes()
        path.unlink(missing_ok=True)
        return {
            "state": STATE_AVAILABLE_VERIFIED if readback == payload else STATE_FAILED_INTEGRITY,
            "write_readback_state": "EXACT" if readback == payload else "MISMATCH",
            "sha256": sha256_bytes(payload),
        }

    def open_project_namespace(self, project_identity: str) -> NamespaceHandle:
        project_hash = sha256_bytes(project_identity.encode("utf-8"))
        namespace_id = f"air-project-{project_hash[:24]}"
        fingerprint = sha256_bytes(f"{ADAPTER_IDENTITY}:{project_hash}".encode("utf-8"))
        (self.root / "namespaces" / namespace_id / "records").mkdir(parents=True, exist_ok=True)
        return NamespaceHandle(namespace_id, fingerprint, project_hash)

    def _record_paths(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> tuple[Path, Path]:
        ref_hash = sha256_bytes(ledger_entry_ref.encode("utf-8"))
        base = self.root / "namespaces" / namespace.namespace_id / "records" / ref_hash
        return base.with_suffix(".record.json"), base.with_suffix(".snapshot.json")

    def prepare_snapshot(self, namespace: NamespaceHandle, record: Mapping[str, Any]) -> Mapping[str, Any]:
        record = dict(record)
        validate_record_shape(record)
        if record["record_state"] != RECORD_PREPARED:
            raise IntegrityError("prepare_snapshot requires PREPARED record_state")
        snapshot_bytes = canonical_json_bytes(record["canonical_object_snapshot"])
        if sha256_bytes(snapshot_bytes) != record["canonical_object_sha256"]:
            raise IntegrityError("canonical snapshot hash mismatch before persistence")
        meta_path, snapshot_path = self._record_paths(namespace, record["ledger_entry_ref"])
        if meta_path.exists():
            existing = self.read_snapshot(namespace, record["ledger_entry_ref"])
            if existing["canonical_object_sha256"] != record["canonical_object_sha256"]:
                raise IntegrityError("ledger_entry_ref already mapped to different snapshot")
            return existing
        self._atomic_write(snapshot_path, snapshot_bytes)
        record["write_readback_state"] = "EXACT"
        persisted = dict(record)
        persisted["canonical_object_snapshot"] = None
        self._atomic_write(meta_path, canonical_json_bytes(persisted))
        return self.read_snapshot(namespace, record["ledger_entry_ref"])

    def read_snapshot(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]:
        meta_path, snapshot_path = self._record_paths(namespace, ledger_entry_ref)
        if not meta_path.exists() or not snapshot_path.exists():
            raise RecordNotFound(ledger_entry_ref)
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        snapshot_bytes = snapshot_path.read_bytes()
        if sha256_bytes(snapshot_bytes) != meta["canonical_object_sha256"]:
            raise IntegrityError(f"stored snapshot hash mismatch: {ledger_entry_ref}")
        snapshot = json.loads(snapshot_bytes.decode("utf-8"))
        result = dict(meta)
        result["canonical_object_snapshot"] = snapshot
        validate_record_shape(result)
        return result

    def stable_retrieve(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]:
        return self.read_snapshot(namespace, ledger_entry_ref)

    def _set_state(self, namespace: NamespaceHandle, ledger_entry_ref: str, state: str) -> Mapping[str, Any]:
        meta_path, _ = self._record_paths(namespace, ledger_entry_ref)
        current = self.read_snapshot(namespace, ledger_entry_ref)
        meta = dict(current)
        meta["record_state"] = state
        meta["canonical_object_snapshot"] = None
        self._atomic_write(meta_path, canonical_json_bytes(meta))
        return self.read_snapshot(namespace, ledger_entry_ref)

    def commit_visible(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]:
        current = self.read_snapshot(namespace, ledger_entry_ref)
        if current["record_state"] not in {RECORD_PREPARED, RECORD_COMMITTED_VISIBLE}:
            raise IntegrityError("only PREPARED record can become COMMITTED_VISIBLE")
        return self._set_state(namespace, ledger_entry_ref, RECORD_COMMITTED_VISIBLE)

    def mark_orphaned(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]:
        current = self.read_snapshot(namespace, ledger_entry_ref)
        if current["record_state"] == RECORD_COMMITTED_VISIBLE:
            raise IntegrityError("committed visible record cannot be retroactively orphaned")
        return self._set_state(namespace, ledger_entry_ref, RECORD_ORPHANED)

    @staticmethod
    def _sequence(ledger_entry_ref: str) -> int:
        try:
            return int(ledger_entry_ref.rsplit("::", 1)[1])
        except (IndexError, ValueError) as exc:
            raise IntegrityError(f"invalid ledger_entry_ref sequence: {ledger_entry_ref}") from exc

    def retrieve_committed_range(self, namespace: NamespaceHandle, start_sequence: int, end_sequence: int) -> list[Mapping[str, Any]]:
        records_dir = self.root / "namespaces" / namespace.namespace_id / "records"
        result = []
        for meta_path in sorted(records_dir.glob("*.record.json")):
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("record_state") != RECORD_COMMITTED_VISIBLE:
                continue
            seq = self._sequence(meta["ledger_entry_ref"])
            if start_sequence <= seq <= end_sequence:
                result.append(self.read_snapshot(namespace, meta["ledger_entry_ref"]))
        return sorted(result, key=lambda r: self._sequence(r["ledger_entry_ref"]))

    def verify_coverage(self, namespace: NamespaceHandle, expected: Iterable[Mapping[str, Any]]) -> CoverageResult:
        missing = []
        mismatched = []
        committed = 0
        expected_list = list(expected)
        for item in expected_list:
            ref = item["ledger_entry_ref"]
            try:
                stored = self.read_snapshot(namespace, ref)
            except RecordNotFound:
                missing.append(ref)
                continue
            except IntegrityError:
                mismatched.append(ref)
                continue
            if stored["record_state"] != RECORD_COMMITTED_VISIBLE:
                missing.append(ref)
                continue
            if stored["canonical_object_sha256"] != item["canonical_object_sha256"]:
                mismatched.append(ref)
                continue
            if item.get("object_identity") is not None and stored.get("object_identity") != item["object_identity"]:
                mismatched.append(ref)
                continue
            committed += 1
        state = STATE_FAILED_INTEGRITY if mismatched else (STATE_DEGRADED_INCOMPLETE if missing else STATE_AVAILABLE_VERIFIED)
        return CoverageResult(state, len(expected_list), committed, tuple(missing), tuple(mismatched))

    def cleanup_orphans(self, namespace: NamespaceHandle) -> int:
        records_dir = self.root / "namespaces" / namespace.namespace_id / "records"
        removed = 0
        for meta_path in records_dir.glob("*.record.json"):
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("record_state") != RECORD_ORPHANED:
                continue
            _, snapshot_path = self._record_paths(namespace, meta["ledger_entry_ref"])
            meta_path.unlink(missing_ok=True)
            snapshot_path.unlink(missing_ok=True)
            removed += 1
        return removed
