#!/usr/bin/env python3
"""Validate AIR_DURABLE_PROVENANCE_PROVIDER_ADAPTER_V1 implementations.

The validator proves only provider contract behavior. It does not grant AIR execution
or Handoff authority and never treats persistence as approval/binding authority.
"""
from __future__ import annotations

import argparse
import json
import tempfile
import sys
from pathlib import Path
from typing import Any, Callable

from adapters.durable_provenance import (
    ADAPTER_IDENTITY,
    FilesystemDurableProvenanceProvider,
    RECORD_COMMITTED_VISIBLE,
    RECORD_PREPARED,
    SQLiteDurableProvenanceProvider,
    STATE_AVAILABLE_VERIFIED,
    STATE_DEGRADED_INCOMPLETE,
    canonical_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

VALIDATOR_IDENTITY = "AIR_DURABLE_PROVENANCE_PROVIDER_VALIDATOR_V1"


def provenance_record(ref: str, sequence: int, payload: Any) -> dict[str, Any]:
    return {
        "provenance_store_id": "validator-store",
        "ledger_entry_ref": ref,
        "canonical_object_sha256": canonical_sha256(payload),
        "canonical_object_snapshot": payload,
        "record_state": RECORD_PREPARED,
        "source_message_count": sequence,
        "source_state_epoch": 7,
        "object_name": "AIR_VALIDATOR_TEST_OBJECT",
        "object_identity": f"validator-object-{sequence}",
        "persistence_provider_class": "VALIDATOR",
        "write_readback_state": "PENDING",
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def exercise_provider(provider: Any, reopen: Callable[[], Any]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    desc = provider.describe_provider()
    require(desc.adapter_identity == ADAPTER_IDENTITY, "adapter identity mismatch")
    require(desc.positive_execution_authority == "NONE", "persistence gained execution authority")
    checks.append({"check": "provider_description", "result": "PASS"})

    probe = provider.probe_write_readback()
    require(probe["state"] == STATE_AVAILABLE_VERIFIED, "write/readback probe did not verify")
    require(probe["write_readback_state"] == "EXACT", "probe readback was not exact")
    checks.append({"check": "probe_write_readback", "result": "PASS"})

    ns = provider.open_project_namespace("AIR validator project A")
    other = provider.open_project_namespace("AIR validator project B")
    require(ns.namespace_id != other.namespace_id, "project namespace isolation failed")
    checks.append({"check": "namespace_isolation", "result": "PASS"})

    r1 = provenance_record("AIR_SURFACED_OBJECT_LEDGER_ENTRY::validator::1", 1, {"b": 2, "a": [1, 2]})
    r2 = provenance_record("AIR_SURFACED_OBJECT_LEDGER_ENTRY::validator::2", 2, {"hello": "world"})
    prepared = provider.prepare_snapshot(ns, r1)
    require(prepared["record_state"] == RECORD_PREPARED, "prepared state not preserved")
    require(prepared["canonical_object_snapshot"] == {"a": [1, 2], "b": 2}, "canonical snapshot mismatch")
    provider.commit_visible(ns, r1["ledger_entry_ref"])
    provider.prepare_snapshot(ns, r2)

    incomplete = provider.verify_coverage(ns, [r1, r2])
    require(incomplete.state == STATE_DEGRADED_INCOMPLETE, "incomplete coverage not detected")
    provider.commit_visible(ns, r2["ledger_entry_ref"])
    complete = provider.verify_coverage(ns, [r1, r2])
    require(complete.state == STATE_AVAILABLE_VERIFIED and complete.complete, "complete coverage not verified")
    checks.append({"check": "prepare_commit_coverage", "result": "PASS"})

    committed = provider.retrieve_committed_range(ns, 1, 2)
    require([item["ledger_entry_ref"] for item in committed] == [r1["ledger_entry_ref"], r2["ledger_entry_ref"]], "committed range ordering mismatch")
    checks.append({"check": "committed_range", "result": "PASS"})

    reopened = reopen()
    desc2 = reopened.describe_provider()
    ns2 = reopened.open_project_namespace("AIR validator project A")
    require(desc.provider_generation == desc2.provider_generation, "provider generation changed across reopen")
    require(desc.provider_instance == desc2.provider_instance, "provider instance changed across reopen")
    stable = reopened.stable_retrieve(ns2, r1["ledger_entry_ref"])
    require(stable["record_state"] == RECORD_COMMITTED_VISIBLE, "stable retrieval lost committed state")
    checks.append({"check": "fresh_process_or_connection_stability", "result": "PASS"})

    orphan = provenance_record("AIR_SURFACED_OBJECT_LEDGER_ENTRY::validator::3", 3, {"orphan": True})
    reopened.prepare_snapshot(ns2, orphan)
    reopened.mark_orphaned(ns2, orphan["ledger_entry_ref"])
    removed = reopened.cleanup_orphans(ns2)
    require(removed >= 1, "orphan cleanup did not remove orphan")
    checks.append({"check": "orphan_lifecycle", "result": "PASS"})
    return checks


def run_validation() -> dict[str, Any]:
    report: dict[str, Any] = {
        "validator_identity": VALIDATOR_IDENTITY,
        "adapter_identity": ADAPTER_IDENTITY,
        "positive_execution_authority": "NONE",
        "providers": {},
        "decision": "PASS",
    }
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fs_root = root / "fs"
        fs = FilesystemDurableProvenanceProvider(fs_root)
        report["providers"]["filesystem"] = exercise_provider(fs, lambda: FilesystemDurableProvenanceProvider(fs_root))

        db = root / "prov.sqlite"
        sql = SQLiteDurableProvenanceProvider(db)
        report["providers"]["sqlite"] = exercise_provider(sql, lambda: SQLiteDurableProvenanceProvider(db))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit machine-readable report")
    args = parser.parse_args()
    try:
        report = run_validation()
    except Exception as exc:
        report = {"validator_identity": VALIDATOR_IDENTITY, "decision": "FAIL", "error": f"{type(exc).__name__}: {exc}"}
        if args.json:
            print(json.dumps(report, sort_keys=True))
        else:
            print(f"FAIL {report['error']}")
        return 1
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        total = sum(len(v) for v in report["providers"].values())
        print(f"PASS {VALIDATOR_IDENTITY}: {total} provider checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
