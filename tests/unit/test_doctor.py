from __future__ import annotations

import os
from pathlib import Path

import pytest

import vm4ai_air.diagnostics.doctor as doctor_module
from vm4ai_air.diagnostics import run_doctor
from vm4ai_air.paths import AppPaths
from vm4ai_air.workspace import WorkspaceManager

ROOT = Path(__file__).resolve().parents[2]


def test_corrupt_active_project_state_fails_doctor(tmp_path: Path) -> None:
    environment = {"AIR_HOME": str(tmp_path / "air-home"), "AIR_RESOURCE_ROOT": str(ROOT)}
    paths = AppPaths.resolve(environment)
    manager = WorkspaceManager(paths, environment=environment)
    manager.init_project("Doctor Project")
    paths.active_project_file.parent.mkdir(parents=True, exist_ok=True)
    paths.active_project_file.write_text("{not-json", encoding="utf-8")

    result = run_doctor(environment=environment, verify_resources=False)
    active = next(item for item in result["checks"] if item["name"] == "ACTIVE_PROJECT")
    assert result["decision"] == "FAIL"
    assert active["status"] == "FAIL"
    assert "Cannot read active project state" in active["detail"]


def test_existing_unwritable_root_fails_doctor(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    environment = {"AIR_HOME": str(tmp_path / "air-home"), "AIR_RESOURCE_ROOT": str(ROOT)}
    paths = AppPaths.resolve(environment)
    paths.ensure_base_directories()
    real_access = os.access

    def fake_access(path: os.PathLike[str] | str, mode: int) -> bool:
        if Path(path) == paths.state_root and mode == os.W_OK:
            return False
        return real_access(path, mode)

    monkeypatch.setattr(doctor_module.os, "access", fake_access)
    result = run_doctor(environment=environment, verify_resources=False)
    state = next(item for item in result["checks"] if item["name"] == "STATE_ROOT")
    assert result["decision"] == "FAIL"
    assert state["status"] == "FAIL"
    assert "not writable" in state["detail"]
