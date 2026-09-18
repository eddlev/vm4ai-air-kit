#!/usr/bin/env python3
"""Dynamic full-surface integrity validator for AIR prompts/catalog/profiles.

This validator is release-gating evidence, not semantic authority. It discovers the
surface at runtime and requires two-way parity with the coverage manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any

VALIDATOR_IDENTITY = "AIR_FULL_SURFACE_INTEGRITY_VALIDATOR_V1"
IN_SCOPE_ROOTS = ("prompts", "catalog", "profiles")
TERMINAL_RESULTS = {"PASS", "NOT_APPLICABLE_WITH_EVIDENCE"}
BLOCKING_RESULTS = {"NOT_TESTED", "UNKNOWN", "PARTIAL", "STALE", "UNCLASSIFIED", "FAILED", "WAIVED_FOR_HARD_INVARIANT"}
REQUIRED_DIMENSIONS = {
    "PHYSICAL_PARSE",
    "IDENTITY_LIFECYCLE",
    "CLOSED_WORLD_SCHEMA",
    "SEMANTIC_OWNERSHIP",
    "PRODUCER_CONSUMER",
    "CROSS_FILE_REFERENCE",
    "AUTHORITY_BOUNDARY",
    "VISIBILITY_EMISSION",
    "ROUTE_STATE_MACHINE",
    "FAILURE_MODE",
    "BEHAVIORAL_CONTRACT",
    "MUTATION_TEST",
    "MIGRATION_BACKWARD_COMPAT",
    "SECURITY_PRIVACY_DATA_BOUNDARY",
    "RELEASE_REPRODUCIBILITY",
}
REQUIRED_SCENARIO_IDS = 20
HARD_MARKERS = {
    "prompts/AIR_CORE_RUNTIME.md": [
        "AIR-FLOOR-029-MANDATORY-VISIBLE-ALIGNMENT-AND-VALIDATION",
        "AIR-FLOOR-030-NEW-TASK-ARTIFACT-VISIBLE-BEFORE-CONTINUATION",
        "RT.DURABILITY_NEGOTIATE",
        "AIR_FULL_SURFACE_INTEGRITY_AUDIT_V1",
        "AIR_PROJECT_RECOVERY_BOOTSTRAP_NO_HANDOFF",
    ],
    "catalog/AIR_RUNTIME_ROUTE_MAP.json": [
        "AIR-FLOOR-029",
        "AIR-FLOOR-030",
        "RT.DURABILITY_NEGOTIATE",
        "DEP.DURABILITY_NEGOTIATION_RESOLVED",
    ],
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover(root: Path) -> list[str]:
    result = []
    for rel_root in IN_SCOPE_ROOTS:
        base = root / rel_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                result.append(path.relative_to(root).as_posix())
    return sorted(result)


def reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def parse_file(path: Path) -> None:
    data = path.read_bytes()
    if data.startswith(b"ï»¿"):
        raise ValueError("UTF-8 BOM prohibited")
    text = data.decode("utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        json.loads(text, object_pairs_hook=reject_duplicate_keys)
    elif suffix != ".md":
        raise ValueError(f"unexpected governed-surface file type: {suffix or '<none>'}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path, manifest_path: Path, scenario_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    manifest = load_json(manifest_path)
    scenarios = load_json(scenario_path)
    discovered = discover(root)
    records = manifest.get("files", [])
    manifest_paths = sorted(item.get("canonical_path", "") for item in records)
    if discovered != manifest_paths:
        for item in sorted(set(discovered) - set(manifest_paths)):
            errors.append(f"DISCOVERED_NOT_MANIFESTED:{item}")
        for item in sorted(set(manifest_paths) - set(discovered)):
            errors.append(f"MANIFEST_NOT_DISCOVERED:{item}")

    record_by_path = {item.get("canonical_path"): item for item in records}
    normalized_names = {}
    for rel in discovered:
        normalized = unicodedata.normalize("NFC", rel).casefold()
        prior = normalized_names.get(normalized)
        if prior is not None and prior != rel:
            errors.append(f"NORMALIZED_FILENAME_COLLISION:{prior}:{rel}")
        normalized_names[normalized] = rel
    for rel in discovered:
        path = root / rel
        try:
            parse_file(path)
        except Exception as exc:
            errors.append(f"PHYSICAL_PARSE:{rel}:{type(exc).__name__}:{exc}")
            continue
        rec = record_by_path.get(rel)
        if not rec:
            continue
        expected_sha = rec.get("sha256")
        if expected_sha and expected_sha != sha256_file(path):
            errors.append(f"STALE_RECEIPT:{rel}")
        expected_bytes = rec.get("byte_count")
        if expected_bytes is not None and expected_bytes != len(path.read_bytes()):
            errors.append(f"BYTE_COUNT_MISMATCH:{rel}")
        expected_lines = rec.get("line_count")
        if expected_lines is not None:
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            if expected_lines != actual_lines:
                errors.append(f"LINE_COUNT_MISMATCH:{rel}")
        dims = rec.get("audit_dimensions", {})
        missing_dims = REQUIRED_DIMENSIONS - set(dims)
        if missing_dims:
            errors.append(f"MISSING_DIMENSIONS:{rel}:{','.join(sorted(missing_dims))}")
        for dim, result in dims.items():
            if result in BLOCKING_RESULTS or result not in TERMINAL_RESULTS:
                errors.append(f"NON_TERMINAL_DIMENSION:{rel}:{dim}:{result}")
        for ref in rec.get("referenced_files", []):
            if ref not in record_by_path:
                errors.append(f"DANGLING_REFERENCE:{rel}->{ref}")

        if rel.endswith("_EXECUTOR.json"):
            text = path.read_text(encoding="utf-8")
            if "EXECUTOR_DRAFT_UNVALIDATED" in text or '"availability_state": "AVAILABLE_UNVALIDATED"' in text or '"status": "DRAFT"' in text:
                errors.append(f"EXECUTOR_DRAFT_LABEL_FORBIDDEN:{rel}")
            if "VALIDATED_AVAILABLE_UNBOUND" not in text:
                errors.append(f"EXECUTOR_VALIDATED_AVAILABLE_UNBOUND_REQUIRED:{rel}")

    for rel, markers in HARD_MARKERS.items():
        path = root / rel
        if not path.exists():
            errors.append(f"MISSING_HARD_INVARIANT_OWNER:{rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"MISSING_HARD_MARKER:{rel}:{marker}")

    scenario_items = scenarios.get("scenarios", [])
    ids = [item.get("scenario_id") for item in scenario_items]
    if len(scenario_items) < REQUIRED_SCENARIO_IDS:
        errors.append(f"SCENARIO_COUNT_LT_{REQUIRED_SCENARIO_IDS}:{len(scenario_items)}")
    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE_SCENARIO_ID")
    required_scenario_fields = {"scenario_id", "surface", "expected_visible_objects", "expected_artifact_behavior", "expected_decision"}
    for item in scenario_items:
        missing = required_scenario_fields - set(item)
        if missing:
            errors.append(f"SCENARIO_MISSING_FIELDS:{item.get('scenario_id')}:{','.join(sorted(missing))}")

    decision = "PASS" if not errors else "FAIL"
    return {
        "validator_identity": VALIDATOR_IDENTITY,
        "release_claim_boundary": "NO_KNOWN_OR_UNTESTED_GAP_WITHIN_DECLARED_AIR_PUBLIC_RELEASE_CONTRACT_SURFACE",
        "discovered_count": len(discovered),
        "manifest_count": len(records),
        "scenario_count": len(scenario_items),
        "errors": errors,
        "decision": decision,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", default="tests/air_full_surface_coverage_manifest.json")
    parser.add_argument("--scenario-matrix", default="tests/air_full_surface_scenario_matrix.json")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    report = validate(root, root / args.manifest, root / args.scenario_matrix)
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(f"{report['decision']} {VALIDATOR_IDENTITY}: files={report['discovered_count']} scenarios={report['scenario_count']} errors={len(report['errors'])}")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
