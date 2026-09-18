"""SQLite implementation of AIR durable provenance adapter V1."""
from __future__ import annotations

import json
import sqlite3
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


class SQLiteDurableProvenanceProvider:
    provider_class = "SQLITE"
    storage_class = "LOCAL_DURABLE_SQLITE"

    def __init__(self, database: str | Path, *, authorization_state: str = "AUTHORIZED_LOCAL") -> None:
        self.database = str(Path(database).expanduser().resolve())
        self.authorization_state = authorization_state
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        return conn

    def _init_db(self) -> None:
        Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS provider_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            conn.execute("""CREATE TABLE IF NOT EXISTS namespaces (
                namespace_id TEXT PRIMARY KEY, namespace_fingerprint TEXT NOT NULL, project_identity_hash TEXT NOT NULL UNIQUE)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS records (
                namespace_id TEXT NOT NULL,
                ledger_entry_ref TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                canonical_object_sha256 TEXT NOT NULL,
                snapshot BLOB NOT NULL,
                record_json TEXT NOT NULL,
                record_state TEXT NOT NULL,
                PRIMARY KEY(namespace_id, ledger_entry_ref))""")
            existing = conn.execute("SELECT value FROM provider_meta WHERE key='adapter_identity'").fetchone()
            if existing and existing[0] != ADAPTER_IDENTITY:
                raise IntegrityError("provider metadata adapter identity mismatch")
            defaults = {
                "adapter_identity": ADAPTER_IDENTITY,
                "provider_generation": str(uuid.uuid4()),
                "provider_instance": str(uuid.uuid4()),
                "provider_class": self.provider_class,
            }
            for key, value in defaults.items():
                conn.execute("INSERT OR IGNORE INTO provider_meta(key,value) VALUES(?,?)", (key, value))

    def _meta(self) -> dict[str, str]:
        with self._connect() as conn:
            return {row[0]: row[1] for row in conn.execute("SELECT key,value FROM provider_meta")}

    def describe_provider(self) -> ProviderDescription:
        meta = self._meta()
        identity = sha256_bytes(self.database.encode("utf-8"))
        return ProviderDescription(
            ADAPTER_IDENTITY,
            f"sqlite:{identity}",
            self.provider_class,
            meta["provider_generation"],
            meta["provider_instance"],
            self.storage_class,
            self.authorization_state,
            (
                "WRITE_EXACT_CANONICAL_BYTES",
                "READBACK_EXACT_BYTES",
                "STABLE_RETRIEVE_BY_PROVENANCE_IDENTITY",
                "PROJECT_NAMESPACE_ISOLATION",
                "COMMITTED_RANGE_RETRIEVAL",
                "COVERAGE_VERIFICATION",
            ),
        )

    def probe_write_readback(self) -> Mapping[str, Any]:
        payload = canonical_json_bytes({"probe": str(uuid.uuid4()), "adapter": ADAPTER_IDENTITY})
        with self._connect() as conn:
            conn.execute("CREATE TEMP TABLE air_probe(payload BLOB NOT NULL)")
            conn.execute("INSERT INTO air_probe(payload) VALUES(?)", (payload,))
            readback = bytes(conn.execute("SELECT payload FROM air_probe").fetchone()[0])
        return {
            "state": STATE_AVAILABLE_VERIFIED if readback == payload else STATE_FAILED_INTEGRITY,
            "write_readback_state": "EXACT" if readback == payload else "MISMATCH",
            "sha256": sha256_bytes(payload),
        }

    def open_project_namespace(self, project_identity: str) -> NamespaceHandle:
        project_hash = sha256_bytes(project_identity.encode("utf-8"))
        namespace_id = f"air-project-{project_hash[:24]}"
        fingerprint = sha256_bytes(f"{ADAPTER_IDENTITY}:{project_hash}".encode("utf-8"))
        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO namespaces(namespace_id,namespace_fingerprint,project_identity_hash) VALUES(?,?,?)",
                (namespace_id, fingerprint, project_hash),
            )
            row = conn.execute(
                "SELECT namespace_fingerprint,project_identity_hash FROM namespaces WHERE namespace_id=?",
                (namespace_id,),
            ).fetchone()
            if not row or row[0] != fingerprint or row[1] != project_hash:
                raise IntegrityError("namespace identity mismatch")
        return NamespaceHandle(namespace_id, fingerprint, project_hash)

    @staticmethod
    def _sequence(ref: str) -> int:
        try:
            return int(ref.rsplit("::", 1)[1])
        except (IndexError, ValueError) as exc:
            raise IntegrityError(f"invalid ledger_entry_ref sequence: {ref}") from exc

    def prepare_snapshot(self, namespace: NamespaceHandle, record: Mapping[str, Any]) -> Mapping[str, Any]:
        record = dict(record)
        validate_record_shape(record)
        if record["record_state"] != RECORD_PREPARED:
            raise IntegrityError("prepare_snapshot requires PREPARED record_state")
        snapshot = canonical_json_bytes(record["canonical_object_snapshot"])
        if sha256_bytes(snapshot) != record["canonical_object_sha256"]:
            raise IntegrityError("canonical snapshot hash mismatch before persistence")
        persisted = dict(record)
        persisted["canonical_object_snapshot"] = None
        persisted["write_readback_state"] = "EXACT"
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT canonical_object_sha256 FROM records WHERE namespace_id=? AND ledger_entry_ref=?",
                (namespace.namespace_id, record["ledger_entry_ref"]),
            ).fetchone()
            if existing:
                if existing[0] != record["canonical_object_sha256"]:
                    raise IntegrityError("ledger_entry_ref already mapped to different snapshot")
            else:
                conn.execute(
                    "INSERT INTO records(namespace_id,ledger_entry_ref,sequence,canonical_object_sha256,snapshot,record_json,record_state) VALUES(?,?,?,?,?,?,?)",
                    (
                        namespace.namespace_id,
                        record["ledger_entry_ref"],
                        self._sequence(record["ledger_entry_ref"]),
                        record["canonical_object_sha256"],
                        snapshot,
                        json.dumps(persisted, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                        RECORD_PREPARED,
                    ),
                )
        return self.read_snapshot(namespace, record["ledger_entry_ref"])

    def read_snapshot(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT canonical_object_sha256,snapshot,record_json,record_state FROM records WHERE namespace_id=? AND ledger_entry_ref=?",
                (namespace.namespace_id, ledger_entry_ref),
            ).fetchone()
        if not row:
            raise RecordNotFound(ledger_entry_ref)
        snapshot = bytes(row[1])
        if sha256_bytes(snapshot) != row[0]:
            raise IntegrityError(f"stored snapshot hash mismatch: {ledger_entry_ref}")
        record = json.loads(row[2])
        record["record_state"] = row[3]
        record["canonical_object_snapshot"] = json.loads(snapshot.decode("utf-8"))
        validate_record_shape(record)
        return record

    def stable_retrieve(self, namespace: NamespaceHandle, ledger_entry_ref: str) -> Mapping[str, Any]:
        return self.read_snapshot(namespace, ledger_entry_ref)

    def _set_state(self, namespace: NamespaceHandle, ledger_entry_ref: str, state: str) -> Mapping[str, Any]:
        self.read_snapshot(namespace, ledger_entry_ref)
        with self._connect() as conn:
            conn.execute(
                "UPDATE records SET record_state=? WHERE namespace_id=? AND ledger_entry_ref=?",
                (state, namespace.namespace_id, ledger_entry_ref),
            )
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

    def retrieve_committed_range(self, namespace: NamespaceHandle, start_sequence: int, end_sequence: int) -> list[Mapping[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT ledger_entry_ref FROM records WHERE namespace_id=? AND record_state=? AND sequence BETWEEN ? AND ? ORDER BY sequence",
                (namespace.namespace_id, RECORD_COMMITTED_VISIBLE, start_sequence, end_sequence),
            ).fetchall()
        return [self.read_snapshot(namespace, row[0]) for row in rows]

    def verify_coverage(self, namespace: NamespaceHandle, expected: Iterable[Mapping[str, Any]]) -> CoverageResult:
        items = list(expected)
        missing = []
        mismatched = []
        committed = 0
        for item in items:
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
        return CoverageResult(state, len(items), committed, tuple(missing), tuple(mismatched))

    def cleanup_orphans(self, namespace: NamespaceHandle) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM records WHERE namespace_id=? AND record_state=?",
                (namespace.namespace_id, RECORD_ORPHANED),
            )
            return cur.rowcount
