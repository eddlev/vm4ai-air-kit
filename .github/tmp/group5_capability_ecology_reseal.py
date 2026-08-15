#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path.cwd()
BASE = ROOT / "profiles" / "capability ecology architect"
TEST_MANIFEST = ROOT / "tests" / "air-test-manifest.json"

FILES = {
    "registry": BASE / "AIR_DOMAIN_CAPABILITY_REGISTRY.json",
    "translator": BASE / "AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json",
    "architect": BASE / "AIR_CAPABILITY_ECOLOGY_ARCHITECT.json",
    "method": BASE / "AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json",
    "manifest": BASE / "AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json",
}

COMPONENT_VERSION_OLD = "2.3.2"
COMPONENT_VERSION_NEW = "2.3.3"
PACKAGE_VERSION_OLD = "2.3.3"
PACKAGE_VERSION_NEW = "2.3.4"
FLOORS = [f"AIR-FLOOR-{n:03d}" for n in range(13, 21)]
FOUNDATION_VERSIONS = {
    "core": "2.4.1",
    "control": "2.4.1",
    "governance": "2.2.0",
    "starter": "2.4.1",
    "handoff_schema": "2.2.0",
}

FOUNDATION = [
    ("AIR_CORE_RUNTIME.md", "AIR_CORE_RUNTIME_V2", "2.4.1", "FOUNDATION_PROMPT"),
    ("AIR_CONTROL_SURFACE.md", "AIR_CONTROL_SURFACE_V2", "2.4.1", "FOUNDATION_PROMPT"),
    ("AIR_GOV.md", "AIR_HR_GOVERNANCE_SUPPLEMENT_V2", "2.2.0", "FOUNDATION_PROMPT"),
    ("AIR_DEFAULT_STARTER_PROFILE.json", "AIR_DEFAULT_STARTER_V2", "2.4.1", "TASK_COMPOSITE"),
    ("AIR_HANDOFF_CARD_TEMPLATE.json", "AIR_HANDOFF_CARD_TEMPLATE_V2", "2.2.0", "TEMPLATE"),
]


def strict_json_load(path: Path) -> Any:
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path, version: str | None = None) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    out = {
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size_bytes": len(path.read_bytes()),
        "line_count": len(text.splitlines()),
    }
    if version is not None:
        out["version"] = version
    return out


def validate_foundation_version(path: Path, expected: str) -> None:
    if path.suffix == ".md":
        text = path.read_text(encoding="utf-8")
        if not re.search(rf"PROMPT_VERSION[^\n]*\b{re.escape(expected)}\b", text):
            raise RuntimeError(f"foundation version mismatch for {path}: expected {expected}")
        return
    obj = strict_json_load(path)
    if path.name == "AIR_HANDOFF_CARD_TEMPLATE.json":
        observed = obj.get("AIR_HANDOFF_CARD", {}).get("schema_version")
    else:
        observed = obj.get("PROMPT_VERSION") or obj.get("prompt_version") or obj.get("schema_version")
    if observed != expected:
        raise RuntimeError(f"foundation version mismatch for {path}: expected {expected}, observed {observed}")


def build_foundation_records() -> list[dict[str, Any]]:
    out = []
    for filename, designation, version, cls in FOUNDATION:
        path = ROOT / "prompts" / filename
        validate_foundation_version(path, version)
        ident = identity(path)
        out.append({
            "filename": filename,
            "designation": designation,
            "version": version,
            "class": cls,
            "sha256": ident["sha256"],
            "size_bytes": ident["size_bytes"],
            "line_count": ident["line_count"],
        })
    return out


def assert_version(obj: dict[str, Any], key: str, expected: str, filename: str) -> None:
    observed = obj.get(key)
    if observed != expected:
        raise RuntimeError(f"{filename}: expected {key}={expected}, observed {observed}")


def patch_foundation_contract(obj: dict[str, Any], foundation_records: list[dict[str, Any]]) -> None:
    fc = obj.get("foundation_compatibility")
    if not isinstance(fc, dict):
        raise RuntimeError("missing foundation_compatibility")
    if "required_files" in fc:
        fc["required_files"] = [dict(x) for x in foundation_records]
    if "required_foundation_files" in fc:
        expected_names = [x["filename"] for x in foundation_records]
        if fc["required_foundation_files"] != expected_names:
            raise RuntimeError("required_foundation_files changed shape unexpectedly")
    fc["required_floor_invariants"] = list(FLOORS)


