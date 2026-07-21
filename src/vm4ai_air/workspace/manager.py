"""Create, register, select, and validate isolated AIR project workspaces."""

from __future__ import annotations

import json
import os
import re
import shutil
import tomllib
import uuid
from collections.abc import Mapping
from contextlib import nullcontext
from pathlib import Path
from typing import Any

from vm4ai_air.config import ConfigManager
from vm4ai_air.config.toml_codec import dumps as dump_toml
from vm4ai_air.errors import WorkspaceError
from vm4ai_air.io import FileLock, atomic_write_bytes, atomic_write_json, atomic_write_text, utc_now
from vm4ai_air.paths import AppPaths
from vm4ai_air.version import __version__
from vm4ai_air.workspace.models import (
    REGISTRY_SCHEMA_VERSION,
    REQUIRED_DIRECTORIES,
    WORKSPACE_SCHEMA_VERSION,
    empty_registry,
    empty_trust_store,
)

_SLUG_INVALID = re.compile(r"[^a-z0-9]+")
_PRIVATE_KEY_MARKERS = (
    b"-----BEGIN PRIVATE KEY-----",
    b"-----BEGIN ENCRYPTED PRIVATE KEY-----",
    b"-----BEGIN OPENSSH PRIVATE KEY-----",
    b"-----BEGIN RSA PRIVATE KEY-----",
    b"-----BEGIN EC PRIVATE KEY-----",
)
_PRIVATE_FILE_NAMES = re.compile(r"(^|[-_.])private([-_.]|$)|\.key$|^id_ed25519$", re.IGNORECASE)


def _slugify(value: str) -> str:
    slug = _SLUG_INVALID.sub("-", value.strip().casefold()).strip("-")
    return slug or "air-project"


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _paths_overlap(first: Path, second: Path) -> bool:
    return first == second or _is_relative_to(first, second) or _is_relative_to(second, first)


