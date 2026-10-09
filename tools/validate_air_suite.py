from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(".").resolve()


def run_stage(name: str, command: list[str]) -> None:
    print(f"=== AIR validation stage: {name} ===", flush=True)
    proc = subprocess.run(command, cwd=ROOT)
    if proc.returncode != 0:
        raise SystemExit(f"AIR validation suite FAILED at stage: {name} (exit {proc.returncode})")


def main() -> None:
    py = sys.executable
    run_stage("v081_repository_source_runtime_contract", [py, "tools/validate_air_v081_repository.py"])
    run_stage("v081_repository_mutation_contract", [py, "tools/test_air_v081_repository_mutations.py"])
    print("AIR canonical validation suite: PASS (v0.8.1 current authority)")


if __name__ == "__main__":
    main()
