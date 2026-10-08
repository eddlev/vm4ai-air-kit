from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_VERSION = "0.8.1"
EXPECTED_SOURCE_TUPLE = "d4678f03448f35c713c11565069715c6fd168bda50601b04a445e86f0f0fce64"
EXPECTED_DERIVED_FP = "729b585f9d2c5a41d273a08f8da313f24847d38c8c61063fb5b830bc215fc4c1"
EXPECTED_CLIENT_RUNTIME_FP = "5b96ee3141ff8cea896c2a26129916ba063aaef6bcdf2df4ea16b9119e74637c"
EXPECTED_RUNTIME_STATE = "R23_AMRS4F_PACKAGE_ENABLED_SEMANTIC_OWNER_CUTOVER"
EXPECTED_CORE_SHA = "6007ab277ebcd0d59911fce6384a8ef417dbdd6f3eea38bfc71e39013b097588"
EXPECTED_HANDOFF_SHA = "8d1c87d3d4d2b191301eec9f27e83ac1e550b0ba99bede5a5d576e9d52e5f122"
EXPECTED_COMMANDS = {
    "default_tier0": "Start a new AIR-P project.",
    "explicit_tier0": "Start a new AIR-P project. Tier0 boot.",
    "explicit_tier1": "Start a new AIR-P project. Tier1 boot.",
    "explicit_tier2": "Start a new AIR-P project. Tier2 boot.",
    "explicit_tier3": "Start a new AIR-P project. Tier3 boot.",
}
CLIENT_EXCLUDED_GENERATED_PATHS = {"tests/test_air_p_compiler.py", "source/AIR_LAW_APPLICABILITY_ROUTER.json"}


class ValidationError(Exception):
    pass


def req(cond: bool, message: str) -> None:
    if not cond:
        raise ValidationError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    def reject_dupes(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValidationError(f"duplicate JSON key {key} in {path}")
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_dupes)


