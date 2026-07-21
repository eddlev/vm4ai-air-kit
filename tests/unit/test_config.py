from __future__ import annotations

from pathlib import Path

import pytest

from vm4ai_air.config import ConfigManager
from vm4ai_air.errors import ConfigurationError
from vm4ai_air.paths import AppPaths


def test_environment_overrides_user_config(tmp_path: Path) -> None:
    environment = {
        "AIR_HOME": str(tmp_path / "home"),
        "AIR_STRICT_RESOURCES": "false",
        "AIR_WORKSPACE_ROOT": str(tmp_path / "workspaces"),
    }
    paths = AppPaths.resolve(environment)
    paths.config_root.mkdir(parents=True)
    paths.config_file.write_text(
        """schema_version = 1

[application]
telemetry_enabled = false

[resources]
strict_verification = true

[workspace]
default_root = ""
""",
        encoding="utf-8",
    )
    config = ConfigManager(paths, environment=environment).load()
    assert config["resources"]["strict_verification"] is False
    assert config["workspace"]["default_root"] == str((tmp_path / "workspaces").resolve())


def test_telemetry_cannot_be_enabled(tmp_path: Path) -> None:
    environment = {"AIR_HOME": str(tmp_path / "home")}
    paths = AppPaths.resolve(environment)
    paths.config_root.mkdir(parents=True)
    paths.config_file.write_text(
        """schema_version = 1

[application]
telemetry_enabled = true
""",
        encoding="utf-8",
    )
    with pytest.raises(ConfigurationError):
        ConfigManager(paths, environment=environment).load()
