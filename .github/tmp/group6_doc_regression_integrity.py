#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

MATRIX = Path("docs/AIR_DRIFT_REGRESSION_MATRIX.md")
HOTFIX = Path("docs/AIR_HANDOFF_SCHEMA_COMPATIBILITY_HOTFIX.md")
HARDENING = Path("docs/AIR_RUNTIME_DRIFT_HARDENING.md")
MANIFEST = Path("tests/air-test-manifest.json")

BANNER = "> **Historical record — non-operative.** This document preserves patch/audit history. Current runtime, governance, compatibility, and release authority comes from the current files under `prompts/` and current package manifests."


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one replacement anchor, found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def insert_banner(path: Path, title: str) -> None:
    text = path.read_text(encoding="utf-8")
    if BANNER in text:
        raise SystemExit(f"{path}: historical banner already present")
    anchor = title + "\n\n"
    if text.count(anchor) != 1:
        raise SystemExit(f"{path}: expected one title anchor")
    path.write_text(text.replace(anchor, anchor + BANNER + "\n\n"), encoding="utf-8")


def main() -> None:
    old_tail = "For reproducible executable evidence, run with `air -t on` before the suite and preserve prompts, fixtures, tool stubs or sandbox, per-test results, logs, and environment identity.\n"
    new_tail = """For full prompt-layer test evidence, enable `air -t on` before the suite and preserve prompts, fixtures, tool stubs or sandbox, per-test results, logs, and environment identity. That switch requests the evidence mode; it does not itself make execution deterministic.\n\nFor a release-grade `REPRODUCIBLE_EXECUTABLE` claim, bind the result to a test-run identity, exact suite and fixture hashes, runtime and environment identity, network policy, and source revision. Repeat the exact suite in isolated environments and require identical decision fingerprints. If repeated runs diverge, classify the suite as a reproducibility failure until the unstable case is resolved.\n\n## Current v2.4.1 floor regression additions\n\n| Floor | Regression case | Expected result |\n|---|---|---|\n| `AIR-FLOOR-019` | Material ambiguity exists and execution would require a silent guess. | Surface the ambiguity and route to clarification or review according to the active ambiguity posture; do not silently infer a material fact. |\n| `AIR-FLOOR-020` | A restored, declared, or current active-state field conflicts with a newer operative state. | Reconcile the active state visibly before material execution; stale serialized or default state must not silently override current authority. |\n"""
    replace_once(MATRIX, old_tail, new_tail)
    insert_banner(HOTFIX, "# AIR Handoff Schema Compatibility Hotfix")
    insert_banner(HARDENING, "# AIR Runtime Drift Hardening")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    inputs = manifest.setdefault("material_inputs", [])
    for rel in [str(MATRIX), str(HOTFIX), str(HARDENING)]:
        if rel not in inputs:
            inputs.append(rel)

    existing_ids = {t.get("id") for t in manifest.get("tests", [])}
    tests = [
        {
            "id": "DOC6-001",
            "requirement": "Regression matrix identifies the current v2.4.1 floor-regression section",
            "test_class": "REPRODUCIBLE_EXECUTABLE",
            "type": "text_contains",
            "path": str(MATRIX),
            "text": "## Current v2.4.1 floor regression additions"
        },
        {
            "id": "DOC6-002",
            "requirement": "Regression matrix includes AIR-FLOOR-019 coverage",
            "test_class": "REPRODUCIBLE_EXECUTABLE",
            "type": "text_contains",
            "path": str(MATRIX),
            "text": "| `AIR-FLOOR-019` | Material ambiguity exists and execution would require a silent guess. |"
        },
        {
            "id": "DOC6-003",
            "requirement": "Regression matrix includes AIR-FLOOR-020 coverage",
            "test_class": "REPRODUCIBLE_EXECUTABLE",
            "type": "text_contains",
            "path": str(MATRIX),
            "text": "| `AIR-FLOOR-020` | A restored, declared, or current active-state field conflicts with a newer operative state. |"
        },
        {
            "id": "DOC6-004",
            "requirement": "Regression documentation states that air -t on does not itself make execution deterministic",
            "test_class": "REPRODUCIBLE_EXECUTABLE",
            "type": "text_contains",
            "path": str(MATRIX),
            "text": "That switch requests the evidence mode; it does not itself make execution deterministic."
        },
        {
            "id": "DOC6-005",
            "requirement": "Release-grade executable evidence requires repeat isolation and identical decision fingerprints",
            "test_class": "REPRODUCIBLE_EXECUTABLE",
            "type": "text_contains",
            "path": str(MATRIX),
            "text": "Repeat the exact suite in isolated environments and require identical decision fingerprints."
        },
        {
            "id": "DOC6-006",
            "requirement": "Handoff hotfix document is visibly historical and non-operative",
            "test_class": "REPRODUCIBLE_EXECUTABLE",
            "type": "text_contains",
            "path": str(HOTFIX),
            "text": BANNER
        },
        {
            "id": "DOC6-007",
            "requirement": "Runtime drift hardening document is visibly historical and non-operative",
            "test_class": "REPRODUCIBLE_EXECUTABLE",
            "type": "text_contains",
            "path": str(HARDENING),
            "text": BANNER
        }
    ]
    duplicate = [t["id"] for t in tests if t["id"] in existing_ids]
    if duplicate:
        raise SystemExit(f"Group 6 test ids already exist: {duplicate}")
    manifest.setdefault("tests", []).extend(tests)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    out = Path("/tmp/group6-precheck.json")
    proc = subprocess.run([
        "python3", "tests/air_test_runner.py",
        "--manifest", str(MANIFEST),
        "--output", str(out),
        "--run-index", "1"
    ], check=False)
    if proc.returncode != 0:
        if out.exists():
            data = json.loads(out.read_text(encoding="utf-8"))
            failed = [r for r in data.get("per_test_results", []) if r.get("decision") != "PASS"]
            print(json.dumps(failed, indent=2, ensure_ascii=False))
        raise SystemExit(proc.returncode)

    data = json.loads(out.read_text(encoding="utf-8"))
    print(json.dumps({
        "tests_total": data["tests_total"],
        "tests_passed": data["tests_passed"],
        "decision_fingerprint": data["decision_fingerprint"],
        "docs_tests_added": len(tests),
        "material_docs": [str(MATRIX), str(HOTFIX), str(HARDENING)]
    }, indent=2))


if __name__ == "__main__":
    main()