def validate_manifest(root: Path, manifest_path: Path, *, source_tuple: bool = False, exact_closure: bool = False) -> dict:
    obj = load_json(manifest_path)
    entries = obj.get("files", [])
    req(isinstance(entries, list) and entries, f"empty files manifest {manifest_path}")
    expected_paths = {entry["path"] for entry in entries}
    req(len(expected_paths) == len(entries), f"duplicate manifest path {manifest_path}")
    for entry in entries:
        p = root / entry["path"]
        req(p.is_file(), f"missing manifest file {entry['path']}")
        raw = p.read_bytes()
        req(len(raw) == entry["size_bytes"], f"size mismatch {entry['path']}")
        req(hashlib.sha256(raw).hexdigest() == entry["sha256"], f"hash mismatch {entry['path']}")
    if exact_closure:
        observed_paths = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
        req(observed_paths == expected_paths, f"manifest closure mismatch {manifest_path}: extra={sorted(observed_paths-expected_paths)} missing={sorted(expected_paths-observed_paths)}")
    if source_tuple:
        preimage = {
            "contract_id": "AIR_CANONICAL_SOURCE_TUPLE_V2",
            "contract_version": "2.0.0",
            "files": {e["path"]: e["sha256"] for e in sorted(entries, key=lambda x: x["path"])},
        }
        observed = hashlib.sha256(json.dumps(preimage, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        req(observed == obj["source_tuple_v2_sha256"] == EXPECTED_SOURCE_TUPLE, "canonical source tuple mismatch")
    return obj


def validate_starter(root: Path) -> None:
    source_starter_path = root / "source/prompts/AIR_DEFAULT_STARTER_PROFILE.json"
    public_starter_path = root / "prompts/AIR_DEFAULT_STARTER_PROFILE.json"
    req(source_starter_path.read_bytes() == public_starter_path.read_bytes(), "public Starter differs from canonical source Starter")
    starter = load_json(source_starter_path)
    req(starter.get("PROMPT_VERSION") == "2.7.0", "Starter PROMPT_VERSION drift")
    states = starter["validation_contract"]["core_runtime_transition_identity_contract"]["current_cutover_states"]
    final = [x for x in states if x.get("state_id") == EXPECTED_RUNTIME_STATE]
    req(len(final) == 1, "exact current AMRS4F state missing or duplicated")
    final = final[0]
    req(final["core_sha256"] == EXPECTED_CORE_SHA, "current Core state hash drift")
    req(final["handoff_template_revision"] == 26, "current state Handoff revision drift")
    req(final["handoff_template_sha256"] == EXPECTED_HANDOFF_SHA, "current state Handoff hash drift")

    consumer = starter["compiler_contract"]["decision_trace_transition_consumer_contract"]
    req(consumer["current_core_sha256"] == EXPECTED_CORE_SHA, "Starter current consumer Core metadata stale")
    req(consumer["current_handoff_template_revision"] == 26, "Starter current consumer Handoff revision stale")
    req(consumer["current_handoff_sha256"] == EXPECTED_HANDOFF_SHA, "Starter current consumer Handoff hash stale")
    req(consumer["current_formal_object_profile"]["object_count"] == 21, "Starter current formal-object profile stale")
    req(consumer["current_law_registry_profile"]["stable_law_count"] == 83, "Starter current law registry profile stale")

    revision = starter["handoff_contract"]["revision_identity_contract"]
    req(revision["current_template_revision"] == 26, "Starter current_template_revision is not 26")
    req(revision["current_template_sha256"] == EXPECTED_HANDOFF_SHA, "Starter current template SHA drift")
    req(revision["current_template_state_id"] == EXPECTED_RUNTIME_STATE, "Starter current template state id drift")

    mirror = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
    req(mirror.get("canonical_first_message_commands") == EXPECTED_COMMANDS, "canonical first-message command set drift")
    dispatch = mirror["user_boot_profile_dispatch"]
    mapping = {
        "TIER_0_ROUTINE": "explicit_tier0",
        "TIER_1_NAVIGATION": "explicit_tier1",
        "TIER_2_TARGETED_SOURCE": "explicit_tier2",
        "TIER_3_DEEP_AUDIT": "explicit_tier3",
    }
    for tier, key in mapping.items():
        req(EXPECTED_COMMANDS[key] in dispatch[tier]["selection_aliases"], f"missing exact first-message alias for {tier}")
    guard = mirror.get("exact_section_boundary_guard", "")
    req("Tier0 dependency-closure" in guard, "Tier0 dependency closure absent from exact-boundary guard")
    req("discarded before model-visible ingestion" in guard, "adjacent-context discard rule missing")
    req(any("adjacent context" in x for x in dispatch["TIER_0_ROUTINE"]["negative_requirements"]), "Tier0 adjacent-context negative contract missing")


def validate_public_source_mirrors(root: Path) -> None:
    for rel in [
        "prompts/AIR_CORE_RUNTIME.md",
        "prompts/AIR_CONTROL_SURFACE.md",
        "prompts/AIR_GOV.md",
        "prompts/AIR_DEFAULT_STARTER_PROFILE.json",
        "prompts/AIR_HANDOFF_CARD_TEMPLATE.json",
        "catalog/AIR_RUNTIME_ROUTE_MAP.json",
        "catalog/AIR_LAW_APPLICABILITY_ROUTER.json",
    ]:
        req((root / rel).is_file(), f"missing public source mirror {rel}")
        req((root / rel).read_bytes() == (root / "source" / rel).read_bytes(), f"public source mirror drift {rel}")


def validate_public_surface(root: Path) -> None:
    req((root / "VERSION").read_text(encoding="utf-8").strip() == EXPECTED_VERSION, "VERSION is not 0.8.1")
    req(not (root / "profiles").exists(), "obsolete profiles/ layout still present")
    readme = (root / "README.md").read_text(encoding="utf-8")
    for command in EXPECTED_COMMANDS.values():
        req(command in readme, f"README missing command: {command}")
    req("v0.8.1 source-synchronization candidate" in readme, "README candidate-state boundary missing")
    workflow = (root / ".github/workflows/air-reproducibility.yml").read_text(encoding="utf-8")
    req("python3 tools/validate_air_suite.py" in workflow, "workflow does not call current validation suite")
    req("v074" not in workflow.lower() and "0.7.4" not in workflow, "workflow still routes to v0.7.4 authority")
    release_entry = (root / "tools/validate_air_release.py").read_text(encoding="utf-8")
    req("validate_air_v081_repository" in release_entry, "active release validator is not v0.8.1")
    suite = (root / "tools/validate_air_suite.py").read_text(encoding="utf-8")
    req("validate_air_v081_repository.py" in suite, "active suite does not run v0.8.1 repository validator")
    req("test_air_v081_repository_mutations.py" in suite, "active suite does not run v0.8.1 mutation contract")


def validate_versions(root: Path) -> None:
    core = (root / "source/prompts/AIR_CORE_RUNTIME.md").read_text(encoding="utf-8")
    control = (root / "source/prompts/AIR_CONTROL_SURFACE.md").read_text(encoding="utf-8")
    gov = (root / "source/prompts/AIR_GOV.md").read_text(encoding="utf-8")
    handoff = load_json(root / "source/prompts/AIR_HANDOFF_CARD_TEMPLATE.json")["AIR_HANDOFF_CARD"]
    route = load_json(root / "source/catalog/AIR_RUNTIME_ROUTE_MAP.json")
    index = load_json(root / "catalog/AIR_SPECIALIST_PACKAGE_INDEX.json")
    req("PROMPT_VERSION: 2.9.0" in core, "Core is not 2.9.0")
    req("PROMPT_VERSION: 2.7.0" in control, "Control is not 2.7.0")
    req("PROMPT_VERSION: 2.4.0" in gov, "Governance is not 2.4.0")
    req(handoff["schema_version"] == handoff["SCHEMA_VERSION"] == "2.3.0", "Handoff schema drift")
    req(handoff["template_revision"] == 26, "Handoff template is not rev26")
    req(route["MAP_VERSION"] == route["ROUTE_MAP_VERSION"] == "1.2.5", "Route Map is not 1.2.5")
    req(index["INDEX_VERSION"] == "1.3.15", "Specialist Index is not 1.3.15")


def file_inventory(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def validate_compiler_and_checked_in_runtime(root: Path) -> None:
    source_root = root / "source"
    py = sys.executable
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run([py, "-B", "-m", "unittest", "discover", "-s", "air_p/tests", "-p", "test_air_p_compiler.py"], cwd=source_root, check=True, env=env)
    builds = []
    with tempfile.TemporaryDirectory(prefix="air-v081-builds-") as td:
        td = Path(td)
        for i in range(3):
            out = td / f"build-{i+1}"
            subprocess.run([py, "-B", "air_p/compiler/compile_air_p.py", "--source-root", str(source_root), "--output", str(out)], cwd=source_root, check=True, stdout=subprocess.DEVNULL, env=env)
            builds.append(out)
        inv = [file_inventory(x) for x in builds]
        req(inv[0] == inv[1] == inv[2], "three compiler builds are not byte-identical")
        req(len(inv[0]) == 142, f"unexpected compiler output count {len(inv[0])}")
        fp = hashlib.sha256(json.dumps([{"path": p, "sha256": h} for p, h in sorted(inv[0].items())], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        req(fp == EXPECTED_DERIVED_FP, "derived inventory fingerprint drift")
        checked = {p: h for p, h in inv[0].items() if p not in CLIENT_EXCLUDED_GENERATED_PATHS}
        cfp = hashlib.sha256(json.dumps([{"path": p, "sha256": h} for p, h in sorted(checked.items())], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        req(cfp == EXPECTED_CLIENT_RUNTIME_FP, "client runtime subset fingerprint drift")
        for rel, expected_hash in checked.items():
            p = root / "air_p" / rel
            req(p.is_file(), f"checked-in client runtime missing air_p/{rel}")
            req(sha(p) == expected_hash, f"checked-in client runtime mismatch air_p/{rel}")
        for rel in CLIENT_EXCLUDED_GENERATED_PATHS:
            req(not (root / "air_p" / rel).exists(), f"client-excluded generated path present air_p/{rel}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    source_manifest = validate_manifest(root / "source", root / "release/AIR_CURRENT_PROJECT_SOURCE_MANIFEST_R131_V081_CANDIDATE.json", source_tuple=True, exact_closure=True)
    req(source_manifest.get("source_file_count") == 126, "source file count is not 126")
    client_runtime = validate_manifest(root, root / "release/AIR_V081_CLIENT_RUNTIME_MANIFEST.json")
    client_runtime_paths = {x["path"] for x in client_runtime["files"]}
    observed_client_runtime_paths = {p.relative_to(root).as_posix() for p in (root / "air_p").rglob("*") if p.is_file()}
    req(observed_client_runtime_paths == client_runtime_paths, f"client runtime closure mismatch: extra={sorted(observed_client_runtime_paths-client_runtime_paths)} missing={sorted(client_runtime_paths-observed_client_runtime_paths)}")
    req(client_runtime.get("checked_in_client_runtime_file_count") == 140, "client runtime file count is not 140")
    req(set(client_runtime.get("excluded_generated_paths", [])) == CLIENT_EXCLUDED_GENERATED_PATHS, "client runtime exclusion set drift")
    req(client_runtime.get("client_runtime_inventory_fingerprint_sha256") == EXPECTED_CLIENT_RUNTIME_FP, "client runtime manifest fingerprint drift")
    specialists = validate_manifest(root, root / "release/AIR_V081_SPECIALIST_BASELINE_MANIFEST.json")
    req(specialists.get("file_count") == 29, "Specialist/evidence carry-forward count drift")
    expected_specialist_paths = {x["path"] for x in specialists["files"]}
    observed_specialist_paths = {p.relative_to(root).as_posix() for surface in (root / "specialists", root / "evidence") for p in surface.rglob("*") if p.is_file()}
    observed_specialist_paths.add("catalog/AIR_SPECIALIST_PACKAGE_INDEX.json")
    req(observed_specialist_paths == expected_specialist_paths, f"Specialist/evidence closure mismatch: extra={sorted(observed_specialist_paths-expected_specialist_paths)} missing={sorted(expected_specialist_paths-observed_specialist_paths)}")

    delta = load_json(root / "release/SOURCE_DELTA_R130_TO_R131_V081_CANDIDATE.json")
    req(delta.get("changed_file_count") == 3 and delta.get("added_file_count") == 0 and delta.get("deleted_file_count") == 0, "R130->R131 source delta scope drift")
    req({x["path"] for x in delta["changed_files"]} == {
        "air_p/compiler/air_p_compiler_engine.py",
        "air_p/tests/test_air_p_compiler.py",
        "prompts/AIR_DEFAULT_STARTER_PROFILE.json",
    }, "R130->R131 changed source path set drift")

    validate_starter(root)
    validate_versions(root)
    validate_public_source_mirrors(root)
    validate_public_surface(root)
    if not args.quick:
        validate_compiler_and_checked_in_runtime(root)

    print("AIR v0.8.1 repository validation: PASS")
    print("source_tuple", EXPECTED_SOURCE_TUPLE)
    print("derived_inventory", EXPECTED_DERIVED_FP)
    print("client_runtime_inventory", EXPECTED_CLIENT_RUNTIME_FP)
    print("runtime_state", EXPECTED_RUNTIME_STATE)
    print("mode", "QUICK" if args.quick else "FULL")


if __name__ == "__main__":
    try:
        main()
    except (ValidationError, KeyError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"AIR v0.8.1 repository validation: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
