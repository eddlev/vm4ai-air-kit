from __future__ import annotations

import json
from pathlib import Path

import pytest

from vm4ai_air.errors import LockError
from vm4ai_air.io import FileLock, atomic_write_json, atomic_write_text


def test_atomic_write_replaces_content(tmp_path: Path) -> None:
    target = tmp_path / "state" / "value.txt"
    atomic_write_text(target, "first")
    atomic_write_text(target, "second")
    assert target.read_text(encoding="utf-8") == "second"
    assert not list(target.parent.glob("*.tmp"))


def test_atomic_json_is_valid(tmp_path: Path) -> None:
    target = tmp_path / "receipt.json"
    atomic_write_json(target, {"status": "PASS", "value": 7})
    assert json.loads(target.read_text(encoding="utf-8"))["value"] == 7


def test_lock_fails_closed_when_held(tmp_path: Path) -> None:
    lock_path = tmp_path / "registry.lock"
    with FileLock(lock_path, timeout=0.1, poll_interval=0.01, stale_after=60), pytest.raises(LockError):
        FileLock(lock_path, timeout=0.03, poll_interval=0.005, stale_after=60).acquire()


def test_atomic_replace_failure_preserves_previous_value(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "state.txt"
    target.write_text("original", encoding="utf-8")

    def fail_replace(source: object, destination: object) -> None:
        raise OSError("simulated replace failure")

    monkeypatch.setattr("vm4ai_air.io.atomic.os.replace", fail_replace)
    with pytest.raises(OSError, match="simulated replace failure"):
        atomic_write_text(target, "replacement")
    assert target.read_text(encoding="utf-8") == "original"
    assert not list(tmp_path.glob("*.tmp"))
