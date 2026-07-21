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
from vm4ai_air.resources.build import MANIFEST_NAME, build_manifest, strict_json_loads
from vm4ai_air.version import __version__

_TOKEN = re.compile(r"[a-z0-9_./:-]+")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_CANONICAL_ROOTS = {"prompts", "profiles", "runtime"}


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
        path = PurePosixPath(normalized)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ResourceIntegrityError(f"Unsafe resource manifest path in {field}: {value}")
        if path.parts[0] not in _CANONICAL_ROOTS:
            raise ResourceIntegrityError(f"Resource manifest path is outside canonical roots: {value}")
        return path.as_posix()

    @classmethod
    def _validate_manifest(cls, manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
        if manifest.get("schema_id") != "AIR_INSTALLED_RESOURCE_MANIFEST":
            raise ResourceIntegrityError("Installed resource manifest schema_id is invalid")
        if manifest.get("package_version") != __version__:
            raise ResourceIntegrityError(
                "Installed resource manifest package version does not match application code",
                details={"manifest": manifest.get("package_version"), "application": __version__},
            )
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
            resource_id = record.get("resource_id")
            if not isinstance(resource_id, str) or not resource_id.startswith("air://"):
                raise ResourceIntegrityError("Resource manifest entry has an invalid resource_id")
            relative_path = cls._safe_relative_path(record.get("relative_path"), "relative_path")
            package_path = cls._safe_relative_path(record.get("package_path"), "package_path")
            if relative_path != package_path:
                raise ResourceIntegrityError(
                    "Stage 2 resource manifest requires relative_path and package_path to match",
                    details={"relative_path": relative_path, "package_path": package_path},
                )
            digest = record.get("sha256")
            size = record.get("size_bytes")
            if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
                raise ResourceIntegrityError(f"Invalid SHA-256 digest for {relative_path}")
            if not isinstance(size, int) or isinstance(size, bool) or size < 0:
                raise ResourceIntegrityError(f"Invalid size for {relative_path}")
            file_name = record.get("file_name")
            if not isinstance(file_name, str) or file_name != PurePosixPath(file_name).name:
                raise ResourceIntegrityError(f"Invalid file_name for {relative_path}")
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
            if not all((root / name).is_dir() for name in ("prompts", "profiles", "runtime")):
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
        return str(self.manifest.get("resource_set_version", "UNKNOWN"))

    @property
    def source_tree_digest(self) -> str:
        return str(self.manifest.get("source_tree_digest", "UNKNOWN"))

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

    def resolve(self, identifier: str) -> dict[str, Any]:
        if identifier in self._by_id:
            return self._by_id[identifier]
        normalized = identifier.replace("\\", "/").lstrip("./")
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
        digest = str(record["sha256"])
        target_dir = self.paths.materialized_resources_root / digest
        target = target_dir / str(record["file_name"])
        receipt_path = target_dir / "materialization-receipt.json"
        target_dir.mkdir(parents=True, exist_ok=True)
        if not target.exists() or _sha256(target.read_bytes()) != digest:
            atomic_write_bytes(target, data)
        receipt = {
            "schema_id": "AIR_RESOURCE_MATERIALIZATION_RECEIPT",
            "schema_version": "1.0.0",
            "created_at_utc": utc_now(),
            "resource_id": record["resource_id"],
            "relative_path": record["relative_path"],
            "source_sha256": digest,
            "package_version": self.manifest.get("package_version"),
            "resource_set_version": self.resource_set_version,
            "materialized_path": str(target),
            "purpose": purpose,
            "cleanup_policy": "CACHE_MANAGED",
        }
        atomic_write_json(receipt_path, receipt)
        return {"decision": "PASS", "path": str(target), "receipt": receipt}
