from __future__ import annotations

import json
import os
import subprocess
import venv
from pathlib import Path

import pytest


def _artifact_from_environment(environment_variable: str, label: str) -> Path | None:
    explicit = os.environ.get(environment_variable)
    if explicit:
        return Path(explicit).resolve()
    dist_dir_value = os.environ.get("AIR_TEST_DIST_DIR")
    if not dist_dir_value:
        return None
    dist_dir = Path(dist_dir_value).resolve()
    pattern = "*.whl" if label == "wheel" else "*.tar.gz"
    matches = sorted(dist_dir.glob(pattern))
    assert len(matches) == 1, f"Expected exactly one {label} in {dist_dir}; found {matches}"
    return matches[0]


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
    artifact = _artifact_from_environment(environment_variable, label)
    if artifact is None:
        pytest.skip(f"{environment_variable} or AIR_TEST_DIST_DIR is not set")
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
    assert run("boot", "validate")["decision"] == "PASS"
    contracts = run("boot", "contracts", "authorization", "--content")
    authorization_schema = contracts["contracts"]["authorization"]["schema"]
    assert authorization_schema["$id"] == "urn:air:authorization-envelope:1"
    assert "approval_ref" in authorization_schema["required"]
    provenance_rule = authorization_schema["allOf"][0]["then"]["properties"]
    assert provenance_rule["approval_ref"]["type"] == "string"
    assert provenance_rule["actor"]["not"]["pattern"] == r"^\s*UNSPECIFIED\s*$"
    boot_plan = run("boot", "plan", "--trigger", "Q1_D_ORIENTATION")
    assert "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1" in boot_plan["planned_modules"]
    bundle = outside / f"installed-{label}-boot.md"
    compile_result = run("boot", "compile", "--trigger", "CODING", "--output", str(bundle))
    assert compile_result["decision"] == "PASS"
    assert bundle.is_file()
    assert b"AIR_RESOURCE_LENGTH_FRAMED_V1" in bundle.read_bytes()
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
