from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_candidate_json_resources_parse() -> None:
    paths = [
        "profiles/hr/sp/index.json",
        "profiles/mo/gov-fw.json",
        "profiles/mo/sp/index.json",
        "prompts/mo/starter.json",
        "runtime/boot/mo-ext.json",
        "runtime/boot/mo-closure.json",
        "runtime/ed/manifest.json",
        "runtime/gov/fw.json",
        "runtime/ho/s/gov.json",
        "runtime/ho/t/gov.json",
        "tests/fx/edition.json",
        "tests/fx/gov.json",
    ]
    for path in paths:
        assert _json(path), path


def test_candidate_markdown_sentinels() -> None:
    expected = {
        "prompts/hr/GOV.md": "AIR_LOAD_SENTINEL :: AIR_HR_GOVERNANCE_SUPPLEMENT_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1",
        "prompts/mo/core.md": "AIR_LOAD_SENTINEL :: AIR_MO_CORE_ENTRY_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1",
        "prompts/mo/surface.md": "AIR_LOAD_SENTINEL :: AIR_MO_SURFACE_ENTRY_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1",
        "runtime/mod/r/gov-auth.md": "AIR_LOAD_SENTINEL :: AIR_RUNTIME_GOVERNANCE_APPROVAL_AND_AUTHORITY_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1",
        "runtime/mod/r/ho-gov.md": "AIR_LOAD_SENTINEL :: AIR_RUNTIME_HANDOFF_GOVERNANCE_STATE_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1",
        "runtime/mod/c/out-token.md": "AIR_LOAD_SENTINEL :: AIR_CONTROL_LEGACY_OUTPUT_AND_TOKEN_DEBUG_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1",
    }
    for path, sentinel in expected.items():
        lines = (ROOT / path).read_text(encoding="utf-8").rstrip().splitlines()
        assert lines[-1] == sentinel, path


def test_hr_prompt_set_is_complete() -> None:
    for name in (
        "AIR CORE RUNTIME.md",
        "AIR CONTROL SURFACE.md",
        "AIR DEFAULT STARTER PROFILE.json",
        "GOV.md",
    ):
        assert (ROOT / "prompts" / "hr" / name).is_file()


def test_mo_entry_and_closure_are_present_but_not_default() -> None:
    starter = _json("prompts/mo/starter.json")
    closure = _json("runtime/boot/mo-closure.json")
    editions = _json("runtime/ed/manifest.json")
    assert starter["edition"] == "MO_MACHINE_OPTIMIZED"
    assert closure["default_switch_allowed"] is False
    assert editions["editions"]["MO_MACHINE_OPTIMIZED"]["runtime_selection"] == "DEFAULT_ONLY_AFTER_VALIDATION"


def test_handoff_governance_excludes_restricted_source_text() -> None:
    schema = _json("runtime/ho/s/gov.json")
    template = _json("runtime/ho/t/gov.json")
    assert schema["properties"]["restricted_source_text_included"]["const"] is False
    assert template["restricted_source_text_included"] is False
    required = set(schema["required"])
    assert {
        "prompt_edition",
        "governance_floor_version",
        "open_approval_gate",
        "active_framework_projections",
        "source_rights_states",
        "token_debug_preference",
    } <= required


def test_extension_manifest_references_existing_resources() -> None:
    manifest = _json("runtime/boot/mo-ext.json")
    for module in manifest["modules"]:
        assert (ROOT / module["relative_path"]).is_file(), module["relative_path"]
    for path in manifest["data_resources"]:
        assert (ROOT / path).is_file(), path


def test_new_paths_are_windows_friendly() -> None:
    tracked = [
        "profiles/hr/sp/index.json",
        "profiles/mo/gov-fw.json",
        "profiles/mo/sp/index.json",
        "prompts/hr/GOV.md",
        "prompts/mo/core.md",
        "prompts/mo/starter.json",
        "prompts/mo/surface.md",
        "runtime/boot/mo-ext.json",
        "runtime/boot/mo-closure.json",
        "runtime/ed/manifest.json",
        "runtime/gov/fw.json",
        "runtime/ho/s/gov.json",
        "runtime/ho/t/gov.json",
        "runtime/mod/c/out-token.md",
        "runtime/mod/r/gov-auth.md",
        "runtime/mod/r/ho-gov.md",
        "tests/fx/edition.json",
        "tests/fx/gov.json",
    ]
    assert max(map(len, tracked)) <= 80
