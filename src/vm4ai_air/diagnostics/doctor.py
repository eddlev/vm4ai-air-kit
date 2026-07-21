"""Read-only installation and workspace diagnostics."""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from vm4ai_air.config import ConfigManager
from vm4ai_air.errors import AirError
from vm4ai_air.paths import AppPaths
from vm4ai_air.resources import ResourceResolver
from vm4ai_air.version import base_version_payload
from vm4ai_air.workspace import WorkspaceManager


def _nearest_existing_parent(path: Path) -> Path:
    current = path
    while not current.exists() and current != current.parent:
        current = current.parent
    return current


def run_doctor(
    *,
    environment: Mapping[str, str] | None = None,
    verify_resources: bool = True,
) -> dict[str, Any]:
    env = dict(os.environ if environment is None else environment)
    paths = AppPaths.resolve(env)
    checks: list[dict[str, Any]] = []

    def add(name: str, status: str, detail: str, **extra: Any) -> None:
        checks.append({"name": name, "status": status, "detail": detail, **extra})

    version = base_version_payload()
    add("PACKAGE_IMPORT", "PASS", f"{version['distribution']} {version['package_version']}")

    for label, path in (
        ("CONFIG_ROOT", paths.config_root),
        ("DATA_ROOT", paths.data_root),
        ("STATE_ROOT", paths.state_root),
        ("CACHE_ROOT", paths.cache_root),
        ("LOG_ROOT", paths.log_root),
    ):
        if path.exists():
            is_directory = path.is_dir()
            writable = is_directory and os.access(path, os.W_OK)
            status = "PASS" if writable else "FAIL"
            if not is_directory:
                detail = f"exists but is not a directory: {path}"
            elif not writable:
                detail = f"directory is not writable: {path}"
            else:
                detail = str(path)
            add(label, status, detail, writable=writable)
        else:
            parent = _nearest_existing_parent(path)
            writable = parent.is_dir() and os.access(parent, os.W_OK)
            add(
                label,
                "PASS" if writable else "FAIL",
                f"not created yet; nearest existing parent: {parent}",
                will_create_on_first_mutation=writable,
            )

    config = ConfigManager(paths, environment=env).validate()
    add(
        "CONFIGURATION",
        "PASS" if config["decision"] == "PASS" else "FAIL",
        config["path"],
        result=config,
    )

    try:
        resolver = ResourceResolver.from_environment(environment=env, paths=paths)
        if resolver.origin == "EXPLICIT_SOURCE_OVERRIDE":
            add(
                "RESOURCE_ORIGIN",
                "WARN",
                "AIR_RESOURCE_ROOT development override is active; this is not installed-wheel evidence.",
            )
        else:
            add("RESOURCE_ORIGIN", "PASS", resolver.origin)
        if verify_resources:
            result = resolver.verify_all()
            add(
                "RESOURCE_SET",
                "PASS" if result["decision"] == "PASS" else "FAIL",
                resolver.resource_set_version,
                result=result,
            )
        version["resource_set_version"] = resolver.resource_set_version
        version["resource_origin"] = resolver.origin
    except AirError as exc:
        add("RESOURCE_SET", "FAIL", exc.message, error=exc.as_dict())
        version["resource_set_version"] = "UNAVAILABLE"
        version["resource_origin"] = "UNAVAILABLE"

    try:
        manager = WorkspaceManager(paths, environment=env)
        projects = manager.list_projects()
        add("PROJECT_REGISTRY", "PASS", f"{len(projects)} registered project(s)")
        if not paths.active_project_file.exists():
            add("ACTIVE_PROJECT", "PASS", "No active project selected")
        else:
            try:
                active = manager.show_project()
            except AirError as exc:
                add("ACTIVE_PROJECT", "FAIL", exc.message, error=exc.as_dict())
            else:
                validation = manager.validate_project(active["project"]["project_id"])
                add(
                    "ACTIVE_PROJECT",
                    "PASS" if validation["decision"] == "PASS" else "FAIL",
                    active["project"]["name"],
                    result=validation,
                )
    except AirError as exc:
        add("PROJECT_REGISTRY", "FAIL", exc.message, error=exc.as_dict())

    failed = [item for item in checks if item["status"] == "FAIL"]
    warned = [item for item in checks if item["status"] == "WARN"]
    decision = "FAIL" if failed else "WARN" if warned else "PASS"
    return {
        "decision": decision,
        "version": version,
        "paths": paths.as_dict(),
        "checks": checks,
        "failed_count": len(failed),
        "warning_count": len(warned),
        "claim_boundary": (
            "Doctor reports observed local state; it does not prove semantic correctness or release readiness."
        ),
    }
