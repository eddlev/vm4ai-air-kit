#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path.cwd()
GOV_DIR = ROOT / "profiles" / "governance specialist"
TEST_MANIFEST = ROOT / "tests" / "air-test-manifest.json"

COMPONENT_ORDER = [
    "AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json",
    "AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json",
    "AIR_AI_GOVERNANCE_SPECIALIST.json",
    "AIR_AI_GOVERNANCE_METHOD_PACK.json",
    "AIR_AI_GOVERNANCE_EXECUTOR.json",
]
MANIFEST_FILE = "AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json"
ALL_PACKAGE_FILES = COMPONENT_ORDER + [MANIFEST_FILE]

DESIGNATIONS = {
    "AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json": "AIR_AI_GOVERNANCE_DOMAIN_PACKAGE_V2",
    "AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json": "AIR_AI_GOVERNANCE_AGENTIC_OVERLAY_V2",
    "AIR_AI_GOVERNANCE_SPECIALIST.json": "AIR_AI_GOVERNANCE_SPECIALIST_V2",
    "AIR_AI_GOVERNANCE_METHOD_PACK.json": "AIR_AI_GOVERNANCE_METHOD_PACK_V2",
    "AIR_AI_GOVERNANCE_EXECUTOR.json": "AIR_AI_GOVERNANCE_EXECUTOR_V2",
    "AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json": "AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST_V2",
}

FOUNDATION = [
    ("AIR_CORE_RUNTIME.md", "AIR_CORE_RUNTIME_V2", "2.4.1", "FOUNDATION_PROMPT"),
    ("AIR_CONTROL_SURFACE.md", "AIR_CONTROL_SURFACE_V2", "2.4.1", "FOUNDATION_PROMPT"),
    ("AIR_GOV.md", "AIR_HR_GOVERNANCE_SUPPLEMENT_V2", "2.2.0", "FOUNDATION_PROMPT"),
    ("AIR_DEFAULT_STARTER_PROFILE.json", "AIR_DEFAULT_STARTER_V2", "2.4.1", "TASK_COMPOSITE"),
    ("AIR_HANDOFF_CARD_TEMPLATE.json", "AIR_HANDOFF_CARD_TEMPLATE_V2", "2.2.0", "TEMPLATE"),
]
REQUIRED_FLOORS = [f"AIR-FLOOR-{n:03d}" for n in range(13, 21)]
COMPONENT_VERSION = "2.3.3"
INTEGRATION_VERSION = "2.3.4"
MANIFEST_VERSION = "2.3.4"


def load_json(path: Path) -> Any:
    def no_dupes(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate JSON key in {path}: {key}")
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_dupes)


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path, version: str | None = None, designation: str | None = None) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    result = {
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size_bytes": len(path.read_bytes()),
        "line_count": len(text.splitlines()),
    }
    if version is not None:
        result["version"] = version
    if designation is not None:
        result["designation"] = designation
    return result


def validate_foundation_version(path: Path, expected: str) -> None:
    if path.suffix == ".md":
        match = re.search(r"(?m)^PROMPT_VERSION:\s*([^\s]+)\s*$", path.read_text(encoding="utf-8"))
        if not match or match.group(1) != expected:
            raise RuntimeError(f"foundation version mismatch for {path}: expected {expected}")
        return
    obj = load_json(path)
    observed = obj.get("PROMPT_VERSION")
    if path.name == "AIR_HANDOFF_CARD_TEMPLATE.json":
        observed = obj.get("schema_version")
    if observed != expected:
        raise RuntimeError(f"foundation version mismatch for {path}: expected {expected}, observed {observed}")


def build_foundation_records() -> list[dict[str, Any]]:
    records = []
    for filename, designation, version, klass in FOUNDATION:
        path = ROOT / "prompts" / filename
        validate_foundation_version(path, version)
        ident = identity(path)
        records.append({
            "filename": filename,
            "designation": designation,
            "version": version,
            "class": klass,
            "sha256": ident["sha256"],
            "size_bytes": ident["size_bytes"],
            "line_count": ident["line_count"],
        })
    return records


def patch_foundation(obj: dict[str, Any], records: list[dict[str, Any]]) -> None:
    block = obj.get("foundation_compatibility")
    if not isinstance(block, dict):
        raise RuntimeError(f"missing foundation_compatibility in {obj.get('SYSTEM_DESIGNATION') or obj.get('PACKAGE_DESIGNATION')}")
    block["required_files"] = records
    block["required_floor_invariants"] = REQUIRED_FLOORS
    block["compatibility_state"] = "VALIDATED_AGAINST_CURRENT_AIR_V2_FOUNDATION_EXACT_IDENTITIES"


