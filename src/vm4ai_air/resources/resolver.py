"""Single installed-resource resolver used by every AIR local consumer."""

from __future__ import annotations

import hashlib
import os
import re
from collections.abc import Mapping
from importlib import resources as importlib_resources
from pathlib import Path, PurePosixPath
from typing import Any

from vm4ai_air.errors import ResourceError, ResourceIntegrityError
from vm4ai_air.io import atomic_write_bytes, atomic_write_json, utc_now
from vm4ai_air.paths import AppPaths
from vm4ai_air.resources.build import (
    CANONICAL_ROOTS,
    MANIFEST_NAME,
    MANIFEST_SCHEMA_VERSION,
    build_manifest,
    resource_id_for_path,
    strict_json_loads,
    tree_digest_for_records,
)
from vm4ai_air.version import __version__

_TOKEN = re.compile(r"[a-z0-9_./:-]+")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_CANONICAL_ROOT_SET = set(CANONICAL_ROOTS)
_RESOURCE_SET_VERSION = re.compile(r"^.+\+sha256\.[0-9a-f]{12}$")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ResourceResolver:
    def __init__(
        self,
        root: Any,
        manifest: Mapping[str, Any],
        *,
        origin: str,
        paths: AppPaths | None = None,
    ) -> None:
        self.root = root
        self.manifest = dict(manifest)
        self.origin = origin
        self.paths = paths or AppPaths.resolve()
        self._records = self._validate_manifest(self.manifest)
        self._by_id = {str(item["resource_id"]): item for item in self._records}
        self._by_path = {str(item["relative_path"]): item for item in self._records}

    @staticmethod
    def _safe_relative_path(value: object, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise ResourceIntegrityError(f"Resource manifest field {field} must be a non-empty string")
        normalized = value.replace("\\", "/")
        raw_parts = normalized.split("/")
        path = PurePosixPath(normalized)
        if (
            path.is_absolute()
            or any(part in {"", ".", ".."} for part in raw_parts)
            or not path.parts
            or ":" in path.parts[0]
        ):
            raise ResourceIntegrityError(f"Unsafe resource manifest path in {field}: {value}")
        if path.parts[0] not in _CANONICAL_ROOT_SET:
            raise ResourceIntegrityError(f"Resource manifest path is outside canonical roots: {value}")
        return path.as_posix()

    @staticmethod
    def _string_list(value: object, field: str, relative_path: str) -> list[str]:
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            raise ResourceIntegrityError(
                f"Resource manifest field {field} must be an array of strings: {relative_path}"
            )
        return list(value)

    @classmethod
    def _validate_manifest(cls, manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
        if manifest.get("schema_id") != "AIR_INSTALLED_RESOURCE_MANIFEST":
            raise ResourceIntegrityError("Installed resource manifest schema_id is invalid")
        if manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
            raise ResourceIntegrityError(
                "Installed resource manifest schema_version is unsupported",
                details={"expected": MANIFEST_SCHEMA_VERSION, "observed": manifest.get("schema_version")},
            )
        if manifest.get("package_version") != __version__:
            raise ResourceIntegrityError(
                "Installed resource manifest package version does not match application code",
                details={"manifest": manifest.get("package_version"), "application": __version__},
            )
        if manifest.get("canonical_roots") != list(CANONICAL_ROOTS):
            raise ResourceIntegrityError(
                "Installed resource manifest canonical_roots are invalid",
                details={"expected": list(CANONICAL_ROOTS), "observed": manifest.get("canonical_roots")},
            )
        release_line = manifest.get("authoring_release_line")
        if not isinstance(release_line, str) or not release_line.strip():
            raise ResourceIntegrityError("Installed resource manifest authoring_release_line is invalid")
        declared_resource_set = manifest.get("resource_set_version")
        if not isinstance(declared_resource_set, str) or not _RESOURCE_SET_VERSION.fullmatch(declared_resource_set):
            raise ResourceIntegrityError("Installed resource manifest resource_set_version is invalid")
        declared_tree_digest = manifest.get("source_tree_digest")
        if not isinstance(declared_tree_digest, str) or not declared_tree_digest.startswith("sha256:"):
            raise ResourceIntegrityError("Installed resource manifest source_tree_digest is invalid")

        resources = manifest.get("resources")
        if not isinstance(resources, list) or not resources:
            raise ResourceIntegrityError("Installed resource manifest has no resources array")
        records: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        seen_paths: set[str] = set()
        for raw in resources:
            if not isinstance(raw, Mapping):
                raise ResourceIntegrityError("Resource manifest entries must be objects")
            record = dict(raw)
            relative_path = cls._safe_relative_path(record.get("relative_path"), "relative_path")
            package_path = cls._safe_relative_path(record.get("package_path"), "package_path")
            if relative_path != package_path:
                raise ResourceIntegrityError(
                    "Stage 2 resource manifest requires relative_path and package_path to match",
                    details={"relative_path": relative_path, "package_path": package_path},
                )
            resource_id = record.get("resource_id")
            expected_resource_id = resource_id_for_path(relative_path)
            if resource_id != expected_resource_id:
                raise ResourceIntegrityError(
                    f"Resource manifest entry has an invalid resource_id: {relative_path}",
                    details={"expected": expected_resource_id, "observed": resource_id},
                )
            digest = record.get("sha256")
            size = record.get("size_bytes")
            if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
                raise ResourceIntegrityError(f"Invalid SHA-256 digest for {relative_path}")
            if not isinstance(size, int) or isinstance(size, bool) or size < 0:
                raise ResourceIntegrityError(f"Invalid size for {relative_path}")
            file_name = record.get("file_name")
            if not isinstance(file_name, str) or file_name != PurePosixPath(relative_path).name:
                raise ResourceIntegrityError(f"Invalid file_name for {relative_path}")
            media_type = record.get("media_type")
            if not isinstance(media_type, str) or not media_type:
                raise ResourceIntegrityError(f"Invalid media_type for {relative_path}")
            record["aliases"] = cls._string_list(record.get("aliases"), "aliases", relative_path)
            record["headings"] = cls._string_list(record.get("headings"), "headings", relative_path)
            record["semantic_markers"] = cls._string_list(
                record.get("semantic_markers"), "semantic_markers", relative_path
            )
            terminal_sentinel = record.get("terminal_sentinel")
            if terminal_sentinel is not None and not isinstance(terminal_sentinel, str):
                raise ResourceIntegrityError(f"Invalid terminal_sentinel for {relative_path}")
            if resource_id in seen_ids or relative_path in seen_paths:
                raise ResourceIntegrityError(f"Duplicate resource manifest identity: {relative_path}")
            seen_ids.add(resource_id)
            seen_paths.add(relative_path)
            record["relative_path"] = relative_path
            record["package_path"] = package_path
            records.append(record)

        declared_count = manifest.get("resource_count")
        if declared_count != len(records):
            raise ResourceIntegrityError(
                "Resource manifest count does not match entries",
                details={"declared": declared_count, "observed": len(records)},
            )
        observed_tree_digest = tree_digest_for_records(records)
        expected_tree_digest = f"sha256:{observed_tree_digest}"
        if declared_tree_digest != expected_tree_digest:
            raise ResourceIntegrityError(
                "Installed resource manifest aggregate source-tree digest does not match entries",
                details={"declared": declared_tree_digest, "observed": expected_tree_digest},
            )
        expected_resource_set = f"{release_line}+sha256.{observed_tree_digest[:12]}"
        if declared_resource_set != expected_resource_set:
            raise ResourceIntegrityError(
                "Installed resource manifest resource-set version does not match entries",
                details={"declared": declared_resource_set, "observed": expected_resource_set},
            )
        return records

    @classmethod
    def from_environment(
        cls,
        *,
        environment: Mapping[str, str] | None = None,
        paths: AppPaths | None = None,
    ) -> ResourceResolver:
        env = dict(os.environ if environment is None else environment)
        override = env.get("AIR_RESOURCE_ROOT")
        if override:
            root = Path(override).expanduser().resolve()
            if not all((root / name).is_dir() for name in CANONICAL_ROOTS):
                raise ResourceError(
                    "AIR_RESOURCE_ROOT must contain prompts, profiles, and runtime directories",
                    details={"resource_root": str(root)},
                )
            manifest = build_manifest(root, __version__)
            return cls(root, manifest, origin="EXPLICIT_SOURCE_OVERRIDE", paths=paths)

        root = importlib_resources.files("vm4ai_air").joinpath("resources", "air")
        manifest_node = root.joinpath(MANIFEST_NAME)
        try:
            text = manifest_node.read_text(encoding="utf-8")
        except (FileNotFoundError, ModuleNotFoundError, OSError) as exc:
            raise ResourceError(
                (
                    "Installed AIR resources are unavailable. Install the built wheel or set "
                    "AIR_RESOURCE_ROOT explicitly for development."
                ),
                details={"expected_manifest": MANIFEST_NAME},
            ) from exc
        manifest = strict_json_loads(text, source=MANIFEST_NAME)
        return cls(root, manifest, origin="INSTALLED_PACKAGE", paths=paths)

    @property
    def resource_set_version(self) -> str:
        return str(self.manifest["resource_set_version"])

    @property
    def source_tree_digest(self) -> str:
        return str(self.manifest["source_tree_digest"])

    def _node_for_record(self, record: Mapping[str, Any]) -> Any:
        node = self.root
        for part in str(record["package_path"]).split("/"):
            node = node.joinpath(part)
        return node

    def _read_bytes(self, record: Mapping[str, Any]) -> bytes:
        node = self._node_for_record(record)
        try:
            return node.read_bytes()
        except OSError as exc:
            raise ResourceError(
                f"Cannot read AIR resource {record['relative_path']}: {exc}",
                details={"resource_id": record["resource_id"]},
            ) from exc

    @staticmethod
    def _normalize_user_path(identifier: str) -> str:
        normalized = identifier.replace("\\", "/")
        raw_parts = normalized.split("/")
        path = PurePosixPath(normalized)
        if (
            path.is_absolute()
            or any(part in {"", ".", ".."} for part in raw_parts)
            or not path.parts
            or ":" in path.parts[0]
        ):
            raise ResourceError(f"Unsafe AIR resource identifier: {identifier}")
        return path.as_posix()

    def resolve(self, identifier: str) -> dict[str, Any]:
        if not isinstance(identifier, str) or not identifier.strip():
            raise ResourceError("AIR resource identifier must be a non-empty string")
        if identifier in self._by_id:
            return self._by_id[identifier]
        if "/" in identifier or "\\" in identifier or identifier.startswith("."):
            normalized = self._normalize_user_path(identifier)
            if normalized in self._by_path:
                return self._by_path[normalized]
        matches = []
        folded = identifier.casefold()
        for record in self._records:
            aliases = [str(item) for item in record.get("aliases", [])]
            if any(alias.casefold() == folded for alias in aliases):
                matches.append(record)
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ResourceError(
                f"AIR resource identifier is ambiguous: {identifier}",
                details={"matches": [item["relative_path"] for item in matches]},
            )
        raise ResourceError(f"Unknown AIR resource: {identifier}")

    def read_bytes(self, identifier: str) -> bytes:
        return self._read_bytes(self.resolve(identifier))

    def read_text(self, identifier: str, *, encoding: str = "utf-8") -> str:
        try:
            return self.read_bytes(identifier).decode(encoding)
        except UnicodeDecodeError as exc:
            raise ResourceError(f"AIR resource is not {encoding} text: {identifier}") from exc

    def list(self, *, prefix: str | None = None) -> list[dict[str, Any]]:
        records = self._records
        if prefix:
            folded = prefix.replace("\\", "/").casefold()
            records = [item for item in records if str(item["relative_path"]).casefold().startswith(folded)]
        return [dict(item) for item in records]

    def search(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        tokens = _TOKEN.findall(query.casefold())
        if not tokens:
            return []
        results: list[tuple[int, dict[str, Any]]] = []
        for record in self._records:
            path = str(record["relative_path"]).casefold()
            aliases = "\n".join(str(item).casefold() for item in record.get("aliases", []))
            headings = "\n".join(str(item).casefold() for item in record.get("headings", []))
            markers = "\n".join(str(item).casefold() for item in record.get("semantic_markers", []))
            score = 0
            for token in tokens:
                if token == path:
                    score += 100
                elif token in path:
                    score += 20
                if token in aliases:
                    score += 10
                if token in markers:
                    score += 8
                if token in headings:
                    score += 3
            if score:
                results.append((score, record))
        results.sort(key=lambda item: (-item[0], str(item[1]["relative_path"]).casefold()))
        return [{"score": score, **dict(record)} for score, record in results[:limit]]

    def verify(self, identifier: str) -> dict[str, Any]:
        record = self.resolve(identifier)
        data = self._read_bytes(record)
        observed = _sha256(data)
        size = len(data)
        passed = observed == record["sha256"] and size == record["size_bytes"]
        return {
            "resource_id": record["resource_id"],
            "relative_path": record["relative_path"],
            "expected_sha256": record["sha256"],
            "observed_sha256": observed,
            "expected_size_bytes": record["size_bytes"],
            "observed_size_bytes": size,
            "decision": "PASS" if passed else "FAIL",
        }

    def verify_all(self) -> dict[str, Any]:
        results = [self.verify(str(record["resource_id"])) for record in self._records]
        failed = [item for item in results if item["decision"] != "PASS"]
        return {
            "decision": "PASS" if not failed else "FAIL",
            "origin": self.origin,
            "resource_set_version": self.resource_set_version,
            "source_tree_digest": self.source_tree_digest,
            "resource_count": len(results),
            "failed_count": len(failed),
            "failures": failed,
            "claim_boundary": "Digest and size verification only; behavioural correctness remains separately tested.",
        }

    def materialize(self, identifier: str, *, purpose: str) -> dict[str, Any]:
        if not purpose.strip():
            raise ResourceError("Materialization requires a non-empty purpose")
        record = self.resolve(identifier)
        data = self._read_bytes(record)
        observed_digest = _sha256(data)
        observed_size = len(data)
        expected_digest = str(record["sha256"])
        expected_size = int(record["size_bytes"])
        if observed_digest != expected_digest or observed_size != expected_size:
            raise ResourceIntegrityError(
                f"Refusing to materialize corrupted AIR resource: {record['relative_path']}",
                details={
                    "expected_sha256": expected_digest,
                    "observed_sha256": observed_digest,
                    "expected_size_bytes": expected_size,
                    "observed_size_bytes": observed_size,
                },
            )

        target_dir = self.paths.materialized_resources_root / observed_digest
        target = target_dir / str(record["file_name"])
        receipt_path = target_dir / "materialization-receipt.json"
        target_dir.mkdir(parents=True, exist_ok=True)
        if not target.exists() or _sha256(target.read_bytes()) != observed_digest:
            atomic_write_bytes(target, data)
        if _sha256(target.read_bytes()) != observed_digest:
            raise ResourceIntegrityError(f"Materialized AIR resource digest mismatch: {target}")
        receipt = {
            "schema_id": "AIR_RESOURCE_MATERIALIZATION_RECEIPT",
            "schema_version": "1.0.0",
            "created_at_utc": utc_now(),
            "resource_id": record["resource_id"],
            "relative_path": record["relative_path"],
            "source_sha256": observed_digest,
            "package_version": self.manifest.get("package_version"),
            "resource_set_version": self.resource_set_version,
            "materialized_path": str(target),
            "purpose": purpose,
            "cleanup_policy": "CACHE_MANAGED",
        }
        atomic_write_json(receipt_path, receipt)
        return {"decision": "PASS", "path": str(target), "receipt": receipt}
