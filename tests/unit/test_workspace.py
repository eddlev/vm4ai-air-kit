from __future__ import annotations

import os
from pathlib import Path

import pytest

from vm4ai_air.errors import WorkspaceError
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


def test_public_key_in_public_key_directory_is_allowed(tmp_path: Path) -> None:
    manager = manager_for(tmp_path)
    record = manager.init_project("Public Key Allowed")["project"]
    workspace = Path(record["workspace_path"])
    (workspace / "trust" / "public-keys" / "signer.pub.pem").write_text(
        "-----BEGIN PUBLIC KEY-----\nnot-a-real-public-key\n",
        encoding="utf-8",
    )
    assert manager.validate_project(record["project_id"])["decision"] == "PASS"


def test_private_key_in_public_key_directory_fails_validation(tmp_path: Path) -> None:
    manager = manager_for(tmp_path)
    record = manager.init_project("Public Key Boundary")["project"]
    workspace = Path(record["workspace_path"])
    (workspace / "trust" / "public-keys" / "deceptive-public.pem").write_text(
        "-----BEGIN PRIVATE KEY-----\nnot-a-real-key\n",
        encoding="utf-8",
    )
    result = manager.validate_project(record["project_id"])
    assert result["decision"] == "FAIL"
    key_check = next(item for item in result["checks"] if item["name"] == "PRIVATE_KEYS_OUTSIDE_WORKSPACE")
    assert "trust/public-keys/deceptive-public.pem" in key_check["detail"]


def test_failed_workspace_creation_leaves_no_registry_entry(tmp_path: Path) -> None:
    manager = manager_for(tmp_path)
    blocking_file = tmp_path / "not-a-directory"
    blocking_file.write_text("block", encoding="utf-8")
    invalid_workspace = blocking_file / "project"
    with pytest.raises(WorkspaceError, match="Cannot prepare AIR workspace location"):
        manager.init_project("Cannot Create", workspace_path=str(invalid_workspace))
    assert manager.list_projects() == []


def test_receipt_failure_rolls_back_project_creation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manager = manager_for(tmp_path)
    workspace = tmp_path / "transactional-project"

    def fail_receipt(_receipt: dict[str, object], _workspace: Path | None) -> None:
        raise OSError("injected receipt failure")

    monkeypatch.setattr(manager, "_write_receipt_files", fail_receipt)
    with pytest.raises(WorkspaceError, match="rolled back"):
        manager.init_project("Transactional Project", workspace_path=str(workspace), make_active=True)

    assert manager.list_projects() == []
    assert not workspace.exists()
    assert not manager.paths.active_project_file.exists()
    assert list(manager.paths.operations_root.glob("*.json")) == []


def test_receipt_failure_rolls_back_active_project_selection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manager = manager_for(tmp_path)
    first = manager.init_project("First Active", make_active=True)["project"]
    second = manager.init_project("Second Active")["project"]
    receipts_before = set(manager.paths.operations_root.glob("*.json"))

    def fail_receipt(_receipt: dict[str, object], _workspace: Path | None) -> None:
        raise OSError("injected receipt failure")

    monkeypatch.setattr(manager, "_write_receipt_files", fail_receipt)
    with pytest.raises(WorkspaceError, match="rolled back"):
        manager.use_project(second["project_id"])

    assert manager.show_project()["project"]["project_id"] == first["project_id"]
    assert set(manager.paths.operations_root.glob("*.json")) == receipts_before