def patch_integration_refresh(obj: dict[str, Any]) -> None:
    ir = obj.get("integration_refresh")
    if not isinstance(ir, dict):
        raise RuntimeError("missing integration_refresh")
    ir["refresh_version"] = PACKAGE_VERSION_NEW
    ml = ir.get("mainline_release_binding")
    if not isinstance(ml, dict):
        raise RuntimeError("missing integration_refresh.mainline_release_binding")
    ml["release_identity"] = "AIR_SPECIALIST_LAYER_INTEGRATED_RELEASE_V2_3_4"
    ml["integration_version"] = PACKAGE_VERSION_NEW
    ml["foundation_versions"] = dict(FOUNDATION_VERSIONS)
    ml["functional_component_change"] = True


def patch_refs(node: Any, sibling_records: dict[str, dict[str, Any]], under_source_baseline: bool = False) -> None:
    if isinstance(node, dict):
        if under_source_baseline:
            return
        name = node.get("filename") or node.get("canonical_filename")
        if name in sibling_records:
            rec = sibling_records[name]
            if "sha256" in node:
                node["sha256"] = rec["sha256"]
            if "observed_sha256" in node:
                node["observed_sha256"] = rec["sha256"]
            if "size_bytes" in node:
                node["size_bytes"] = rec["size_bytes"]
            if "line_count" in node:
                node["line_count"] = rec["line_count"]
            if "version" in node:
                node["version"] = COMPONENT_VERSION_NEW
        for key, value in list(node.items()):
            if key == "source_baseline":
                continue
            patch_refs(value, sibling_records, False)
    elif isinstance(node, list):
        for value in node:
            patch_refs(value, sibling_records, under_source_baseline)


def component_record(path: Path) -> dict[str, Any]:
    ident = identity(path)
    return {
        "sha256": ident["sha256"],
        "size_bytes": ident["size_bytes"],
        "line_count": ident["line_count"],
        "version": COMPONENT_VERSION_NEW,
    }


