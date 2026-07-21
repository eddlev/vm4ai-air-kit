"""Platform-aware AIR application paths."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from platformdirs import PlatformDirs


@dataclass(frozen=True)
class AppPaths:
    config_root: Path
    data_root: Path
    state_root: Path
    cache_root: Path
    log_root: Path

    @classmethod
    def resolve(cls, environment: Mapping[str, str] | None = None) -> AppPaths:
        env = dict(os.environ if environment is None else environment)
        home_override = env.get("AIR_HOME")
        if home_override:
            base = Path(home_override).expanduser().resolve()
            defaults = {
                "config_root": base / "config",
                "data_root": base / "data",
                "state_root": base / "state",
                "cache_root": base / "cache",
                "log_root": base / "logs",
            }
        else:
            dirs = PlatformDirs(appname="AIR", appauthor="VM4AI", roaming=False, ensure_exists=False)
            defaults = {
                "config_root": Path(dirs.user_config_dir),
                "data_root": Path(dirs.user_data_dir),
                "state_root": Path(dirs.user_state_dir),
                "cache_root": Path(dirs.user_cache_dir),
                "log_root": Path(dirs.user_log_dir),
            }

        overrides = {
            "config_root": env.get("AIR_CONFIG_HOME"),
            "data_root": env.get("AIR_DATA_HOME"),
            "state_root": env.get("AIR_STATE_HOME"),
            "cache_root": env.get("AIR_CACHE_HOME"),
            "log_root": env.get("AIR_LOG_HOME"),
        }
        resolved: dict[str, Path] = {}
        for key, default in defaults.items():
            value = overrides[key]
            resolved[key] = Path(value).expanduser().resolve() if value else default.expanduser().resolve()
        return cls(**resolved)

    @property
    def config_file(self) -> Path:
        return self.config_root / "config.toml"

    @property
    def registry_file(self) -> Path:
        return self.data_root / "registry.json"

    @property
    def projects_root(self) -> Path:
        return self.data_root / "projects"

    @property
    def keystore_root(self) -> Path:
        return self.data_root / "keystore"

    @property
    def trust_root(self) -> Path:
        return self.data_root / "trust"

    @property
    def migrations_root(self) -> Path:
        return self.data_root / "migrations"

    @property
    def active_project_file(self) -> Path:
        return self.state_root / "active-project.json"

    @property
    def operations_root(self) -> Path:
        return self.state_root / "operations"

    @property
    def materialized_resources_root(self) -> Path:
        return self.cache_root / "materialized-resources"

    def ensure_base_directories(self) -> None:
        for path in (
            self.config_root,
            self.data_root,
            self.state_root,
            self.cache_root,
            self.log_root,
            self.projects_root,
            self.keystore_root,
            self.trust_root,
            self.migrations_root,
            self.operations_root,
        ):
            path.mkdir(parents=True, exist_ok=True)

    def as_dict(self) -> dict[str, str]:
        return {
            "config_root": str(self.config_root),
            "config_file": str(self.config_file),
            "data_root": str(self.data_root),
            "projects_root": str(self.projects_root),
            "keystore_root": str(self.keystore_root),
            "state_root": str(self.state_root),
            "active_project_file": str(self.active_project_file),
            "cache_root": str(self.cache_root),
            "materialized_resources_root": str(self.materialized_resources_root),
            "log_root": str(self.log_root),
        }
