#!/usr/bin/env python3
"""Negative/mutation checks for AIR durable provenance provider V1."""
from __future__ import annotations

import json
import sqlite3
import tempfile
import sys
from pathlib import Path

from adapters.durable_provenance import (
    FilesystemDurableProvenanceProvider,
    IntegrityError,
    RECORD_PREPARED,
    SQLiteDurableProvenanceProvider,
    STATE_FAILED_INTEGRITY,
    canonical_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MUTATION_SUITE_IDENTITY = "AIR_DURABLE_PROVENANCE_PROVIDER_MUTATION_SUITE_V1"


def record(ref: str, payload: object, identity: str = "obj") -> dict:
    return {
        "provenance_store_id": "mutation-store",
        "ledger_entry_ref": ref,
        "canonical_object_sha256": canonical_sha256(payload),
        "canonical_object_snapshot": payload,
        "record_state": RECORD_PREPARED,
        "source_message_count": 1,
        "source_state_epoch": 1,
        "object_name": "AIR_MUTATION_TEST",
        "object_identity": identity,
        "persistence_provider_class": "MUTATION_TEST",
        "write_readback_state": "PENDING",
    }


def expect_integrity(fn, label: str) -> None:
    try:
        fn()
    except IntegrityError:
        return
    raise AssertionError(f"mutation survived: {label}")


def filesystem_mutations(root: Path) -> list[str]:
    p = FilesystemDurableProvenanceProvider(root)
    ns = p.open_project_namespace("project")
    r = record("AIR_SURFACED_OBJECT_LEDGER_ENTRY::mut::1", {"x": 1})
    p.prepare_snapshot(ns, r)
    p.commit_visible(ns, r["ledger_entry_ref"])
    expect_integrity(lambda: p.mark_orphaned(ns, r["ledger_entry_ref"]), "committed->orphaned")

    _, snapshot = p._record_paths(ns, r["ledger_entry_ref"])
    snapshot.write_bytes(b"{}")
    expect_integrity(lambda: p.read_snapshot(ns, r["ledger_entry_ref"]), "filesystem snapshot corruption")

    p2 = FilesystemDurableProvenanceProvider(root / "second")
    ns2 = p2.open_project_namespace("project")
    r1 = record("AIR_SURFACED_OBJECT_LEDGER_ENTRY::mut2::1", {"x": 1})
    p2.prepare_snapshot(ns2, r1)
    r2 = record(r1["ledger_entry_ref"], {"x": 2})
    expect_integrity(lambda: p2.prepare_snapshot(ns2, r2), "ref reuse different hash")
    return ["committed_orphan_rejected", "snapshot_corruption_detected", "ref_collision_detected"]


def sqlite_mutations(db: Path) -> list[str]:
    p = SQLiteDurableProvenanceProvider(db)
    ns = p.open_project_namespace("project")
    r = record("AIR_SURFACED_OBJECT_LEDGER_ENTRY::sqlmut::1", {"x": 1})
    p.prepare_snapshot(ns, r)
    p.commit_visible(ns, r["ledger_entry_ref"])
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE records SET snapshot=? WHERE namespace_id=? AND ledger_entry_ref=?", (b"{}", ns.namespace_id, r["ledger_entry_ref"]))
    expect_integrity(lambda: p.read_snapshot(ns, r["ledger_entry_ref"]), "sqlite snapshot corruption")
    return ["sqlite_snapshot_corruption_detected"]


def coverage_identity_mutation(root: Path) -> list[str]:
    p = FilesystemDurableProvenanceProvider(root)
    ns = p.open_project_namespace("project")
    r = record("AIR_SURFACED_OBJECT_LEDGER_ENTRY::cov::1", {"x": 1}, "identity-A")
    p.prepare_snapshot(ns, r)
    p.commit_visible(ns, r["ledger_entry_ref"])
    expected = dict(r)
    expected["object_identity"] = "identity-B"
    result = p.verify_coverage(ns, [expected])
    if result.state != STATE_FAILED_INTEGRITY or not result.mismatched_refs:
        raise AssertionError("mutation survived: coverage identity mismatch")
    return ["coverage_identity_mismatch_detected"]


def main() -> int:
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            killed = []
            killed += filesystem_mutations(root / "fs")
            killed += sqlite_mutations(root / "prov.sqlite")
            killed += coverage_identity_mutation(root / "coverage")
        print(json.dumps({"suite": MUTATION_SUITE_IDENTITY, "decision": "PASS", "killed_mutations": killed}, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"suite": MUTATION_SUITE_IDENTITY, "decision": "FAIL", "error": f"{type(exc).__name__}: {exc}"}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
