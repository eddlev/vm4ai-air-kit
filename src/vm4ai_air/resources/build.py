"""Build and validate AIR installed-resource metadata."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import re
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

from vm4ai_air.errors import ResourceIntegrityError

CANONICAL_ROOTS = ("prompts", "profiles", "runtime")
MANIFEST_NAME = "AIR INSTALLED RESOURCE MANIFEST.json"
INDEX_NAME = "AIR RESOURCE INDEX.json"
BUNDLES_NAME = "AIR INSTALLED BUNDLE DEFINITIONS.json"
RECEIPT_NAME = "AIR RESOURCE BUILD RECEIPT.json"
MANIFEST_SCHEMA_VERSION = "1.0.0"

_PATCH_MARKER = re.compile(r"^Patch marker:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
_SENTINEL = re.compile(r"^AIR_LOAD_SENTINEL\s*::\s*(.+?)\s*$")


def _pairs_no_duplicates(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ResourceIntegrityError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_loads(text: str, *, source: str = "<memory>") -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=lambda raw: (_ for _ in ()).throw(
                ResourceIntegrityError(f"Non-finite JSON constant {raw!r} in {source}")
            ),
        )
    except ResourceIntegrityError:
        raise
    except Exception as exc:
        raise ResourceIntegrityError(f"Invalid JSON in {source}: {exc}") from exc


def strict_json_load(path: Path) -> Any:
    try:
        return strict_json_loads(path.read_text(encoding="utf-8"), source=str(path))
    except OSError as exc:
        raise ResourceIntegrityError(f"Cannot read JSON resource {path}: {exc}") from exc


def _generated_at() -> str:
    source_date_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    moment = datetime.fromtimestamp(int(source_date_epoch), tz=UTC) if source_date_epoch else datetime.now(UTC)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resource_id_for_path(relative_path: str) -> str:
    """Return the canonical logical identifier for a repository-relative AIR resource path."""
    return "air://" + quote(relative_path, safe="/._-")


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result


def _boot_sentinel_map(source_root: Path) -> dict[str, str]:
    manifest_path = source_root / "runtime" / "boot" / "AIR BOOT MODULE MANIFEST.json"
    manifest = strict_json_load(manifest_path)
    result: dict[str, str] = {}
    for key in ("kernel", "boot_starter"):
        item = manifest.get(key)
        if isinstance(item, dict) and item.get("relative_path") and item.get("terminal_sentinel"):
            result[str(item["relative_path"])] = str(item["terminal_sentinel"])
    for module in manifest.get("modules", []):
        if isinstance(module, dict) and module.get("relative_path") and module.get("terminal_sentinel"):
            result[str(module["relative_path"])] = str(module["terminal_sentinel"])
    return result


def _last_nonempty_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()
    return ""


def _release_line(source_root: Path) -> str:
    manifest_path = source_root / "runtime" / "AIR RUNTIME DIRECTORY MANIFEST.json"
    value = strict_json_load(manifest_path)
    release_line = value.get("release_line") if isinstance(value, dict) else None
    return str(release_line or "unversioned")


def _canonical_files(source_root: Path) -> list[Path]:
    files: list[Path] = []
    for root_name in CANONICAL_ROOTS:
        root = source_root / root_name
        if not root.is_dir():
            raise ResourceIntegrityError(f"Missing canonical AIR source directory: {root}")
        for path in root.rglob("*"):
            if path.is_symlink():
                raise ResourceIntegrityError(f"Canonical AIR resources may not contain symlinks: {path}")
            if path.is_file() and "__pycache__" not in path.parts and not path.name.endswith(".pyc"):
                files.append(path)
    return sorted(files, key=lambda item: item.relative_to(source_root).as_posix().casefold())


def _json_metadata(value: Any) -> tuple[list[str], list[str]]:
    aliases: list[str] = []
    markers: list[str] = []
    if not isinstance(value, dict):
        return aliases, markers
    for key in (
        "SYSTEM_DESIGNATION",
        "module_id",
        "schema_id",
        "title",
        "PROFILE_KIND",
        "artifact_class",
        "STANDARD_CODE",
    ):
        item = value.get(key)
        if isinstance(item, str):
            aliases.append(item)
    patch_marker = value.get("patch_marker")
    if isinstance(patch_marker, str):
        markers.append(patch_marker)
    elif isinstance(patch_marker, list):
        markers.extend(str(item) for item in patch_marker if isinstance(item, str))
    return aliases, markers


def _record_for_file(path: Path, source_root: Path, expected_sentinels: dict[str, str]) -> dict[str, Any]:
    relative_path = path.relative_to(source_root).as_posix()
    data = path.read_bytes()
    aliases = [relative_path, path.name, path.stem]
    headings: list[str] = []
    semantic_markers: list[str] = []
    terminal_sentinel: str | None = None

    if path.suffix.lower() == ".json":
        value = strict_json_loads(data.decode("utf-8"), source=relative_path)
        json_aliases, json_markers = _json_metadata(value)
        aliases.extend(json_aliases)
        semantic_markers.extend(json_markers)
    elif path.suffix.lower() in {".md", ".markdown", ".txt", ".rego", ".py", ".ps1", ".sh", ".cmd"}:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ResourceIntegrityError(f"Text resource is not UTF-8: {relative_path}") from exc
        if path.suffix.lower() in {".md", ".markdown"}:
            headings = [match.group(2).strip() for match in _HEADING.finditer(text)][:200]
            semantic_markers.extend(match.group(1).strip() for match in _PATCH_MARKER.finditer(text))
            last_line = _last_nonempty_line(text)
            if _SENTINEL.match(last_line):
                terminal_sentinel = last_line
        expected = expected_sentinels.get(relative_path)
        canonical_prompt = relative_path in {
            "prompts/AIR CORE RUNTIME.md",
            "prompts/AIR CONTROL SURFACE.md",
        }
        if expected and terminal_sentinel != expected:
            raise ResourceIntegrityError(
                f"Terminal sentinel mismatch for {relative_path}",
                details={"expected": expected, "observed": terminal_sentinel},
            )
        if canonical_prompt and not terminal_sentinel:
            raise ResourceIntegrityError(f"Canonical prompt is missing a terminal sentinel: {relative_path}")

    media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {
        "resource_id": resource_id_for_path(relative_path),
        "relative_path": relative_path,
        "package_path": relative_path,
        "file_name": path.name,
        "media_type": media_type,
        "size_bytes": len(data),
        "sha256": _sha256(data),
        "aliases": _dedupe(aliases),
        "headings": _dedupe(headings),
        "semantic_markers": _dedupe(semantic_markers),
        "terminal_sentinel": terminal_sentinel,
    }


def tree_digest_for_records(records: Iterable[Mapping[str, Any]]) -> str:
    """Compute the canonical aggregate digest for an ordered resource manifest record set."""
    tree_hasher = hashlib.sha256()
    for record in records:
        tree_hasher.update(str(record["relative_path"]).encode("utf-8"))
        tree_hasher.update(b"\0")
        tree_hasher.update(str(record["sha256"]).encode("ascii"))
        tree_hasher.update(b"\n")
    return tree_hasher.hexdigest()


def build_manifest(source_root: Path, package_version: str) -> dict[str, Any]:
    root = source_root.resolve()
    expected_sentinels = _boot_sentinel_map(root)
    records = [_record_for_file(path, root, expected_sentinels) for path in _canonical_files(root)]
    tree_digest = tree_digest_for_records(records)
    release_line = _release_line(root)
    return {
        "schema_id": "AIR_INSTALLED_RESOURCE_MANIFEST",
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "package_version": package_version,
        "authoring_release_line": release_line,
        "resource_set_version": f"{release_line}+sha256.{tree_digest[:12]}",
        "source_tree_digest": f"sha256:{tree_digest}",
        "generated_at_utc": _generated_at(),
        "canonical_roots": list(CANONICAL_ROOTS),
        "resource_count": len(records),
        "resources": records,
        "claim_boundary": (
            "This manifest proves the observed packaged file relationship and digests. "
            "It does not prove behavioural correctness, authorization, backend enforcement, or release approval."
        ),
    }


def build_index(manifest: dict[str, Any]) -> dict[str, Any]:
    entries = []
    for record in manifest["resources"]:
        entries.append(
            {
                "resource_id": record["resource_id"],
                "relative_path": record["relative_path"],
                "file_name": record["file_name"],
                "media_type": record["media_type"],
                "aliases": record["aliases"],
                "headings": record["headings"],
                "semantic_markers": record["semantic_markers"],
            }
        )
    return {
        "schema_id": "AIR_RESOURCE_INDEX",
        "schema_version": "1.0.0",
        "resource_set_version": manifest["resource_set_version"],
        "entries": entries,
    }


def _id_for_path(manifest: dict[str, Any], relative_path: str) -> str:
    for record in manifest["resources"]:
        if record["relative_path"] == relative_path:
            return str(record["resource_id"])
    raise ResourceIntegrityError(f"Bundle references missing resource: {relative_path}")


def build_bundle_definitions(manifest: dict[str, Any]) -> dict[str, Any]:
    complete_paths = [
        "prompts/AIR CORE RUNTIME.md",
        "prompts/AIR CONTROL SURFACE.md",
        "prompts/AIR DEFAULT STARTER PROFILE.json",
    ]
    return {
        "schema_id": "AIR_INSTALLED_BUNDLE_DEFINITIONS",
        "schema_version": "1.0.0",
        "resource_set_version": manifest["resource_set_version"],
        "bundles": [
            {
                "bundle_id": "COMPLETE_AIR_PROMPT_SET",
                "display_name": "Complete AIR Prompt Set",
                "status": "AVAILABLE",
                "resources": [_id_for_path(manifest, path) for path in complete_paths],
                "user_facing": True,
            },
            {
                "bundle_id": "LEGACY_MODULAR_BOOT_SOURCE_SET",
                "display_name": "Legacy modular boot source set",
                "status": "MIGRATION_PENDING_STAGE_3",
                "resources": [
                    _id_for_path(manifest, "runtime/boot/AIR BOOT KERNEL.md"),
                    _id_for_path(manifest, "runtime/boot/AIR BOOT MODULE MANIFEST.json"),
                    _id_for_path(manifest, "runtime/boot/AIR BOOT STARTER PROFILE.json"),
                ],
                "user_facing": False,
            },
        ],
    }


def build_receipt(manifest: dict[str, Any]) -> dict[str, Any]:
    sentinel_count = sum(1 for record in manifest["resources"] if record.get("terminal_sentinel"))
    json_count = sum(1 for record in manifest["resources"] if record["relative_path"].endswith(".json"))
    return {
        "schema_id": "AIR_RESOURCE_BUILD_RECEIPT",
        "schema_version": "1.0.0",
        "package_version": manifest["package_version"],
        "resource_set_version": manifest["resource_set_version"],
        "source_tree_digest": manifest["source_tree_digest"],
        "generated_at_utc": manifest["generated_at_utc"],
        "checks": {
            "canonical_roots_present": True,
            "all_json_parsed_strictly": True,
            "declared_sentinels_verified": True,
            "canonical_prompt_sentinels_verified": True,
            "resource_count": manifest["resource_count"],
            "json_count": json_count,
            "sentinel_count": sentinel_count,
        },
        "decision": "PASS",
        "claim_boundary": "Build-time structural and digest evidence only; behavioural tests remain separate.",
    }


def write_generated_metadata(source_root: Path, output_dir: Path, package_version: str) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(source_root, package_version)
    payloads = {
        MANIFEST_NAME: manifest,
        INDEX_NAME: build_index(manifest),
        BUNDLES_NAME: build_bundle_definitions(manifest),
        RECEIPT_NAME: build_receipt(manifest),
    }
    for name, value in payloads.items():
        (output_dir / name).write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return manifest
