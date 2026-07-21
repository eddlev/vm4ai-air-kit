from __future__ import annotations

import json
import os
import subprocess
import venv
from pathlib import Path

import pytest


@pytest.mark.package
@pytest.mark.parametrize(
    ("environment_variable", "label"),
    [
        ("AIR_TEST_WHEEL", "wheel"),
        ("AIR_TEST_SDIST", "sdist"),
    ],
)
def test_built_distribution_installs_and_runs_without_repository(
    tmp_path: Path,
    environment_variable: str,
    label: str,
) -> None:
    artifact_value = os.environ.get(environment_variable)
    if not artifact_value:
        pytest.skip(f"{environment_variable} is not set")
    artifact = Path(artifact_value).resolve()
    assert artifact.is_file()

    environment_dir = tmp_path / f"venv-{label}"
    venv.EnvBuilder(with_pip=True).create(environment_dir)
    python = environment_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", str(artifact)], check=True)
    subprocess.run([str(python), "-m", "pip", "check"], check=True)

    outside = tmp_path / f"outside-repository-{label}"
    outside.mkdir()
    environment = dict(os.environ)
    environment["AIR_HOME"] = str(tmp_path / f"air-home-{label}")
    environment.pop("AIR_RESOURCE_ROOT", None)
    environment.pop("PYTHONPATH", None)

    def run(*arguments: str) -> dict[str, object]:
        completed = subprocess.run(
            [str(python), "-m", "vm4ai_air", "--json", *arguments],
            cwd=outside,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout
        return json.loads(completed.stdout)

    version = run("--version")
    assert version["resource_origin"] == "INSTALLED_PACKAGE"
    assert version["resource_set_version"] != "UNAVAILABLE"
    assert run("resources", "verify")["decision"] == "PASS"
    project = run("project", "init", f"Installed {label} Project", "--use")["project"]
    assert Path(project["workspace_path"]).is_dir()
    assert run("project", "validate")["decision"] == "PASS"
    assert run("doctor")["decision"] in {"PASS", "WARN"}

    location = subprocess.run(
        [str(python), "-c", "import vm4ai_air, pathlib; print(pathlib.Path(vm4ai_air.__file__).resolve())"],
        cwd=outside,
        env=environment,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    assert str(environment_dir.resolve()) in location
