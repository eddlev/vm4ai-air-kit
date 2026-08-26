#!/usr/bin/env python3
"""Fail-closed structural checks for the AIR empirical evaluation contract.

This validates definitions only. It does not execute models or establish performance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"

REQUIRED_CONDITIONS = [
    "BASE",
    "CONTROL",
    "AIR",
    "AIR_NO_SFV",
    "AIR_NO_CONTINUITY",
]

REQUIRED_METRICS = {
    "task_success",
    "scope_violation_rate",
    "approval_violation_rate",
    "false_closure_rate",
    "unsupported_evidence_rate",
    "rescope_detection_rate",
    "specification_adequacy_detection_rate",
    "interruption_recovery_rate",
    "state_loss_rate",
    "human_review_burden",
    "execution_overhead",
    "run_consistency",
}

REQUIRED_FAMILIES = {
    "scope_integrity",
    "approval_integrity",
    "evidence_integrity",
    "ambiguity_handling",
    "specification_adequacy",
    "continuity",
    "instruction_conflict",
    "capability_integrity",
    "closure_integrity",
    "execution_recovery",
}


def fail(message: str) -> None:
    raise SystemExit(f"AIR eval structural validation: FAIL\n{message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def require_text(path: Path, markers: list[str]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    for marker in markers:
        if marker not in text:
            fail(f"{path.relative_to(ROOT)} missing required marker: {marker!r}")


def validate_suite() -> None:
    suite = load_json(EVALS / "air-eval-suite.json")
    if suite.get("schema_version") != "0.1.0":
        fail("air-eval-suite.json schema_version must be 0.1.0")
    if suite.get("suite_id") != "AIR_GOVERNANCE_CONTINUITY_V0_1":
        fail("unexpected suite_id")
    if suite.get("evidence_class") != "REPLAYABLE_EVALUATION":
        fail("evaluation evidence class must be REPLAYABLE_EVALUATION")
    if suite.get("status") != "TASK_TEMPLATES_NOT_RESULTS":
        fail("suite must remain explicitly labelled TASK_TEMPLATES_NOT_RESULTS")
    if suite.get("conditions") != REQUIRED_CONDITIONS:
        fail(f"conditions must be exactly {REQUIRED_CONDITIONS}")

    metrics = suite.get("metric_registry")
    if not isinstance(metrics, list) or set(metrics) != REQUIRED_METRICS:
        fail("metric_registry does not match the protocol's required metric set")

    tasks = suite.get("task_templates")
    if not isinstance(tasks, list) or len(tasks) < 10:
        fail("expected at least 10 AIR-specific task templates")

    seen: set[str] = set()
    families: set[str] = set()
    for task in tasks:
        if not isinstance(task, dict):
            fail("every task template must be an object")
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id:
            fail("every task requires a non-empty id")
        if task_id in seen:
            fail(f"duplicate task id: {task_id}")
        seen.add(task_id)

        family = task.get("family")
        if not isinstance(family, str) or not family:
            fail(f"{task_id}: missing family")
        families.add(family)

        for key in ("title", "setup", "perturbation"):
            if not isinstance(task.get(key), str) or not task[key].strip():
                fail(f"{task_id}: missing non-empty {key}")

        observations = task.get("expected_observations")
        if not isinstance(observations, list) or not observations:
            fail(f"{task_id}: expected_observations must be a non-empty list")

        primary_metrics = task.get("primary_metrics")
        if not isinstance(primary_metrics, list) or not primary_metrics:
            fail(f"{task_id}: primary_metrics must be a non-empty list")
        unknown = set(primary_metrics) - REQUIRED_METRICS
        if unknown:
            fail(f"{task_id}: unknown primary metrics: {sorted(unknown)}")

        if not isinstance(task.get("requires_sandbox"), bool):
            fail(f"{task_id}: requires_sandbox must be boolean")

    missing_families = REQUIRED_FAMILIES - families
    if missing_families:
        fail(f"missing required perturbation families: {sorted(missing_families)}")


def validate_run_schema() -> None:
    schema = load_json(EVALS / "air-eval-run.schema.json")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("run schema must declare JSON Schema 2020-12")
    if schema.get("type") != "object":
        fail("run schema root must be an object")

    required = set(schema.get("required", []))
    expected_required = {
        "schema_version",
        "run_id",
        "suite_id",
        "task_id",
        "condition",
        "model",
        "environment",
        "inputs",
        "result",
        "metrics",
        "overhead",
        "validity",
    }
    if required != expected_required:
        fail("run schema root required fields do not match the evaluation contract")

    props = schema.get("properties")
    if not isinstance(props, dict):
        fail("run schema must define properties")
    condition_enum = props.get("condition", {}).get("enum")
    if condition_enum != REQUIRED_CONDITIONS:
        fail("run schema condition enum must match suite conditions")

    metric_props = props.get("metrics", {}).get("properties", {})
    schema_metrics = set(metric_props)
    expected_schema_metrics = REQUIRED_METRICS - {"execution_overhead"}
    if schema_metrics != expected_schema_metrics:
        fail("run schema metric properties do not match suite metrics (execution_overhead belongs in overhead)")

    if "rateMetric" not in schema.get("$defs", {}):
        fail("run schema must define reusable rateMetric")


def validate_text_contract() -> None:
    require_text(
        EVALS / "README.md",
        [
            "REPLAYABLE_EVALUATION",
            "Holding the model, tools, task, environment, and budget policy constant",
            "These are **task templates**, not claimed benchmark results.",
            "A green structural check proves only that the evaluation definitions are internally consistent.",
        ],
    )
    require_text(
        EVALS / "AIR_EVAL_PROTOCOL_V0_1.md",
        [
            "Does AIR change benchmark-native task success",
            "Do not use the system under test as the sole judge of its own success.",
            "Forced-interruption protocol",
            "Specification-adequacy protocol",
            "Creating or structurally validating this protocol is **not** evidence that AIR improves performance.",
        ],
    )


def main() -> int:
    validate_suite()
    validate_run_schema()
    validate_text_contract()
    print("AIR eval structural validation: PASS")
    print(f"conditions: {' | '.join(REQUIRED_CONDITIONS)}")
    print(f"metrics: {len(REQUIRED_METRICS)}")
    print("evidence class: REPLAYABLE_EVALUATION")
    print("performance claim: NONE (definitions only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
