#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GROUND_DIR = ROOT / "profiles" / "grounding specialist"
TEST_MANIFEST = ROOT / "tests" / "air-test-manifest.json"

COMPONENTS = [
    ("AIR_GROUNDING_DOMAIN_PACKAGE.json", "AIR_GROUNDING_DOMAIN_PACKAGE_V2"),
    ("AIR_GROUNDING_METHOD_PACK.json", "AIR_GROUNDING_METHOD_PACK_V2"),
    ("AIR_GROUNDING_SPECIALIST.json", "AIR_GROUNDING_SPECIALIST_V2"),
    ("AIR_GROUNDING_EXECUTOR.json", "AIR_GROUNDING_EXECUTOR_V2"),
]
MANIFEST_NAME = "AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json"
CURRENT_COMPONENT_VERSION = "2.3.2"
TARGET_COMPONENT_VERSION = "2.3.3"
CURRENT_MANIFEST_VERSION = "2.3.3"
TARGET_MANIFEST_VERSION = "2.3.4"
CURRENT_REFRESH_VERSION = "2.3.3"
TARGET_REFRESH_VERSION = "2.3.4"
FLOORS = [f"AIR-FLOOR-{n:03d}" for n in range(13, 21)]
FOUNDATION_VERSION_MAP = {
    "core": "2.4.1",
    "control": "2.4.1",
    "governance": "2.2.0",
    "starter": "2.4.1",
    "handoff_schema": "2.2.0",
}


def strict_load(path: Path) -> Any:
    def no_dupes(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise ValueError(f"duplicate JSON key {k!r} in {path}")
            out[k] = v
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_dupes)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def identity(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "line_count": len(data.decode("utf-8").splitlines()),
    }


