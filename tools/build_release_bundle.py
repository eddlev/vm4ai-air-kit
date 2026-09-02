#!/usr/bin/env python3
"""Build deterministic AIR core release assets from the current repository foundation."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
VERSION_FILE = ROOT / "VERSION"

FOUNDATION = [
    ("AIR_CORE_RUNTIME.md", ROOT / "prompts" / "AIR_CORE_RUNTIME.md"),
    ("AIR_CONTROL_SURFACE.md", ROOT / "prompts" / "AIR_CONTROL_SURFACE.md"),
    ("AIR_GOV.md", ROOT / "prompts" / "AIR_GOV.md"),
    ("AIR_DEFAULT_STARTER_PROFILE.json", ROOT / "prompts" / "AIR_DEFAULT_STARTER_PROFILE.json"),
    ("AIR_HANDOFF_CARD_TEMPLATE.json", ROOT / "prompts" / "AIR_HANDOFF_CARD_TEMPLATE.json"),
]

EXTRA_FILES = [
    ("START_HERE.md", ROOT / "START_HERE.md"),
    ("RELEASE_CHANNEL_POLICY.md", ROOT / "RELEASE_CHANNEL_POLICY.md"),
    ("VALIDATION_EVIDENCE_0.6.0-preview.1.md", ROOT / "VALIDATION_EVIDENCE_0.6.0-preview.1.md"),
    ("BUG_REPORTING.md", ROOT / "BUG_REPORTING.md"),
    ("COMPATIBILITY.md", ROOT / "COMPATIBILITY.md"),
    ("LICENSE", ROOT / "LICENSE"),
    ("NOTICE", ROOT / "NOTICE"),
]

ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644 << 16
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_text_version(path: Path, field: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(field)}:\s*([^\s]+)\s*$", text, re.MULTILINE)
    if not match:
        raise SystemExit(f"missing {field} in {path.relative_to(ROOT)}")
    return match.group(1)


def require_kit_release_version() -> str:
    if not VERSION_FILE.is_file():
        raise SystemExit("missing VERSION file")
    value = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(value):
        raise SystemExit(f"invalid AIR Kit release version in VERSION: {value!r}")
    return value


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def zip_bytes(entries: dict[str, bytes], output: Path) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = FILE_MODE
            info.create_system = 3
            archive.writestr(info, entries[name])


def main() -> None:
    kit_release_version = require_kit_release_version()
    core_version = require_text_version(FOUNDATION[0][1], "PROMPT_VERSION")
    control_version = require_text_version(FOUNDATION[1][1], "PROMPT_VERSION")
    governance_version = require_text_version(FOUNDATION[2][1], "PROMPT_VERSION")
    starter = load_json(FOUNDATION[3][1])
    handoff = load_json(FOUNDATION[4][1])

    starter_version = starter.get("PROMPT_VERSION")
    card = handoff.get("AIR_HANDOFF_CARD", {})
    handoff_schema = card.get("schema_version")
    handoff_schema_upper = card.get("SCHEMA_VERSION")

    if not starter_version:
        raise SystemExit("missing PROMPT_VERSION in AIR_DEFAULT_STARTER_PROFILE.json")
    if not handoff_schema or handoff_schema != handoff_schema_upper:
        raise SystemExit("Handoff schema_version / SCHEMA_VERSION missing or inconsistent")

    source_entries: dict[str, bytes] = {}
    file_manifest = []
    for bundle_name, source_path in FOUNDATION:
        if not source_path.is_file():
            raise SystemExit(f"missing required foundation file: {source_path.relative_to(ROOT)}")
        data = source_path.read_bytes()
        source_entries[bundle_name] = data
        file_manifest.append(
            {
                "filename": bundle_name,
                "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256_bytes(data),
                "size_bytes": len(data),
            }
        )

    for bundle_name, source_path in EXTRA_FILES:
        if not source_path.is_file():
            raise SystemExit(f"missing release file: {source_path.relative_to(ROOT)}")
        source_entries[bundle_name] = source_path.read_bytes()

    release_tag = os.environ.get("AIR_RELEASE_TAG") or None
    source_revision = os.environ.get("AIR_SOURCE_COMMIT") or None

    manifest = {
        "bundle_designation": "AIR_CORE_RELEASE_BUNDLE_V2",
        "bundle_version": kit_release_version,
        "kit_release_version": kit_release_version,
        "release_tag": release_tag,
        "source_revision": source_revision,
        "runtime_origin": "PROMPT_COMPILED",
        "backend_validation_claimed": False,
        "hidden_reasoning_claimed": False,
        "foundation_versions": {
            "core": core_version,
            "control": control_version,
            "governance": governance_version,
            "starter": starter_version,
            "handoff_schema": handoff_schema,
        },
        "foundation_files": file_manifest,
        "bundle_contents": sorted([*source_entries.keys(), "AIR_CORE_MANIFEST.json"]),
        "versioning_boundary": "AIR Kit release version and AIR runtime component versions are separate version axes.",
        "assurance_boundary": "The manifest identifies packaged repository bytes. It does not prove host-model behavior, backend enforcement, correctness, or provider compatibility.",
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    source_entries["AIR_CORE_MANIFEST.json"] = manifest_bytes

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    stable_zip = DIST / "AIR-core.zip"
    versioned_zip = DIST / f"AIR-v{kit_release_version}-core.zip"
    zip_bytes(source_entries, stable_zip)
    shutil.copyfile(stable_zip, versioned_zip)
    (DIST / "AIR_CORE_MANIFEST.json").write_bytes(manifest_bytes)

    checksum_targets = [stable_zip, versioned_zip, DIST / "AIR_CORE_MANIFEST.json"]
    checksum_lines = [f"{sha256_bytes(path.read_bytes())}  {path.name}" for path in checksum_targets]
    (DIST / "SHA256SUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    with zipfile.ZipFile(stable_zip, "r") as archive:
        names = archive.namelist()
        expected = sorted(source_entries)
        if names != expected:
            raise SystemExit(f"bundle contents mismatch: expected {expected}, got {names}")

    if stable_zip.read_bytes() != versioned_zip.read_bytes():
        raise SystemExit("stable and versioned AIR bundle bytes differ")

    print(
        f"AIR Kit v{kit_release_version} assets built "
        f"for Core {core_version} / Control {control_version} / Starter {starter_version}"
    )
    for path in sorted(DIST.iterdir()):
        print(f"{path.name}: {len(path.read_bytes())} bytes sha256={sha256_bytes(path.read_bytes())}")


if __name__ == "__main__":
    main()