def patch_refreshes(value: Any, *, under_source: bool = False) -> None:
    if isinstance(value, dict):
        if under_source:
            return
        if "refresh_version" in value:
            value["refresh_version"] = INTEGRATION_VERSION
        if "mainline_release_binding" in value and isinstance(value["mainline_release_binding"], dict):
            binding = value["mainline_release_binding"]
            binding["release_identity"] = "AIR_SPECIALIST_LAYER_INTEGRATED_RELEASE_V2_3_4"
            binding["integration_version"] = INTEGRATION_VERSION
            binding["foundation_versions"] = {
                "core": "2.4.1",
                "control": "2.4.1",
                "governance": "2.2.0",
                "starter": "2.4.1",
                "handoff_schema": "2.2.0",
            }
            if "functional_component_change" in binding:
                binding["functional_component_change"] = True
        for key, child in list(value.items()):
            patch_refreshes(child, under_source=(key == "source_baseline"))
    elif isinstance(value, list):
        for child in value:
            patch_refreshes(child, under_source=under_source)


def referenced_component(value: dict[str, Any]) -> str | None:
    for key in ("filename", "canonical_filename", "dependency_filename", "required_filename"):
        candidate = value.get(key)
        if candidate in ALL_PACKAGE_FILES:
            return candidate
    for key in ("designation", "SYSTEM_DESIGNATION", "dependency_designation", "required_designation"):
        candidate = value.get(key)
        for filename, designation in DESIGNATIONS.items():
            if candidate == designation:
                return filename
    return None


def patch_component_refs(value: Any, identities: dict[str, dict[str, Any]], *, under_source: bool = False) -> None:
    if isinstance(value, dict):
        if under_source:
            return
        target = referenced_component(value)
        if target and target in identities and any(k in value for k in ("sha256", "size_bytes", "line_count")):
            ident = identities[target]
            if "sha256" in value:
                value["sha256"] = ident["sha256"]
            if "size_bytes" in value:
                value["size_bytes"] = ident["size_bytes"]
            if "line_count" in value:
                value["line_count"] = ident["line_count"]
            if "version" in value and target != MANIFEST_FILE:
                value["version"] = COMPONENT_VERSION
        for key, child in list(value.items()):
            patch_component_refs(child, identities, under_source=(key == "source_baseline"))
    elif isinstance(value, list):
        for child in value:
            patch_component_refs(child, identities, under_source=under_source)


def replace_method_legacy_grades(value: Any, *, under_source: bool = False) -> None:
    if isinstance(value, dict):
        if under_source:
            return
        for key, child in list(value.items()):
            if isinstance(child, str):
                if child == "AGENT_REPORTED":
                    value[key] = "PROMPT_LAYER_DECLARED"
                elif child == "AGENT_REPORTED_WITH_SOURCE_TRACE":
                    value[key] = "PROMPT_LAYER_DECLARED_WITH_SOURCE_TRACE"
            else:
                replace_method_legacy_grades(child, under_source=(key == "source_baseline"))
    elif isinstance(value, list):
        for child in value:
            replace_method_legacy_grades(child, under_source=under_source)


def add_method_semantics(obj: dict[str, Any]) -> None:
    obj["verification_grade_semantics"] = {
        "field_scope": "METHOD_LOCAL_WORKFLOW_GRADE",
        "current_prompt_layer_values": [
            "PROMPT_LAYER_DECLARED",
            "PROMPT_LAYER_DECLARED_WITH_SOURCE_TRACE",
        ],
        "legacy_aliases_retired": [
            "AGENT_REPORTED",
            "AGENT_REPORTED_WITH_SOURCE_TRACE",
        ],
        "canonical_record_mapping": {
            "PROMPT_LAYER_DECLARED": "SURFACED_OUTPUT_GOVERNANCE_RECORD",
            "PROMPT_LAYER_DECLARED_WITH_SOURCE_TRACE": "SOURCE_SUPPORTED_GOVERNANCE_RECORD",
        },
        "interpretation_boundary": "Method-local prompt-layer grades describe surfaced declared output and, where stated, visible source support. They are not TOOL_OBSERVED_GOVERNANCE_RECORD, BACKEND_ENFORCED_GOVERNANCE_RECORD, hidden reasoning, independent verification, or deterministic execution evidence unless separately supported by the corresponding Core-owned evidence class.",
    }


def find_unresolved_hashed_refs(value: Any, identities: dict[str, dict[str, Any]], *, under_source: bool = False, path: str = "") -> list[str]:
    problems: list[str] = []
    if isinstance(value, dict):
        if under_source:
            return problems
        target = referenced_component(value)
        if target and any(k in value for k in ("sha256", "size_bytes", "line_count")) and target not in identities:
            problems.append(f"{path or '<root>'}: hashed reference to unresolved future component {target}")
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            problems.extend(find_unresolved_hashed_refs(child, identities, under_source=(key == "source_baseline"), path=child_path))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            child_path = f"{path}.{idx}" if path else str(idx)
            problems.extend(find_unresolved_hashed_refs(child, identities, under_source=under_source, path=child_path))
    return problems


