from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "runtime" / "boot" / "tools" / "air-boot.py"


def run_legacy(tmp_path: Path, *arguments: str) -> dict[str, object]:
    environment = dict(os.environ)
    environment["AIR_HOME"] = str(tmp_path / "air-home")
    completed = subprocess.run(
        [sys.executable, str(TOOL), *arguments],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout
    return json.loads(completed.stdout)


def test_legacy_boot_adapter_delegates_to_stage3_service(tmp_path: Path) -> None:
    validation = run_legacy(tmp_path, "validate-manifest")
    assert validation["decision"] == "PASS"
    assert validation["manifest_version"] == "2.0.0"

    plan = run_legacy(tmp_path, "plan", "--trigger", "Q1_D_ORIENTATION")
    assert "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1" in plan["planned_modules"]
