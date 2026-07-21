"""Cross-platform atomic writes and cooperative lock files."""

from __future__ import annotations

import json
import os
import socket
import tempfile
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from vm4ai_air.errors import LockError


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_write_bytes(path: os.PathLike[str] | str, data: bytes, *, mode: int | None = None) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temporary = Path(temporary_name)
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, target)
        _fsync_directory(target.parent)
        return target
    finally:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)


def atomic_write_text(
    path: os.PathLike[str] | str,
    text: str,
    *,
    encoding: str = "utf-8",
    mode: int | None = None,
) -> Path:
    return atomic_write_bytes(path, text.encode(encoding), mode=mode)


def atomic_write_json(
    path: os.PathLike[str] | str,
    value: Any,
    *,
    mode: int | None = None,
) -> Path:
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    return atomic_write_text(path, payload, mode=mode)


class FileLock:
    """A cooperative exclusive lock represented by an atomically created file."""

    def __init__(
        self,
        path: os.PathLike[str] | str,
        *,
        timeout: float = 10.0,
        poll_interval: float = 0.1,
        stale_after: float = 300.0,
    ) -> None:
        self.path = Path(path)
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.stale_after = stale_after
        self._descriptor: int | None = None
        self._token = str(uuid.uuid4())

    def _payload(self) -> bytes:
        value = {
            "schema_version": 1,
            "token": self._token,
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "created_at_utc": utc_now(),
        }
        return (json.dumps(value, ensure_ascii=False) + "\n").encode("utf-8")

    def _remove_stale_lock(self) -> bool:
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            return True
        if age <= self.stale_after:
            return False
        try:
            self.path.unlink()
            return True
        except FileNotFoundError:
            return True
        except OSError:
            return False

    def acquire(self) -> FileLock:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                os.write(descriptor, self._payload())
                os.fsync(descriptor)
                self._descriptor = descriptor
                return self
            except FileExistsError as exc:
                if self._remove_stale_lock():
                    continue
                if time.monotonic() >= deadline:
                    raise LockError(
                        f"Timed out waiting for lock: {self.path}",
                        details={"lock_path": str(self.path), "timeout_seconds": self.timeout},
                    ) from exc
                time.sleep(self.poll_interval)

    def release(self) -> None:
        if self._descriptor is not None:
            os.close(self._descriptor)
            self._descriptor = None
        try:
            current = json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, ValueError):
            current = None
        if isinstance(current, dict) and current.get("token") != self._token:
            return
        self.path.unlink(missing_ok=True)

    def __enter__(self) -> FileLock:
        return self.acquire()

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.release()