def collect_identity_test_paths(value: Any, identities: dict[str, dict[str, Any]], *, under_source: bool = False, path: str = "") -> list[tuple[str, str, Any]]:
    found: list[tuple[str, str, Any]] = []
    if isinstance(value, dict):
        if under_source:
            return found
        target = referenced_component(value)
        if target in identities:
            ident = identities[target]
            for field in ("sha256", "size_bytes", "line_count"):
                if field in value:
                    field_path = f"{path}.{field}" if path else field
                    found.append((field_path, field, ident[field]))
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            found.extend(collect_identity_test_paths(child, identities, under_source=(key == "source_baseline"), path=child_path))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            child_path = f"{path}.{idx}" if path else str(idx)
            found.extend(collect_identity_test_paths(child, identities, under_source=under_source, path=child_path))
    return found


def make_test(test_id: str, path: str, kind: str, requirement: str, **kwargs: Any) -> dict[str, Any]:
    out = {
        "id": test_id,
        "requirement": requirement,
        "test_class": "REPRODUCIBLE_EXECUTABLE",
        "type": kind,
        "path": path,
    }
    out.update(kwargs)
    return out


def main() -> None:
    foundation_records = build_foundation_records()
    identities: dict[str, dict[str, Any]] = {}
    component_objs: dict[str, dict[str, Any]] = {}

    for filename in COMPONENT_ORDER:
        path = GOV_DIR / filename
        obj = load_json(path)
        observed = obj.get("package_version")
        if observed not in {"2.3.2", COMPONENT_VERSION}:
            raise RuntimeError(f"unexpected package_version for {filename}: {observed}")
        obj["package_version"] = COMPONENT_VERSION
        patch_foundation(obj, foundation_records)
        patch_refreshes(obj)
        patch_component_refs(obj, identities)

        if filename == "AIR_AI_GOVERNANCE_METHOD_PACK.json":
            replace_method_legacy_grades(obj)
            add_method_semantics(obj)

        unresolved = find_unresolved_hashed_refs(obj, identities)
        if unresolved:
            raise RuntimeError("; ".join(unresolved))

        write_json(path, obj)
        ident = identity(path, version=COMPONENT_VERSION, designation=DESIGNATIONS[filename])
        identities[filename] = ident
        component_objs[filename] = obj

    manifest_path = GOV_DIR / MANIFEST_FILE
    manifest = load_json(manifest_path)
    observed_manifest_version = manifest.get("PACKAGE_VERSION")
    if observed_manifest_version not in {"2.3.3", MANIFEST_VERSION}:
        raise RuntimeError(f"unexpected governance manifest version: {observed_manifest_version}")
    manifest["PACKAGE_VERSION"] = MANIFEST_VERSION
    if isinstance(manifest.get("status"), str):
        manifest["status"] = manifest["status"].replace("V2_3_3_", "V2_3_4_")
    patch_foundation(manifest, foundation_records)
    patch_refreshes(manifest)
    patch_component_refs(manifest, identities)
    if "generated_at" in manifest:
        manifest["generated_at"] = subprocess.check_output(["git", "show", "-s", "--format=%cI", "HEAD"], text=True).strip()
    write_json(manifest_path, manifest)
    identities[MANIFEST_FILE] = identity(manifest_path, version=MANIFEST_VERSION, designation=DESIGNATIONS[MANIFEST_FILE])

    test_manifest = load_json(TEST_MANIFEST)
    material_inputs = set(test_manifest.get("material_inputs", []))
    for filename in ALL_PACKAGE_FILES:
        material_inputs.add(f"profiles/governance specialist/{filename}")
    test_manifest["material_inputs"] = sorted(material_inputs)
    tests = [t for t in test_manifest.get("tests", []) if not str(t.get("id", "")).startswith("GOV4-")]

    for idx, filename in enumerate(ALL_PACKAGE_FILES, start=1):
        rel = f"profiles/governance specialist/{filename}"
        tests.append(make_test(f"GOV4-{idx:02d}-PARSE", rel, "json_strict_parse", f"{filename} must parse as strict JSON"))
        tests.append(make_test(f"GOV4-{idx:02d}-SHA", rel, "sha256_equals", f"{filename} exact bytes must match the resealed identity", expected=identities[filename]["sha256"]))

    for file_index, filename in enumerate(ALL_PACKAGE_FILES, start=1):
        rel = f"profiles/governance specialist/{filename}"
        obj = load_json(GOV_DIR / filename)
        version_path = "PACKAGE_VERSION" if filename == MANIFEST_FILE else "package_version"
        version_expected = MANIFEST_VERSION if filename == MANIFEST_FILE else COMPONENT_VERSION
        tests.append(make_test(f"GOV4-V{file_index:02d}", rel, "json_value_equals", f"{filename} must carry the Group 4 package version", json_path=version_path, expected=version_expected))

        for foundation_index, record in enumerate(foundation_records):
            prefix = f"foundation_compatibility.required_files.{foundation_index}"
            tests.append(make_test(
                f"GOV4-F{file_index:02d}-{foundation_index:02d}-VER",
                rel,
                "json_value_equals",
                f"{filename} must pin current {record['filename']} version",
                json_path=f"{prefix}.version",
                expected=record["version"],
            ))
            tests.append(make_test(
                f"GOV4-F{file_index:02d}-{foundation_index:02d}-SHA",
                rel,
                "json_value_equals",
                f"{filename} must pin exact current {record['filename']} SHA-256",
                json_path=f"{prefix}.sha256",
                expected=record["sha256"],
            ))

        for floor_index, floor in enumerate(REQUIRED_FLOORS):
            tests.append(make_test(
                f"GOV4-R{file_index:02d}-{floor_index:02d}",
                rel,
                "json_value_equals",
                f"{filename} must include current required governance floor {floor}",
                json_path=f"foundation_compatibility.required_floor_invariants.{floor_index}",
                expected=floor,
            ))

        for ref_index, (json_path, field, expected) in enumerate(collect_identity_test_paths(obj, identities), start=1):
            tests.append(make_test(
                f"GOV4-I{file_index:02d}-{ref_index:03d}",
                rel,
                "json_value_equals",
                f"{filename} sibling/component identity field {json_path} must match resealed bytes",
                json_path=json_path,
                expected=expected,
            ))

    method_rel = "profiles/governance specialist/AIR_AI_GOVERNANCE_METHOD_PACK.json"
    tests.extend([
        make_test("GOV4-SEM-01", method_rel, "text_not_contains", "Legacy AGENT_REPORTED verification vocabulary must be retired from operative Method bytes", text="AGENT_REPORTED"),
        make_test("GOV4-SEM-02", method_rel, "text_contains", "Method must use explicit prompt-layer declared grade", text="PROMPT_LAYER_DECLARED"),
        make_test("GOV4-SEM-03", method_rel, "text_contains", "Method must use prompt-layer declared with source trace where applicable", text="PROMPT_LAYER_DECLARED_WITH_SOURCE_TRACE"),
        make_test("GOV4-SEM-04", method_rel, "json_value_equals", "Method verification grades must be explicitly scoped as method-local", json_path="verification_grade_semantics.field_scope", expected="METHOD_LOCAL_WORKFLOW_GRADE"),
        make_test("GOV4-SEM-05", method_rel, "json_value_equals", "Prompt-layer declared must map to surfaced-output governance record", json_path="verification_grade_semantics.canonical_record_mapping.PROMPT_LAYER_DECLARED", expected="SURFACED_OUTPUT_GOVERNANCE_RECORD"),
        make_test("GOV4-SEM-06", method_rel, "json_value_equals", "Prompt-layer declared with source trace must map to source-supported governance record", json_path="verification_grade_semantics.canonical_record_mapping.PROMPT_LAYER_DECLARED_WITH_SOURCE_TRACE", expected="SOURCE_SUPPORTED_GOVERNANCE_RECORD"),
    ])

    test_manifest["tests"] = tests
    write_json(TEST_MANIFEST, test_manifest)

    env = os.environ.copy()
    env.update({
        "TZ": "UTC",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONHASHSEED": "0",
        "AIR_TEST_SEED": "0",
        "AIR_NETWORK_POLICY": "PRECHECK_NOT_ISOLATED",
        "AIR_SOURCE_COMMIT": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    })
    subprocess.run([
        "python3", "tests/air_test_runner.py",
        "--manifest", "tests/air-test-manifest.json",
        "--output", "/tmp/group4-precheck.json",
        "--run-index", "1",
    ], cwd=ROOT, env=env, check=True)

    summary = {
        "foundation": foundation_records,
        "components": {name: {k: identities[name][k] for k in ("sha256", "size_bytes", "line_count")} for name in COMPONENT_ORDER},
        "manifest": {k: identities[MANIFEST_FILE][k] for k in ("sha256", "size_bytes", "line_count")},
        "governance_tests_added": len([t for t in tests if str(t.get("id", "")).startswith("GOV4-")]),
        "semantic_change": {
            "retired": ["AGENT_REPORTED", "AGENT_REPORTED_WITH_SOURCE_TRACE"],
            "current": ["PROMPT_LAYER_DECLARED", "PROMPT_LAYER_DECLARED_WITH_SOURCE_TRACE"],
        },
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