class WorkspaceManager:
    def __init__(
        self,
        paths: AppPaths | None = None,
        *,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        self.environment = dict(os.environ if environment is None else environment)
        self.paths = paths or AppPaths.resolve(self.environment)
        self.config = ConfigManager(self.paths, environment=self.environment).load()

    def _registry_lock(self) -> FileLock:
        return FileLock(self.paths.registry_file.with_suffix(".lock"))

    def _active_project_lock(self) -> FileLock:
        return FileLock(self.paths.active_project_file.with_suffix(".lock"))

    def _read_registry(self) -> dict[str, Any]:
        if not self.paths.registry_file.exists():
            return empty_registry()
        try:
            value = json.loads(self.paths.registry_file.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise WorkspaceError(f"Cannot read AIR project registry: {exc}") from exc
        if not isinstance(value, dict) or value.get("schema_version") != REGISTRY_SCHEMA_VERSION:
            raise WorkspaceError("AIR project registry schema is unsupported")
        projects = value.get("projects")
        if not isinstance(projects, list):
            raise WorkspaceError("AIR project registry projects must be an array")
        return value

    def _workspace_root(self) -> Path:
        configured = str(self.config["workspace"]["default_root"] or "").strip()
        return Path(configured).expanduser().resolve() if configured else self.paths.projects_root

    @staticmethod
    def _snapshot_file(path: Path) -> tuple[bool, bytes | None]:
        if not path.exists():
            return False, None
        return True, path.read_bytes()

    @staticmethod
    def _restore_file(path: Path, snapshot: tuple[bool, bytes | None]) -> None:
        existed, data = snapshot
        if existed:
            if data is None:
                raise OSError(f"Missing rollback bytes for {path}")
            atomic_write_bytes(path, data)
        else:
            path.unlink(missing_ok=True)

    def _receipt_document(
        self,
        operation: str,
        *,
        project_id: str | None,
        details: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "operation_id": str(uuid.uuid4()),
            "operation": operation,
            "status": "PASS",
            "created_at_utc": utc_now(),
            "package_version": __version__,
            "project_id": project_id,
            "details": details,
            "claim_boundary": (
                "A local operation receipt records observed tool activity; it is not general authorization."
            ),
        }

    def _receipt_paths(self, receipt: Mapping[str, Any], workspace: Path | None) -> list[Path]:
        operation_id = str(receipt["operation_id"])
        paths = [self.paths.operations_root / f"{operation_id}.json"]
        if workspace is not None:
            paths.insert(0, workspace / "logs" / "operations" / f"{operation_id}.json")
        return paths

    def _remove_receipt_files(self, receipt: Mapping[str, Any], workspace: Path | None) -> None:
        for path in self._receipt_paths(receipt, workspace):
            path.unlink(missing_ok=True)

    def _write_receipt_files(self, receipt: dict[str, Any], workspace: Path | None) -> None:
        written: list[Path] = []
        try:
            for path in self._receipt_paths(receipt, workspace):
                atomic_write_json(path, receipt)
                written.append(path)
        except Exception:
            for path in written:
                path.unlink(missing_ok=True)
            raise

    @staticmethod
    def _raise_transaction_failure(
        action: str,
        exc: Exception,
        rollback_errors: list[str],
    ) -> None:
        details: dict[str, Any] = {"cause": str(exc)}
        if rollback_errors:
            details["rollback_errors"] = rollback_errors
        message = f"{action} failed"
        if rollback_errors:
            message += "; rollback was incomplete"
        else:
            message += " and was rolled back"
        raise WorkspaceError(message, details=details) from exc

    def _project_document(
        self,
        *,
        project_id: str,
        name: str,
        slug: str,
        created_at: str,
        source_path: str | None,
    ) -> dict[str, Any]:
        return {
            "schema_version": WORKSPACE_SCHEMA_VERSION,
            "project": {
                "id": project_id,
                "name": name,
                "slug": slug,
                "created_at_utc": created_at,
                "source_path": source_path or "",
            },
        }

    def _create_workspace_tree(self, root: Path, document: dict[str, Any]) -> None:
        root.mkdir(parents=True, exist_ok=False)
        for relative in REQUIRED_DIRECTORIES:
            (root / relative).mkdir(parents=True, exist_ok=False)
        atomic_write_text(root / "air-project.toml", dump_toml(document))
        atomic_write_json(root / "trust" / "trust-store.json", empty_trust_store())
        atomic_write_json(
            root / "state" / "project.json",
            {
                "schema_version": 1,
                "project_id": document["project"]["id"],
                "current_active_step": None,
                "status": "INITIALIZED",
            },
        )

    def init_project(
        self,
        name: str,
        *,
        workspace_path: str | None = None,
        source_path: str | None = None,
        make_active: bool = False,
    ) -> dict[str, Any]:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise WorkspaceError("Project name cannot be empty")
        project_id = str(uuid.uuid4())
        slug = _slugify(cleaned_name)
        created_at = utc_now()
        source = str(Path(source_path).expanduser().resolve()) if source_path else None
        default_root = self._workspace_root()
        workspace = (
            Path(workspace_path).expanduser().resolve()
            if workspace_path
            else (default_root / f"{slug}-{project_id[:8]}").resolve()
        )
        keystore = self.paths.keystore_root.resolve()
        if _paths_overlap(workspace, keystore):
            raise WorkspaceError("Project workspace may not overlap the AIR private keystore")

        try:
            self.paths.ensure_base_directories()
            workspace.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise WorkspaceError(f"Cannot prepare AIR workspace location {workspace}: {exc}") from exc

        staging = workspace.parent / f".{workspace.name}.creating-{uuid.uuid4().hex}"
        document = self._project_document(
            project_id=project_id,
            name=cleaned_name,
            slug=slug,
            created_at=created_at,
            source_path=source,
        )
        record = {
            "project_id": project_id,
            "name": cleaned_name,
            "slug": slug,
            "workspace_path": str(workspace),
            "source_path": source,
            "created_at_utc": created_at,
            "status": "ACTIVE",
        }
        receipt = self._receipt_document(
            "PROJECT_INIT",
            project_id=project_id,
            details={
                "name": cleaned_name,
                "workspace_path": str(workspace),
                "source_path": source,
                "made_active": make_active,
            },
        )

        with self._registry_lock(), (self._active_project_lock() if make_active else nullcontext()):
            registry = self._read_registry()
            for existing_record in registry["projects"]:
                registered_path = Path(existing_record["workspace_path"]).expanduser().resolve()
                if _paths_overlap(workspace, registered_path):
                    raise WorkspaceError(
                        "Project workspace overlaps an existing registered workspace",
                        details={
                            "existing_project_id": existing_record["project_id"],
                            "existing_path": str(registered_path),
                        },
                    )
                if str(existing_record["name"]).casefold() == cleaned_name.casefold():
                    raise WorkspaceError(
                        "A project with this name is already registered",
                        details={"existing_project_id": existing_record["project_id"]},
                    )
            if workspace.exists():
                raise WorkspaceError(f"Workspace already exists: {workspace}")

            try:
                registry_snapshot = self._snapshot_file(self.paths.registry_file)
                active_snapshot = self._snapshot_file(self.paths.active_project_file) if make_active else None
            except OSError as exc:
                raise WorkspaceError(f"Cannot snapshot AIR state before project creation: {exc}") from exc

            moved = False
            try:
                self._create_workspace_tree(staging, document)
                os.replace(staging, workspace)
                moved = True
                registry["projects"].append(record)
                registry["projects"].sort(key=lambda item: str(item["name"]).casefold())
                atomic_write_json(self.paths.registry_file, registry)
                if make_active:
                    atomic_write_json(
                        self.paths.active_project_file,
                        {
                            "schema_version": 1,
                            "project_id": project_id,
                            "selected_at_utc": utc_now(),
                            "selection_source": "PROJECT_INIT_USE",
                        },
                    )
                self._write_receipt_files(receipt, workspace)
            except Exception as exc:
                rollback_errors: list[str] = []
                if staging.exists():
                    shutil.rmtree(staging, ignore_errors=True)
                try:
                    self._remove_receipt_files(receipt, workspace if moved else None)
                except OSError as rollback_exc:
                    rollback_errors.append(f"receipt cleanup: {rollback_exc}")
                if make_active and active_snapshot is not None:
                    try:
                        self._restore_file(self.paths.active_project_file, active_snapshot)
                    except OSError as rollback_exc:
                        rollback_errors.append(f"active project state: {rollback_exc}")
                try:
                    self._restore_file(self.paths.registry_file, registry_snapshot)
                except OSError as rollback_exc:
                    rollback_errors.append(f"project registry: {rollback_exc}")
                if moved and workspace.exists():
                    try:
                        shutil.rmtree(workspace)
                    except OSError as rollback_exc:
                        rollback_errors.append(f"workspace removal: {rollback_exc}")
                self._raise_transaction_failure("AIR project creation", exc, rollback_errors)

        return {"decision": "PASS", "project": record, "receipt": receipt}

    def list_projects(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self._read_registry()["projects"]]

    def _active_project_id(self) -> str | None:
        if not self.paths.active_project_file.exists():
            return None
        try:
            value = json.loads(self.paths.active_project_file.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise WorkspaceError(f"Cannot read active project state: {exc}") from exc
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise WorkspaceError("Active project state schema is unsupported")
        project_id = value.get("project_id")
        if not isinstance(project_id, str) or not project_id.strip():
            raise WorkspaceError("Active project state has no valid project_id")
        return project_id

    def resolve_project(self, identifier: str | None = None) -> dict[str, Any]:
        requested = identifier or self._active_project_id()
        if not requested:
            raise WorkspaceError("No project identifier was supplied and no active project is selected")
        folded = requested.casefold()
        matches = []
        for record in self.list_projects():
            if record["project_id"] == requested:
                return record
            if (
                record["project_id"].startswith(requested)
                or str(record["name"]).casefold() == folded
                or str(record["slug"]).casefold() == folded
            ):
                matches.append(record)
        unique = {item["project_id"]: item for item in matches}
        if len(unique) == 1:
            return next(iter(unique.values()))
        if len(unique) > 1:
            raise WorkspaceError(
                f"Project identifier is ambiguous: {requested}",
                details={"matches": list(unique)},
            )
        raise WorkspaceError(f"Unknown AIR project: {requested}")

    def show_project(self, identifier: str | None = None) -> dict[str, Any]:
        record = self.resolve_project(identifier)
        return {
            "decision": "PASS",
            "active": record["project_id"] == self._active_project_id(),
            "project": record,
        }

    def use_project(self, identifier: str) -> dict[str, Any]:
        record = self.resolve_project(identifier)
        workspace = Path(record["workspace_path"]).expanduser().resolve()
        if not workspace.is_dir():
            raise WorkspaceError(f"Cannot select AIR project; workspace is unavailable: {workspace}")
        receipt = self._receipt_document(
            "PROJECT_USE",
            project_id=record["project_id"],
            details={"workspace_path": record["workspace_path"]},
        )
        try:
            self.paths.state_root.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise WorkspaceError(f"Cannot prepare AIR active project state: {exc}") from exc

        with self._active_project_lock():
            try:
                active_snapshot = self._snapshot_file(self.paths.active_project_file)
            except OSError as exc:
                raise WorkspaceError(f"Cannot snapshot active project state: {exc}") from exc
            try:
                atomic_write_json(
                    self.paths.active_project_file,
                    {
                        "schema_version": 1,
                        "project_id": record["project_id"],
                        "selected_at_utc": utc_now(),
                        "selection_source": "EXPLICIT_COMMAND",
                    },
                )
                self._write_receipt_files(receipt, workspace)
            except Exception as exc:
                rollback_errors: list[str] = []
                try:
                    self._remove_receipt_files(receipt, workspace)
                except OSError as rollback_exc:
                    rollback_errors.append(f"receipt cleanup: {rollback_exc}")
                try:
                    self._restore_file(self.paths.active_project_file, active_snapshot)
                except OSError as rollback_exc:
                    rollback_errors.append(f"active project state: {rollback_exc}")
                self._raise_transaction_failure("AIR project selection", exc, rollback_errors)
        return {"decision": "PASS", "project": record, "receipt": receipt}

    def _read_project_document(self, workspace: Path) -> dict[str, Any]:
        path = workspace / "air-project.toml"
        try:
            with path.open("rb") as handle:
                value = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise WorkspaceError(f"Cannot read project configuration {path}: {exc}") from exc
        if not isinstance(value, dict):
            raise WorkspaceError(f"Project configuration must be a TOML table: {path}")
        return value

    def _private_key_findings(self, workspace: Path) -> list[str]:
        findings: list[str] = []
        for path in workspace.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(workspace).as_posix()
            if _PRIVATE_FILE_NAMES.search(path.name):
                findings.append(relative)
                continue
            try:
                data = path.read_bytes()[:8192]
            except OSError:
                continue
            if any(marker in data for marker in _PRIVATE_KEY_MARKERS):
                findings.append(relative)
        return sorted(set(findings))

    def validate_project(self, identifier: str | None = None) -> dict[str, Any]:
        record = self.resolve_project(identifier)
        workspace = Path(record["workspace_path"]).expanduser().resolve()
        checks: list[dict[str, Any]] = []

        def check(name: str, passed: bool, detail: str) -> None:
            checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

        check("WORKSPACE_EXISTS", workspace.is_dir(), str(workspace))
        if not workspace.is_dir():
            return {"decision": "FAIL", "project": record, "checks": checks}

        try:
            document = self._read_project_document(workspace)
            project = document.get("project", {}) if isinstance(document, dict) else {}
            check("PROJECT_CONFIG_SCHEMA", document.get("schema_version") == WORKSPACE_SCHEMA_VERSION, "schema_version")
            check("PROJECT_ID_MATCH", project.get("id") == record["project_id"], str(project.get("id")))
            check("PROJECT_NAME_MATCH", project.get("name") == record["name"], str(project.get("name")))
        except WorkspaceError as exc:
            check("PROJECT_CONFIG_READABLE", False, exc.message)

        for relative in REQUIRED_DIRECTORIES:
            path = workspace / relative
            check(f"DIRECTORY_{relative.replace('/', '_').upper()}", path.is_dir(), relative)
            if path.exists():
                check(
                    f"NO_SYMLINK_ESCAPE_{relative.replace('/', '_').upper()}",
                    not path.is_symlink() and _is_relative_to(path.resolve(), workspace),
                    str(path),
                )

        private_keys = self._private_key_findings(workspace)
        check(
            "PRIVATE_KEYS_OUTSIDE_WORKSPACE",
            not private_keys,
            "none found" if not private_keys else ", ".join(private_keys),
        )
        failed = [item for item in checks if item["status"] == "FAIL"]
        return {
            "decision": "PASS" if not failed else "FAIL",
            "project": record,
            "workspace_path": str(workspace),
            "checks": checks,
            "failed_count": len(failed),
            "claim_boundary": (
                "Workspace validation checks local structure and boundaries, not project correctness or authorization."
            ),
        }
