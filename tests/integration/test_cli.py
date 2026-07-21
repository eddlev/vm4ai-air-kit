from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_air(tmp_path: Path, *arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update(
        {
            "AIR_HOME": str(tmp_path / "air-home"),
            "AIR_RESOURCE_ROOT": str(ROOT),
            "PYTHONPATH": str(ROOT / "src"),
        }
    )
    return subprocess.run(
        [sys.executable, "-m", "vm4ai_air", "--json", *arguments],
        cwd=cwd or tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def payload(result: subprocess.CompletedProcess[str]) -> object:
    assert result.stdout, result.stderr
    return json.loads(result.stdout)


def test_cli_operates_outside_repository(tmp_path: Path) -> None:
    version = run_air(tmp_path, "--version")
    assert version.returncode == 0
    assert payload(version)["package_version"] == "0.4.0.dev0"

    created = run_air(tmp_path, "project", "init", "CLI Project", "--use", cwd=tmp_path)
    assert created.returncode == 0, created.stderr
    project = payload(created)["project"]
    assert Path(project["workspace_path"]).is_dir()

    listed = run_air(tmp_path, "project", "list", cwd=Path(project["workspace_path"]))
    assert listed.returncode == 0
    assert len(payload(listed)) == 1

    validated = run_air(tmp_path, "project", "validate", cwd=tmp_path)
    assert validated.returncode == 0
    assert payload(validated)["decision"] == "PASS"

    resources = run_air(tmp_path, "resources", "verify", cwd=tmp_path)
    assert resources.returncode == 0
    assert payload(resources)["decision"] == "PASS"

    doctor = run_air(tmp_path, "doctor", cwd=tmp_path)
    assert doctor.returncode == 0
    assert payload(doctor)["decision"] in {"PASS", "WARN"}