def markdown_identity(filename: str, path: Path, class_name: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    designation = re.search(r"^SYSTEM_DESIGNATION:\s*(\S+)\s*$", text, re.MULTILINE)
    version = re.search(r"^PROMPT_VERSION:\s*(\S+)\s*$", text, re.MULTILINE)
    if not designation or not version:
        raise ValueError(f"missing designation/version in {path}")
    return {
        "filename": filename,
        "designation": designation.group(1),
        "version": version.group(1),
        "class": class_name,
        **identity(path),
    }


def foundation_records() -> list[dict[str, Any]]:
    records = [
        markdown_identity("AIR_CORE_RUNTIME.md", ROOT / "prompts" / "AIR_CORE_RUNTIME.md", "FOUNDATION_PROMPT"),
        markdown_identity("AIR_CONTROL_SURFACE.md", ROOT / "prompts" / "AIR_CONTROL_SURFACE.md", "FOUNDATION_PROMPT"),
        markdown_identity("AIR_GOV.md", ROOT / "prompts" / "AIR_GOV.md", "FOUNDATION_PROMPT"),
    ]
    starter_path = ROOT / "prompts" / "AIR_DEFAULT_STARTER_PROFILE.json"
    starter = strict_load(starter_path)
    records.append({
        "filename": "AIR_DEFAULT_STARTER_PROFILE.json",
        "designation": starter["SYSTEM_DESIGNATION"],
        "version": starter["PROMPT_VERSION"],
        "class": "TASK_COMPOSITE",
        **identity(starter_path),
    })
    handoff_path = ROOT / "prompts" / "AIR_HANDOFF_CARD_TEMPLATE.json"
    handoff = strict_load(handoff_path)["AIR_HANDOFF_CARD"]
    records.append({
        "filename": "AIR_HANDOFF_CARD_TEMPLATE.json",
        "designation": handoff["template_designation"],
        "version": handoff["schema_version"],
        "class": "TEMPLATE",
        **identity(handoff_path),
    })
    observed = {
        "core": records[0]["version"],
        "control": records[1]["version"],
        "governance": records[2]["version"],
        "starter": records[3]["version"],
        "handoff_schema": records[4]["version"],
    }
    if observed != FOUNDATION_VERSION_MAP:
        raise ValueError(f"unexpected current foundation versions: {observed}")
    return records


def patch_foundation(obj: dict[str, Any], foundations: list[dict[str, Any]]) -> None:
    fc = obj["foundation_compatibility"]
    current_names = [r["filename"] for r in fc["required_files"]]
    expected_names = [r["filename"] for r in foundations]
    if current_names != expected_names:
        raise ValueError(f"unexpected foundation file order: {current_names}")
    fc["required_files"] = [dict(r) for r in foundations]
    existing_floors = fc["required_floor_invariants"]
    if existing_floors[:6] != FLOORS[:6]:
        raise ValueError(f"unexpected existing floor prefix: {existing_floors}")
    fc["required_floor_invariants"] = list(FLOORS)


def patch_integration_refresh(obj: dict[str, Any]) -> None:
    refresh = obj["integration_refresh"]
    if refresh.get("refresh_version") != CURRENT_REFRESH_VERSION:
        raise ValueError(f"unexpected refresh version in {obj.get('SYSTEM_DESIGNATION')}: {refresh.get('refresh_version')}")
    refresh["refresh_version"] = TARGET_REFRESH_VERSION
    binding = refresh["mainline_release_binding"]
    binding["release_identity"] = "AIR_SPECIALIST_LAYER_INTEGRATED_RELEASE_V2_3_4"
    binding["integration_version"] = TARGET_REFRESH_VERSION
    binding["foundation_versions"] = dict(FOUNDATION_VERSION_MAP)
    binding["functional_component_change"] = True


def update_identity_refs(node: Any, identities: dict[str, dict[str, Any]]) -> None:
    if isinstance(node, dict):
        filename = node.get("filename")
        if filename in identities and all(k in node for k in ("sha256", "size_bytes", "line_count")):
            node.update(identities[filename])
        for value in node.values():
            update_identity_refs(value, identities)
    elif isinstance(node, list):
        for value in node:
            update_identity_refs(value, identities)


def dotted_paths_for_identity_refs(node: Any, known_filenames: set[str], prefix: str = "") -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = []
    if isinstance(node, dict):
        filename = node.get("filename")
        if filename in known_filenames and all(k in node for k in ("sha256", "size_bytes", "line_count")):
            found.append((prefix, node))
        for key, value in node.items():
            child = f"{prefix}.{key}" if prefix else key
            found.extend(dotted_paths_for_identity_refs(value, known_filenames, child))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            child = f"{prefix}.{i}" if prefix else str(i)
            found.extend(dotted_paths_for_identity_refs(value, known_filenames, child))
    return found


def append_test(tests: list[dict[str, Any]], counter: list[int], **payload: Any) -> None:
    counter[0] += 1
    tests.append({"id": f"AIR-GROUND-{counter[0]:03d}", **payload})


def main() -> None:
    foundations = foundation_records()
    component_identities: dict[str, dict[str, Any]] = {}
    component_objects: dict[str, dict[str, Any]] = {}

    for filename, designation in COMPONENTS:
        path = GROUND_DIR / filename
        obj = strict_load(path)
        if obj.get("SYSTEM_DESIGNATION") != designation:
            raise ValueError(f"designation mismatch in {filename}")
        if obj.get("package_version") != CURRENT_COMPONENT_VERSION:
            raise ValueError(f"unexpected package_version in {filename}: {obj.get('package_version')}")
        obj["package_version"] = TARGET_COMPONENT_VERSION
        patch_foundation(obj, foundations)
        patch_integration_refresh(obj)
        update_identity_refs(obj, component_identities)
        write_json(path, obj)
        component_identities[filename] = identity(path)
        component_objects[filename] = strict_load(path)

    manifest_path = GROUND_DIR / MANIFEST_NAME
    manifest = strict_load(manifest_path)
    if manifest.get("PACKAGE_VERSION") != CURRENT_MANIFEST_VERSION:
        raise ValueError(f"unexpected Grounding manifest version: {manifest.get('PACKAGE_VERSION')}")
    manifest["PACKAGE_VERSION"] = TARGET_MANIFEST_VERSION
    manifest["status"] = "V2_3_4_OPERATIVE_COMPATIBILITY_AUTHORITY_RESEALED_AVAILABLE_UNBOUND"
    manifest["generated_at"] = subprocess.check_output(
        ["git", "show", "-s", "--format=%cI", "HEAD"], cwd=ROOT, text=True
    ).strip()
    patch_foundation(manifest, foundations)
    by_filename = {entry["filename"]: entry for entry in manifest["components"]}
    if set(by_filename) != set(component_identities):
        raise ValueError(f"unexpected Grounding manifest component set: {sorted(by_filename)}")
    for filename, ident in component_identities.items():
        entry = by_filename[filename]
        entry["version"] = TARGET_COMPONENT_VERSION
        entry.update(ident)
    write_json(manifest_path, manifest)
    manifest_identity = identity(manifest_path)
    manifest = strict_load(manifest_path)

    test_manifest = strict_load(TEST_MANIFEST)
    ground_relpaths = [f"profiles/grounding specialist/{name}" for name, _ in COMPONENTS] + [
        f"profiles/grounding specialist/{MANIFEST_NAME}"
    ]
    for rel in ground_relpaths:
        if rel not in test_manifest["material_inputs"]:
            test_manifest["material_inputs"].append(rel)

    tests = [t for t in test_manifest["tests"] if not str(t.get("id", "")).startswith("AIR-GROUND-")]
    counter = [0]

    all_ground_identities = dict(component_identities)
    all_ground_identities[MANIFEST_NAME] = manifest_identity
    for filename, _designation in COMPONENTS:
        rel = f"profiles/grounding specialist/{filename}"
        append_test(tests, counter, type="json_strict_parse", path=rel,
                    requirement=f"{filename} remains strict JSON without duplicate keys.")
        append_test(tests, counter, type="sha256_equals", path=rel,
                    expected=component_identities[filename]["sha256"],
                    requirement=f"{filename} bytes match the resealed identity.")
        append_test(tests, counter, type="json_value_equals", path=rel, json_path="package_version",
                    expected=TARGET_COMPONENT_VERSION,
                    requirement=f"{filename} carries Grounding component version {TARGET_COMPONENT_VERSION}.")
        append_test(tests, counter, type="json_value_equals", path=rel,
                    json_path="foundation_compatibility.required_files", expected=foundations,
                    requirement=f"{filename} is sealed to the exact current five-file AIR foundation.")
        append_test(tests, counter, type="json_value_equals", path=rel,
                    json_path="foundation_compatibility.required_floor_invariants", expected=FLOORS,
                    requirement=f"{filename} requires AIR-FLOOR-013 through AIR-FLOOR-020.")
        append_test(tests, counter, type="json_value_equals", path=rel,
                    json_path="integration_refresh.refresh_version", expected=TARGET_REFRESH_VERSION,
                    requirement=f"{filename} carries the Grounding integration refresh version {TARGET_REFRESH_VERSION}.")
        append_test(tests, counter, type="json_value_equals", path=rel,
                    json_path="integration_refresh.mainline_release_binding.foundation_versions",
                    expected=FOUNDATION_VERSION_MAP,
                    requirement=f"{filename} mainline binding names the current AIR foundation versions.")
        append_test(tests, counter, type="json_value_equals", path=rel,
                    json_path="integration_refresh.mainline_release_binding.functional_component_change",
                    expected=True,
                    requirement=f"{filename} records the new floor/foundation compatibility as a functional compatibility change.")

    manifest_rel = f"profiles/grounding specialist/{MANIFEST_NAME}"
    append_test(tests, counter, type="json_strict_parse", path=manifest_rel,
                requirement="Grounding package manifest remains strict JSON without duplicate keys.")
    append_test(tests, counter, type="sha256_equals", path=manifest_rel, expected=manifest_identity["sha256"],
                requirement="Grounding package manifest bytes match the regenerated identity.")
    append_test(tests, counter, type="json_value_equals", path=manifest_rel, json_path="PACKAGE_VERSION",
                expected=TARGET_MANIFEST_VERSION,
                requirement=f"Grounding manifest version is {TARGET_MANIFEST_VERSION}.")
    append_test(tests, counter, type="json_value_equals", path=manifest_rel,
                json_path="foundation_compatibility.required_files", expected=foundations,
                requirement="Grounding manifest is sealed to the exact current five-file AIR foundation.")
    append_test(tests, counter, type="json_value_equals", path=manifest_rel,
                json_path="foundation_compatibility.required_floor_invariants", expected=FLOORS,
                requirement="Grounding manifest requires AIR-FLOOR-013 through AIR-FLOOR-020.")
    append_test(tests, counter, type="json_value_equals", path=manifest_rel, json_path="components",
                expected=manifest["components"],
                requirement="Grounding manifest component identities exactly match the resealed component bytes.")

    for record in foundations:
        rel = f"prompts/{record['filename']}"
        append_test(tests, counter, type="sha256_equals", path=rel, expected=record["sha256"],
                    requirement=f"Grounding foundation seal remains bound to current {record['filename']} bytes.")

    known = set(component_identities)
    for filename in ["AIR_GROUNDING_METHOD_PACK.json", "AIR_GROUNDING_SPECIALIST.json", "AIR_GROUNDING_EXECUTOR.json"]:
        rel = f"profiles/grounding specialist/{filename}"
        obj = component_objects[filename]
        refs = dotted_paths_for_identity_refs(obj, known)
        if not refs:
            raise ValueError(f"no exact sibling identity refs found in {filename}")
        for path, value in refs:
            append_test(tests, counter, type="json_value_equals", path=rel, json_path=path, expected=value,
                        requirement=f"{filename} sibling pin {path} matches the resealed Grounding component identity.")

    test_manifest["tests"] = tests
    write_json(TEST_MANIFEST, test_manifest)

    # Fail closed with one direct run before the branch commit is created.
    subprocess.run([
        "python3", "tests/air_test_runner.py",
        "--manifest", "tests/air-test-manifest.json",
        "--output", "/tmp/group3-grounding-precheck.json",
        "--run-index", "1",
    ], cwd=ROOT, check=True)

    print(json.dumps({
        "foundation": foundations,
        "components": component_identities,
        "manifest": manifest_identity,
        "grounding_tests_added": counter[0],
    }, indent=2))


if __name__ == "__main__":
    main()
