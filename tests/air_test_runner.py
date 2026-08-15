#!/usr/bin/env python3
"""Deterministic/replayable AIR test runner using only the Python standard library."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

RUNNER_VERSION = "1.0.0"


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strict_json_load(path: Path) -> Any:
    def no_dupes(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate JSON key: {key}")
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_dupes)


def json_path_get(value: Any, dotted_path: str) -> Any:
    cur = value
    for part in dotted_path.split(".") if dotted_path else []:
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            cur = cur[part]
        else:
            raise KeyError(f"cannot descend through {type(cur).__name__} at {part}")
    return cur


def stable_environment() -> dict[str, str]:
    return {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
        "tz": os.environ.get("TZ", ""),
        "lang": os.environ.get("LANG", ""),
        "lc_all": os.environ.get("LC_ALL", ""),
        "pythonhashseed": os.environ.get("PYTHONHASHSEED", ""),
        "air_test_seed": os.environ.get("AIR_TEST_SEED", ""),
        "network_policy": os.environ.get("AIR_NETWORK_POLICY", "UNVERIFIED"),
        "container_image": os.environ.get("AIR_CONTAINER_IMAGE", "UNVERIFIED"),
        "source_commit": os.environ.get("AIR_SOURCE_COMMIT", "UNVERIFIED"),
    }


def collect_input_hashes(root: Path, inputs: list[str]) -> dict[str, str]:
    result = {}
    for rel in sorted(inputs):
        path = root / rel
        if not path.is_file():
            raise FileNotFoundError(f"material input not found: {rel}")
        result[rel] = sha256_file(path)
    return result


def run_test(root: Path, test: dict[str, Any]) -> dict[str, Any]:
    test_id = test["id"]
    kind = test["type"]
    expected = test.get("expected")
    observed: Any = None
    passed = False
    failure_reason = None

    try:
        if kind == "file_exists":
            observed = (root / test["path"]).is_file()
            passed = observed is True
        elif kind == "text_contains":
            text = (root / test["path"]).read_text(encoding="utf-8")
            observed = test["text"] in text
            passed = observed is True
        elif kind == "text_not_contains":
            text = (root / test["path"]).read_text(encoding="utf-8")
            observed = test["text"] not in text
            passed = observed is True
        elif kind == "regex_count":
            text = (root / test["path"]).read_text(encoding="utf-8")
            observed = len(re.findall(test["pattern"], text, flags=re.MULTILINE))
            passed = observed == expected
        elif kind == "json_strict_parse":
            strict_json_load(root / test["path"])
            observed = "PARSED_NO_DUPLICATE_KEYS"
            passed = True
        elif kind == "json_value_equals":
            obj = strict_json_load(root / test["path"])
            observed = json_path_get(obj, test["json_path"])
            passed = observed == expected
        elif kind == "sha256_equals":
            observed = sha256_file(root / test["path"])
            passed = observed == expected
        elif kind == "command":
            argv = test["argv"]
            if not isinstance(argv, list) or not argv or not all(isinstance(x, str) for x in argv):
                raise ValueError("command argv must be a non-empty string array")
            cwd = root / test.get("cwd", ".")
            env = os.environ.copy()
            env.update({str(k): str(v) for k, v in test.get("env", {}).items()})
            proc = subprocess.run(
                argv,
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=int(test.get("timeout_seconds", 120)),
                check=False,
            )
            observed = {
                "exit_code": proc.returncode,
                "stdout_sha256": sha256_bytes(proc.stdout),
                "stderr_sha256": sha256_bytes(proc.stderr),
            }
            passed = proc.returncode == int(test.get("expected_exit_code", 0))
            if passed and test.get("expected_stdout_sha256"):
                passed = observed["stdout_sha256"] == test["expected_stdout_sha256"]
            if passed and test.get("expected_stderr_sha256"):
                passed = observed["stderr_sha256"] == test["expected_stderr_sha256"]
        else:
            raise ValueError(f"unsupported test type: {kind}")
    except Exception as exc:
        failure_reason = f"{type(exc).__name__}: {exc}"
        observed = None
        passed = False

    return {
        "id": test_id,
        "requirement": test.get("requirement", ""),
        "test_class": test.get("test_class", "REPRODUCIBLE_EXECUTABLE"),
        "type": kind,
        "expected": expected,
        "observed": observed,
        "decision": "PASS" if passed else "FAIL",
        "failure_reason": failure_reason,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--run-index", type=int, required=True)
    args = parser.parse_args()

    root = Path.cwd().resolve()
    manifest_path = (root / args.manifest).resolve()
    manifest_bytes = manifest_path.read_bytes()
    manifest = strict_json_load(manifest_path)

    if manifest.get("schema_version") != "1.0.0":
        raise SystemExit("unsupported manifest schema_version")
    if not manifest.get("suite_id"):
        raise SystemExit("manifest suite_id is required")

    env_identity = stable_environment()
    input_hashes = collect_input_hashes(root, manifest.get("material_inputs", []))
    input_set_sha256 = sha256_bytes(canonical_json(input_hashes))
    environment_fingerprint = sha256_bytes(canonical_json(env_identity))

    started = int(time.time())
    results = [run_test(root, test) for test in manifest.get("tests", [])]
    completed = int(time.time())

    decision_payload = [
        {
            "id": r["id"],
            "test_class": r["test_class"],
            "decision": r["decision"],
            "observed": r["observed"],
        }
        for r in results
    ]
    decision_fingerprint = sha256_bytes(canonical_json(decision_payload))
    passed = sum(1 for r in results if r["decision"] == "PASS")
    failed = len(results) - passed
    run_id_seed = {
        "suite": manifest["suite_id"],
        "suite_sha256": sha256_bytes(manifest_bytes),
        "source_commit": env_identity["source_commit"],
        "run_index": args.run_index,
        "started": started,
    }
    run_id = "AIR-TEST-" + sha256_bytes(canonical_json(run_id_seed))[:20]

    output = {
        "record_schema_version": "1.0.0",
        "run_id": run_id,
        "run_index": args.run_index,
        "suite_id": manifest["suite_id"],
        "suite_sha256": sha256_bytes(manifest_bytes),
        "definition_or_manifest_sha256": sha256_bytes(manifest_bytes),
        "fixture_set_sha256": input_set_sha256,
        "material_input_hashes": input_hashes,
        "source_revision": env_identity["source_commit"],
        "runner_identity": "tests/air_test_runner.py",
        "runner_version": RUNNER_VERSION,
        "runtime_identity": {
            "python_implementation": env_identity["python_implementation"],
            "python_version": env_identity["python_version"],
        },
        "environment_identity": env_identity,
        "environment_fingerprint": environment_fingerprint,
        "working_directory": str(root),
        "execution_command_or_argv": sys.argv,
        "random_seed_or_not_applicable": env_identity["air_test_seed"] or "NOT_APPLICABLE",
        "network_policy": env_identity["network_policy"],
        "started_at_epoch": started,
        "completed_at_epoch": completed,
        "test_evidence_class": "REPRODUCIBLE_EXECUTABLE",
        "reproducibility_state": "UNVERIFIED_PENDING_REPEAT_COMPARISON",
        "tests_total": len(results),
        "tests_passed": passed,
        "tests_failed": failed,
        "decision": "PASS" if failed == 0 else "FAIL",
        "decision_fingerprint": decision_fingerprint,
        "per_test_results": results,
        "claim_boundary": "This record proves only the executable checks observed in this run. It does not prove untested intent, hidden model state, or external effects outside the recorded environment."
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{passed}/{len(results)} executable checks passed; run_id={run_id}; fingerprint={decision_fingerprint}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
