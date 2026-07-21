from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from jsonschema import validate

from vm4ai_air.boot import BootCompiler
from vm4ai_air.errors import BootError, ResourceIntegrityError
from vm4ai_air.paths import AppPaths

ROOT = Path(__file__).resolve().parents[2]


def compiler_for(tmp_path: Path, root: Path = ROOT) -> BootCompiler:
    environment = {"AIR_HOME": str(tmp_path / "air-home"), "AIR_RESOURCE_ROOT": str(root)}
    return BootCompiler.from_environment(environment=environment, paths=AppPaths.resolve(environment))


def test_boot_validation_and_semantic_closure_pass(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    result = compiler.validate()
    assert result["decision"] == "PASS"
    assert result["module_count"] == 23
    assert result["failed_count"] == 0


def test_q1d_plan_contains_complete_orientation_closure(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    result = compiler.plan(["Q1_D_ORIENTATION"])
    assert result["decision"] == "PASS"
    assert result["boot_mode"] == "LOCAL_BUNDLED"
    assert "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1" in result["planned_modules"]
    assert "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1" in result["planned_modules"]
    assert "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1" in result["planned_modules"]
    orientation = compiler.q1d_orientation()
    assert orientation["activation_state"] == "NOT_ACTIVATED"
    assert "## 1. No prior AIR knowledge required" in orientation["content"]
    assert "## 11. Return to Q1" in orientation["content"]


def test_unknown_trigger_falls_back_visibly_to_complete_prompt_set(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    result = compiler.plan(["DO_WHATEVER_IT_TAKES"])
    assert result["decision"] == "REVIEW"
    assert result["boot_mode"] == "FULL_MONOLITH"
    assert result["fallback_state"] == "UNKNOWN_TRIGGER_FULL_MONOLITH"
    assert result["unknown_triggers"] == ["DO_WHATEVER_IT_TAKES"]


def test_compile_is_byte_deterministic_for_same_inputs(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    first = compiler.compile(["CODING", "REPOSITORY"])
    second = compiler.compile(["REPOSITORY", "CODING"])
    assert first["bundle_bytes"] == second["bundle_bytes"]
    assert first["bundle_sha256"] == hashlib.sha256(first["bundle_bytes"]).hexdigest()
    assert first["plan"]["authorization_decision"] == "NOT_EVALUATED"
    assert "AIR_RUNTIME_CONTRACT_GATE_AND_EXECUTION_V1" in first["plan"]["planned_modules"]


def test_boot_validation_detects_tampered_q1d_module(tmp_path: Path) -> None:
    copied = tmp_path / "copy"
    shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", ".venv*", "dist", ".air-build"))
    q1d = copied / "runtime/modules/control/AIR CONTROL MODULE - Q1-D BEGINNER ORIENTATION.md"
    q1d.write_text(q1d.read_text(encoding="utf-8") + "\ntampered\n", encoding="utf-8")
    try:
        compiler_for(tmp_path / "state", copied)
    except ResourceIntegrityError as exc:
        assert "Terminal sentinel mismatch" in exc.message
    else:  # pragma: no cover - fail-closed source validation must trigger first
        raise AssertionError("tampered Q1-D module was accepted")


def test_full_fallback_bundle_contains_complete_prompt_set(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    compiled = compiler.compile(["UNKNOWN_TRIGGER"])
    paths = [item["relative_path"] for item in compiled["bundle_manifest"]["resources"]]
    assert paths == [
        "prompts/AIR CORE RUNTIME.md",
        "prompts/AIR CONTROL SURFACE.md",
        "prompts/AIR DEFAULT STARTER PROFILE.json",
    ]
    assert compiled["decision"] == "REVIEW"


def test_compile_receipt_matches_runtime_schema(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    compiled = compiler.compile(["NEW_PROJECT"])
    receipt = compiler.receipt(compiled)
    schema = json.loads(
        (ROOT / "runtime/boot/schemas/AIR BOOT COMPILE RECEIPT SCHEMA.json").read_text(encoding="utf-8")
    )
    validate(receipt, schema)


def test_compile_refuses_output_inside_canonical_resource_roots(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    protected = ROOT / "runtime" / "should-not-be-written.md"
    try:
        compiler.write_bundle(protected, ["NEW_PROJECT"], overwrite=True)
    except BootError as exc:
        assert "may not overwrite canonical authoring resources" in exc.message
    else:  # pragma: no cover
        raise AssertionError("canonical resource output path was accepted")
    assert not protected.exists()


def test_new_project_plan_closes_reachable_q1d_branch(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    result = compiler.plan(["NEW_PROJECT"])
    assert "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1" in result["planned_modules"]


def test_default_session_entry_plan_closes_all_q1_routes(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    result = compiler.plan()
    assert result["requested_triggers"] == ["SESSION_ENTRY"]
    assert "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1" in result["planned_modules"]
    assert "AIR_RUNTIME_POLICY_AND_HANDOFF_SECURITY_V1" in result["planned_modules"]
    assert "AIR_CONTROL_POLICY_HANDOFF_AND_PORTABILITY_V1" in result["planned_modules"]


def test_bundle_and_receipt_write_roll_back_together(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import vm4ai_air.boot.compiler as compiler_module

    compiler = compiler_for(tmp_path)
    output = tmp_path / "bundle.md"
    receipt = tmp_path / "receipt.json"

    def fail_receipt(_path: Path, _value: object) -> None:
        raise OSError("injected receipt failure")

    monkeypatch.setattr(compiler_module, "atomic_write_json", fail_receipt)
    try:
        compiler.write_bundle(output, ["NEW_PROJECT"], receipt_output=receipt)
    except BootError as exc:
        assert "rolled back" in exc.message
    else:  # pragma: no cover
        raise AssertionError("receipt failure did not fail the bundle transaction")
    assert not output.exists()
    assert not receipt.exists()


def test_bundle_and_receipt_must_use_different_paths(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    output = tmp_path / "same-output"
    try:
        compiler.write_bundle(output, ["NEW_PROJECT"], receipt_output=output)
    except BootError as exc:
        assert "must be different files" in exc.message
    else:  # pragma: no cover
        raise AssertionError("same bundle and receipt path was accepted")


def test_standalone_receipt_refuses_canonical_resource_root(tmp_path: Path) -> None:
    compiler = compiler_for(tmp_path)
    protected = ROOT / "runtime" / "should-not-be-written.json"
    try:
        compiler.write_receipt(protected, ["NEW_PROJECT"], overwrite=True)
    except BootError as exc:
        assert "may not overwrite canonical authoring resources" in exc.message
    else:  # pragma: no cover
        raise AssertionError("canonical receipt output path was accepted")
    assert not protected.exists()
