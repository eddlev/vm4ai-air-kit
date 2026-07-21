from __future__ import annotations

import os
from pathlib import Path

from vm4ai_air.paths import AppPaths
from vm4ai_air.workspace import WorkspaceManager


def manager_for(tmp_path: Path) -> WorkspaceManager:
    environment = {"AIR_HOME": str(tmp_path / "air-home")}
    return WorkspaceManager(AppPaths.resolve(environment), environment=environment)


def test_two_projects_are_isolated_and_selection_is_explicit(tmp_path: Path) -> None:
    manager = manager_for(tmp_path)
    first = manager.init_project("First Project", make_active=True)["project"]
    second = manager.init_project("Second Project")["project"]
    first_path = Path(first["workspace_path"])
    second_path = Path(second["workspace_path"])
    assert first_path != second_path
    assert not first_path.is_relative_to(second_path)
    assert not second_path.is_relative_to(first_path)
    assert manager.show_project()["project"]["project_id"] == first["project_id"]

    original = Path.cwd()
    try:
        os.chdir(second_path)
        assert manager.show_project()["project"]["project_id"] == first["project_id"]
    finally:
        os.chdir(original)

    manager.use_project(second["project_id"])
    assert manager.show_project()["project"]["project_id"] == second["project_id"]
    assert manager.validate_project(first["project_id"])["decision"] == "PASS"
    assert manager.validate_project(second["project_id"])["decision"] == "PASS"


def test_private_key_inside_workspace_fails_validation(tmp_path: Path) -> None:
    manager = manager_for(tmp_path)
    record = manager.init_project("Key Boundary")["project"]
    workspace = Path(record["workspace_path"])
    (workspace / "evidence" / "private.pem").write_text(
        "-----BEGIN ENCRYPTED PRIVATE KEY-----\nnot-a-real-key\n",
        encoding="utf-8",
    )
    result = manager.validate_project(record["project_id"])
    assert result["decision"] == "FAIL"
    key_check = next(item for item in result["checks"] if item["name"] == "PRIVATE_KEYS_OUTSIDE_WORKSPACE")
    assert key_check["status"] == "FAIL"


def test_failed_workspace_creation_leaves_no_registry_entry(tmp_path: Path) -> None:
    manager = manager_for(tmp_path)
    blocking_file = tmp_path / "not-a-directory"
    blocking_file.write_text("block", encoding="utf-8")
    invalid_workspace = blocking_file / "project"
    try:
        manager.init_project("Cannot Create", workspace_path=str(invalid_workspace))
    except Exception as exc:
        assert "Cannot prepare AIR workspace location" in str(exc)
    else:
        raise AssertionError("Workspace creation unexpectedly succeeded")
    assert manager.list_projects() == []
