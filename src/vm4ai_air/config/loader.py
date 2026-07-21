"""Versioned AIR configuration with explicit precedence."""

from __future__ import annotations

import os
import tomllib
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from vm4ai_air.config.toml_codec import dumps as dump_toml
from vm4ai_air.errors import ConfigurationError
from vm4ai_air.io import atomic_write_text
from vm4ai_air.paths import AppPaths

CONFIG_SCHEMA_VERSION = 1

DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": CONFIG_SCHEMA_VERSION,
    "application": {
        "telemetry_enabled": False,
    },
    "workspace": {
        "default_root": "",
    },
}

_ALLOWED_KEYS = {
    "schema_version": None,
    "application": {"telemetry_enabled"},
    "workspace": {"default_root"},
}


def _deep_merge(base: dict[str, Any], overlay: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, Mapping) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def environment_overlay(environment: Mapping[str, str]) -> dict[str, Any]:
    overlay: dict[str, Any] = {}
    if "AIR_WORKSPACE_ROOT" in environment:
        overlay.setdefault("workspace", {})["default_root"] = environment["AIR_WORKSPACE_ROOT"]
    return overlay


def validate_config(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if value.get("schema_version") != CONFIG_SCHEMA_VERSION:
        errors.append(f"schema_version must be {CONFIG_SCHEMA_VERSION}; found {value.get('schema_version')!r}")
    for key in value:
        if key not in _ALLOWED_KEYS:
            errors.append(f"unknown top-level configuration key: {key}")
    for section, allowed in _ALLOWED_KEYS.items():
        if allowed is None or section not in value:
            continue
        section_value = value[section]
        if not isinstance(section_value, Mapping):
            errors.append(f"{section} must be a table")
            continue
        for key in section_value:
            if key not in allowed:
                errors.append(f"unknown configuration key: {section}.{key}")
    application = value.get("application", {})
    if isinstance(application, Mapping) and application.get("telemetry_enabled") is not False:
        errors.append("application.telemetry_enabled must remain false; AIR has no telemetry path")
    workspace = value.get("workspace", {})
    if isinstance(workspace, Mapping):
        default_root = workspace.get("default_root", "")
        if not isinstance(default_root, str):
            errors.append("workspace.default_root must be a string")
    return errors


class ConfigManager:
    def __init__(
        self,
        paths: AppPaths | None = None,
        *,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        self.environment = dict(os.environ if environment is None else environment)
        self.paths = paths or AppPaths.resolve(self.environment)

    def read_user_config(self) -> dict[str, Any]:
        path = self.paths.config_file
        if not path.exists():
            return {}
        try:
            with path.open("rb") as handle:
                value = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise ConfigurationError(f"Cannot read AIR configuration {path}: {exc}") from exc
        if not isinstance(value, dict):
            raise ConfigurationError(f"AIR configuration must be a TOML table: {path}")
        return value

    def load(self, *, cli_overlay: Mapping[str, Any] | None = None) -> dict[str, Any]:
        value = _deep_merge(DEFAULT_CONFIG, self.read_user_config())
        value = _deep_merge(value, environment_overlay(self.environment))
        if cli_overlay:
            value = _deep_merge(value, cli_overlay)
        errors = validate_config(value)
        if errors:
            raise ConfigurationError("AIR configuration is invalid", details={"errors": errors})
        workspace_root = value["workspace"]["default_root"]
        if workspace_root:
            value["workspace"]["default_root"] = str(Path(workspace_root).expanduser().resolve())
        return value

    def validate(self) -> dict[str, Any]:
        try:
            value = self.load()
        except ConfigurationError as exc:
            return {
                "decision": "FAIL",
                "path": str(self.paths.config_file),
                "errors": exc.details.get("errors", [exc.message]),
            }
        return {
            "decision": "PASS",
            "path": str(self.paths.config_file),
            "exists": self.paths.config_file.exists(),
            "configuration": value,
        }

    def write_default(self, *, overwrite: bool = False) -> Path:
        path = self.paths.config_file
        if path.exists() and not overwrite:
            raise ConfigurationError(f"Configuration already exists: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(path, dump_toml(DEFAULT_CONFIG))
        return path