def patch_component(path: Path, foundation_records: list[dict[str, Any]], sibling_records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    obj = strict_json_load(path)
    assert_version(obj, "package_version", COMPONENT_VERSION_OLD, path.name)
    obj["package_version"] = COMPONENT_VERSION_NEW
    patch_foundation_contract(obj, foundation_records)
    patch_refs(obj, sibling_records)
    patch_integration_refresh(obj)
    write_json(path, obj)
    return component_record(path)


def patch_manifest(path: Path, foundation_records: list[dict[str, Any]], sibling_records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    obj = strict_json_load(path)
    assert_version(obj, "PACKAGE_VERSION", PACKAGE_VERSION_OLD, path.name)
    obj["PACKAGE_VERSION"] = PACKAGE_VERSION_NEW
    obj["status"] = "V2_3_4_OPERATIVE_COMPATIBILITY_AUTHORITY_RESEALED_AVAILABLE_UNBOUND"
    obj["generated_at"] = subprocess.check_output(
        ["git", "show", "-s", "--format=%cI", "origin/main"], text=True
    ).strip()
    patch_foundation_contract(obj, foundation_records)
    patch_integration_refresh(obj)

    components = obj.get("components")
    if not isinstance(components, list) or len(components) != 4:
        raise RuntimeError("manifest component list shape changed")
    for item in components:
        filename = item.get("filename")
        if filename not in sibling_records:
            raise RuntimeError(f"manifest unexpected component: {filename}")
        rec = sibling_records[filename]
        item["version"] = COMPONENT_VERSION_NEW
        item["sha256"] = rec["sha256"]
        item["size_bytes"] = rec["size_bytes"]
        item["line_count"] = rec["line_count"]

    patch_refs(obj, sibling_records)
    write_json(path, obj)
    return identity(path) | {"version": PACKAGE_VERSION_NEW}


def json_path_parts(path: str) -> list[str]:
    return path.split(".") if path else []


def enumerate_ref_tests(
    node: Any,
    sibling_records: dict[str, dict[str, Any]],
    rel_path: str,
    json_path: str = "",
    under_source_baseline: bool = False,
) -> list[dict[str, Any]]:
    tests: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if under_source_baseline:
            return tests
        name = node.get("filename") or node.get("canonical_filename")
        if name in sibling_records:
            rec = sibling_records[name]
            for field in ("sha256", "observed_sha256"):
                if field in node:
                    tests.append({
                        "type": "json_value_equals",
                        "path": rel_path,
                        "json_path": f"{json_path}.{field}" if json_path else field,
                        "expected": rec["sha256"],
                        "requirement": f"{rel_path} must pin current {name} {field}",
                    })
            for field in ("size_bytes", "line_count"):
                if field in node:
                    tests.append({
                        "type": "json_value_equals",
                        "path": rel_path,
                        "json_path": f"{json_path}.{field}" if json_path else field,
                        "expected": rec[field],
                        "requirement": f"{rel_path} must pin current {name} {field}",
                    })
            if "version" in node:
                tests.append({
                    "type": "json_value_equals",
                    "path": rel_path,
                    "json_path": f"{json_path}.version" if json_path else "version",
                    "expected": COMPONENT_VERSION_NEW,
                    "requirement": f"{rel_path} must pin current {name} component version",
                })
        for key, value in node.items():
            if key == "source_baseline":
                continue
            child = f"{json_path}.{key}" if json_path else key
            tests.extend(enumerate_ref_tests(value, sibling_records, rel_path, child, False))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            child = f"{json_path}.{index}" if json_path else str(index)
            tests.extend(enumerate_ref_tests(value, sibling_records, rel_path, child, under_source_baseline))
    return tests


def add_test(test_list: list[dict[str, Any]], test: dict[str, Any], counter: list[int]) -> None:
    counter[0] += 1
    test = dict(test)
    test["id"] = f"CAP5-{counter[0]:03d}"
    test.setdefault("test_class", "REPRODUCIBLE_EXECUTABLE")
    test_list.append(test)


def update_test_manifest(
    foundation_records: list[dict[str, Any]],
    sibling_records: dict[str, dict[str, Any]],
    manifest_record: dict[str, Any],
) -> int:
    suite = strict_json_load(TEST_MANIFEST)
    if suite.get("schema_version") != "1.0.0":
        raise RuntimeError("unexpected test manifest schema")

    rels = [str(path.relative_to(ROOT)) for path in FILES.values()]
    material_inputs = suite.setdefault("material_inputs", [])
    for rel in rels:
        if rel not in material_inputs:
            material_inputs.append(rel)

    tests = [t for t in suite.get("tests", []) if not str(t.get("id", "")).startswith("CAP5-")]
    counter = [0]

    final_records = dict(sibling_records)
    final_records[FILES["manifest"].name] = manifest_record

    for key, path in FILES.items():
        rel = str(path.relative_to(ROOT))
        rec = final_records[path.name]
        add_test(tests, {
            "type": "json_strict_parse",
            "path": rel,
            "requirement": f"{path.name} must parse as strict JSON without duplicate keys",
        }, counter)
        add_test(tests, {
            "type": "sha256_equals",
            "path": rel,
            "expected": rec["sha256"],
            "requirement": f"{path.name} exact bytes must match the Group 5 seal",
        }, counter)

        obj = strict_json_load(path)
        version_key = "PACKAGE_VERSION" if key == "manifest" else "package_version"
        version_expected = PACKAGE_VERSION_NEW if key == "manifest" else COMPONENT_VERSION_NEW
        add_test(tests, {
            "type": "json_value_equals",
            "path": rel,
            "json_path": version_key,
            "expected": version_expected,
            "requirement": f"{path.name} must expose the Group 5 package version",
        }, counter)
        add_test(tests, {
            "type": "json_value_equals",
            "path": rel,
            "json_path": "foundation_compatibility.required_floor_invariants",
            "expected": FLOORS,
            "requirement": f"{path.name} must require AIR floors 013 through 020",
        }, counter)
        add_test(tests, {
            "type": "json_value_equals",
            "path": rel,
            "json_path": "integration_refresh.refresh_version",
            "expected": PACKAGE_VERSION_NEW,
            "requirement": f"{path.name} integration refresh must be 2.3.4",
        }, counter)
        add_test(tests, {
            "type": "json_value_equals",
            "path": rel,
            "json_path": "integration_refresh.mainline_release_binding.foundation_versions",
            "expected": FOUNDATION_VERSIONS,
            "requirement": f"{path.name} must declare current five-file foundation versions",
        }, counter)
        add_test(tests, {
            "type": "json_value_equals",
            "path": rel,
            "json_path": "integration_refresh.mainline_release_binding.functional_component_change",
            "expected": True,
            "requirement": f"{path.name} must record the operative compatibility refresh as a component change",
        }, counter)

        fc = obj.get("foundation_compatibility", {})
        if "required_files" in fc:
            add_test(tests, {
                "type": "json_value_equals",
                "path": rel,
                "json_path": "foundation_compatibility.required_files",
                "expected": foundation_records,
                "requirement": f"{path.name} exact foundation identities must match current main",
            }, counter)

        for ref_test in enumerate_ref_tests(obj, sibling_records, rel):
            add_test(tests, ref_test, counter)

    manifest_rel = str(FILES["manifest"].relative_to(ROOT))
    add_test(tests, {
        "type": "json_value_equals",
        "path": manifest_rel,
        "json_path": "status",
        "expected": "V2_3_4_OPERATIVE_COMPATIBILITY_AUTHORITY_RESEALED_AVAILABLE_UNBOUND",
        "requirement": "Capability Ecology manifest status must match package version 2.3.4",
    }, counter)

    # Explicitly guard the dependency that the superseded bulk repair failed to refresh.
    translator_rel = str(FILES["translator"].relative_to(ROOT))
    add_test(tests, {
        "type": "json_value_equals",
        "path": translator_rel,
        "json_path": "external_dependency_state.domain_capability_registry.observed_sha256",
        "expected": sibling_records[FILES["registry"].name]["sha256"],
        "requirement": "Translator must pin the exact resealed Domain Capability Registry hash",
    }, counter)

    suite["tests"] = tests
    write_json(TEST_MANIFEST, suite)
    return counter[0]


def main() -> None:
    foundation_records = build_foundation_records()

    # Dependency order: Registry -> Translator -> Architect -> Method -> Manifest.
    sibling_records: dict[str, dict[str, Any]] = {}

    registry_rec = patch_component(FILES["registry"], foundation_records, sibling_records)
    sibling_records[FILES["registry"].name] = registry_rec

    translator_rec = patch_component(FILES["translator"], foundation_records, sibling_records)
    sibling_records[FILES["translator"].name] = translator_rec

    architect_rec = patch_component(FILES["architect"], foundation_records, sibling_records)
    sibling_records[FILES["architect"].name] = architect_rec

    method_rec = patch_component(FILES["method"], foundation_records, sibling_records)
    sibling_records[FILES["method"].name] = method_rec

    manifest_rec = patch_manifest(FILES["manifest"], foundation_records, sibling_records)

    tests_added = update_test_manifest(foundation_records, sibling_records, manifest_rec)

    # Recompute manifest identity after test manifest changes only for reporting; package bytes are unchanged.
    precheck = Path("/tmp/group5-precheck.json")
    proc = subprocess.run([
        "python3", "tests/air_test_runner.py",
        "--manifest", "tests/air-test-manifest.json",
        "--output", str(precheck),
        "--run-index", "1",
    ], check=False)
    if proc.returncode != 0:
        data = strict_json_load(precheck) if precheck.exists() else {}
        failed = [r for r in data.get("per_test_results", []) if r.get("decision") != "PASS"]
        print(json.dumps(failed, indent=2, ensure_ascii=False))
        raise SystemExit(proc.returncode)

    print(json.dumps({
        "foundation": foundation_records,
        "components": sibling_records,
        "manifest": manifest_rec,
        "capability_tests_added": tests_added,
        "translator_registry_pin": sibling_records[FILES["registry"].name]["sha256"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
