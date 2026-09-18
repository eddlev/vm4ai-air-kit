#!/usr/bin/env python3
"""Mutation suite for AIR full-surface integrity validator."""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from validate_air_full_surface_integrity import REQUIRED_DIMENSIONS, validate

SUITE_IDENTITY = "AIR_FULL_SURFACE_INTEGRITY_MUTATION_SUITE_V1"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def terminal_dims() -> dict[str, str]:
    return {dim: "PASS" for dim in REQUIRED_DIMENSIONS}


def build_fixture(root: Path) -> tuple[Path, Path]:
    core = root / "prompts/AIR_CORE_RUNTIME.md"
    route = root / "catalog/AIR_RUNTIME_ROUTE_MAP.json"
    executor = root / "profiles/test/AIR_TEST_EXECUTOR.json"
    write(core, "\n".join([
        "AIR-FLOOR-029-MANDATORY-VISIBLE-ALIGNMENT-AND-VALIDATION",
        "AIR-FLOOR-030-NEW-TASK-ARTIFACT-VISIBLE-BEFORE-CONTINUATION",
        "RT.DURABILITY_NEGOTIATE",
        "AIR_FULL_SURFACE_INTEGRITY_AUDIT_V1",
        "AIR_PROJECT_RECOVERY_BOOTSTRAP_NO_HANDOFF",
    ]))
    write(route, json.dumps({"markers": ["AIR-FLOOR-029", "AIR-FLOOR-030", "RT.DURABILITY_NEGOTIATE", "DEP.DURABILITY_NEGOTIATION_RESOLVED"]}))
    write(executor, json.dumps({"status": "VALIDATED_AVAILABLE", "availability_state": "VALIDATED_AVAILABLE_UNBOUND", "role": "EXECUTOR_NON_AGENT_LAYER"}))
    paths = [core, route, executor]
    records = []
    for path in paths:
        records.append({
            "canonical_path": path.relative_to(root).as_posix(),
            "designation_class": "TEST",
            "expected_status": "VALIDATED",
            "semantic_owners": [],
            "owned_concepts": [],
            "referenced_files": [],
            "referring_files": [],
            "audit_dimensions": terminal_dims(),
            "deterministic_check_refs": ["fixture"],
            "behavioral_scenario_refs": ["S01"],
            "mutation_refs": ["M01"],
            "migration_refs": [],
            "release_seal_refs": [],
            "sha256": sha(path),
            "current_result": "PASS",
        })
    manifest = root / "tests/air_full_surface_coverage_manifest.json"
    scenario = root / "tests/air_full_surface_scenario_matrix.json"
    write(manifest, json.dumps({"manifest_identity": "fixture", "files": records}, indent=2))
    scenarios = [{
        "scenario_id": f"S{i:02d}",
        "surface": "fixture",
        "expected_visible_objects": ["AIR_ALIGNMENT_CHECK", "AIR_VALIDATION_REPORT"],
        "expected_artifact_behavior": "CURRENT_ARTIFACT_VISIBLE_WHEN_TASK_BINDS",
        "expected_decision": "PASS",
    } for i in range(1, 21)]
    write(scenario, json.dumps({"scenario_matrix_identity": "fixture", "scenarios": scenarios}, indent=2))
    return manifest, scenario


def must_fail(root: Path, manifest: Path, scenario: Path, label: str) -> None:
    report = validate(root, manifest, scenario)
    if report["decision"] != "FAIL":
        raise AssertionError(f"mutation survived: {label}")


