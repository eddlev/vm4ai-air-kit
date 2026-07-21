from __future__ import annotations

from pathlib import Path

from vm4ai_air.paths import AppPaths


def test_air_home_produces_separate_roots(tmp_path: Path) -> None:
    paths = AppPaths.resolve({"AIR_HOME": str(tmp_path / "air")})
    assert paths.config_root == (tmp_path / "air" / "config").resolve()
    assert paths.data_root == (tmp_path / "air" / "data").resolve()
    assert paths.state_root == (tmp_path / "air" / "state").resolve()
    assert paths.cache_root == (tmp_path / "air" / "cache").resolve()
    assert paths.log_root == (tmp_path / "air" / "logs").resolve()
    assert paths.keystore_root != paths.projects_root


def test_individual_override_wins(tmp_path: Path) -> None:
    paths = AppPaths.resolve(
        {
            "AIR_HOME": str(tmp_path / "air"),
            "AIR_DATA_HOME": str(tmp_path / "custom-data"),
        }
    )
    assert paths.data_root == (tmp_path / "custom-data").resolve()