def main() -> int:
    killed = []
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "base"
        manifest, scenario = build_fixture(base)
        if validate(base, manifest, scenario)["decision"] != "PASS":
            raise AssertionError("baseline fixture did not pass")

        import shutil
        root = Path(td) / "m1"; shutil.copytree(base, root); write(root / "prompts/EXTRA.md", "x")
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "unmanifested file"); killed.append("unmanifested_file")

        root = Path(td) / "m2"; shutil.copytree(base, root); write(root / "catalog/AIR_RUNTIME_ROUTE_MAP.json", "{")
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "invalid json"); killed.append("invalid_json")

        root = Path(td) / "m3"; shutil.copytree(base, root)
        core = root / "prompts/AIR_CORE_RUNTIME.md"; core.write_text(core.read_text().replace("AIR-FLOOR-029-MANDATORY-VISIBLE-ALIGNMENT-AND-VALIDATION\n", ""), encoding="utf-8")
        m = json.loads((root / "tests/air_full_surface_coverage_manifest.json").read_text())
        for rec in m["files"]:
            if rec["canonical_path"] == "prompts/AIR_CORE_RUNTIME.md": rec["sha256"] = sha(core)
        write(root / "tests/air_full_surface_coverage_manifest.json", json.dumps(m, indent=2))
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "floor029 removed"); killed.append("floor029_removed")

        root = Path(td) / "m4"; shutil.copytree(base, root); ex = root / "profiles/test/AIR_TEST_EXECUTOR.json"; write(ex, json.dumps({"status": "DRAFT", "availability_state": "AVAILABLE_UNVALIDATED"}))
        m = json.loads((root / "tests/air_full_surface_coverage_manifest.json").read_text())
        for rec in m["files"]:
            if rec["canonical_path"].endswith("AIR_TEST_EXECUTOR.json"): rec["sha256"] = sha(ex)
        write(root / "tests/air_full_surface_coverage_manifest.json", json.dumps(m, indent=2))
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "draft executor"); killed.append("draft_executor")

        root = Path(td) / "m5"; shutil.copytree(base, root); m = json.loads((root / "tests/air_full_surface_coverage_manifest.json").read_text()); m["files"][0]["audit_dimensions"]["AUTHORITY_BOUNDARY"] = "NOT_TESTED"; write(root / "tests/air_full_surface_coverage_manifest.json", json.dumps(m, indent=2))
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "not tested dimension"); killed.append("not_tested_dimension")

        root = Path(td) / "m6"; shutil.copytree(base, root); s = json.loads((root / "tests/air_full_surface_scenario_matrix.json").read_text()); s["scenarios"] = s["scenarios"][:19]; write(root / "tests/air_full_surface_scenario_matrix.json", json.dumps(s, indent=2))
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "scenario count"); killed.append("scenario_count")

        root = Path(td) / "m7"; shutil.copytree(base, root); m = json.loads((root / "tests/air_full_surface_coverage_manifest.json").read_text()); m["files"][0]["referenced_files"] = ["prompts/DOES_NOT_EXIST.md"]; write(root / "tests/air_full_surface_coverage_manifest.json", json.dumps(m, indent=2))
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "dangling reference"); killed.append("dangling_reference")

        root = Path(td) / "m8"; shutil.copytree(base, root); route = root / "catalog/AIR_RUNTIME_ROUTE_MAP.json"; write(route, '{"dup":1,"dup":2}')
        m = json.loads((root / "tests/air_full_surface_coverage_manifest.json").read_text())
        for rec in m["files"]:
            if rec["canonical_path"] == "catalog/AIR_RUNTIME_ROUTE_MAP.json": rec["sha256"] = sha(route)
        write(root / "tests/air_full_surface_coverage_manifest.json", json.dumps(m, indent=2))
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "duplicate json key"); killed.append("duplicate_json_key")

        root = Path(td) / "m9"; shutil.copytree(base, root); (root / "profiles/test/unexpected.bin").parent.mkdir(parents=True, exist_ok=True); (root / "profiles/test/unexpected.bin").write_bytes(b"binary")
        must_fail(root, root / "tests/air_full_surface_coverage_manifest.json", root / "tests/air_full_surface_scenario_matrix.json", "unexpected governed file"); killed.append("unexpected_governed_file")

    print(json.dumps({"suite": SUITE_IDENTITY, "decision": "PASS", "killed_mutations": killed}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
