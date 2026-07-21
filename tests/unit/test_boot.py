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


def _copy_candidate(tmp_path: Path) -> Path:
    copied = tmp_path / "copy"
    shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", ".venv*", "dist", ".air-build"))
    return copied


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _refresh_declared_resource(root: Path, relative_path: str) -> None:
    manifest_path = root / "runtime/boot/AIR BOOT MODULE MANIFEST.json"
    manifest = _load_json(manifest_path)
    data = (root / relative_path).read_bytes()
    entries: list[dict[str, object]] = []
    for key in ("kernel", "boot_starter", "semantic_closure", "compile_receipt_schema", "compile_receipt_template"):
        entry = manifest.get(key)
        if isinstance(entry, dict):
            entries.append(entry)
    canonical = manifest.get("canonical_monolith")
    if isinstance(canonical, list):
        entries.extend(entry for entry in canonical if isinstance(entry, dict))
    modules = manifest.get("modules")
    if isinstance(modules, list):
        entries.extend(entry for entry in modules if isinstance(entry, dict))
    matched = False
    for entry in entries:
        declared_path = entry.get("relative_path", entry.get("file"))
        if declared_path == relative_path:
            entry["sha256"] = hashlib.sha256(data).hexdigest()
            entry["size_bytes"] = len(data)
            matched = True
    assert matched, relative_path
    _write_json(manifest_path, manifest)


def _extract_length_framed_resources(bundle: bytes) -> list[tuple[dict[str, object], bytes]]:
    marker = b"<!-- AIR_RESOURCE_BEGIN "
    offset = 0
    result: list[tuple[dict[str, object], bytes]] = []
    while True:
        begin = bundle.find(marker, offset)
        if begin < 0:
            break
        header_end = bundle.find(b" -->\n", begin)
        assert header_end >= 0
        metadata_start = begin + len(marker)
        metadata = json.loads(bundle[metadata_start:header_end].decode("utf-8"))
        data_start = header_end + len(b" -->\n")
        size = metadata["size_bytes"]
        assert isinstance(size, int)
        data = bundle[data_start : data_start + size]
        footer = f"\n<!-- AIR_RESOURCE_END {metadata['relative_path']} -->\n".encode()
        assert bundle[data_start + size : data_start + size + len(footer)] == footer
        result.append((metadata, data))
        offset = data_start + size + len(footer)
    return result


def test_validation_rejects_self_consistent_kernel_without_required_contract(tmp_path: Path) -> None:
    copied = _copy_candidate(tmp_path)
    kernel_path = copied / "runtime/boot/AIR BOOT KERNEL.md"
    kernel_path.write_text("arbitrary kernel\n", encoding="utf-8")

    manifest_path = copied / "runtime/boot/AIR BOOT MODULE MANIFEST.json"
    manifest = _load_json(manifest_path)
    kernel = manifest["kernel"]
    assert isinstance(kernel, dict)
    kernel.pop("terminal_sentinel")
    kernel_data = kernel_path.read_bytes()
    kernel["sha256"] = hashlib.sha256(kernel_data).hexdigest()
    kernel["size_bytes"] = len(kernel_data)

    starter_path = copied / "runtime/boot/AIR BOOT STARTER PROFILE.json"
    starter = _load_json(starter_path)
    starter_kernel = starter["kernel"]
    assert isinstance(starter_kernel, dict)
    starter_kernel["sha256"] = kernel["sha256"]
    starter_kernel["size_bytes"] = kernel["size_bytes"]
    _write_json(starter_path, starter)
    starter_data = starter_path.read_bytes()
    boot_starter = manifest["boot_starter"]
    assert isinstance(boot_starter, dict)
    boot_starter["sha256"] = hashlib.sha256(starter_data).hexdigest()
    boot_starter["size_bytes"] = len(starter_data)
    _write_json(manifest_path, manifest)

    result = compiler_for(tmp_path / "state", copied).validate()
    assert result["decision"] == "FAIL"
    assert any(
        check["name"] in {"KERNEL_DECLARATION", "KERNEL_RESOURCE_SENTINEL"}
        and check["status"] == "FAIL"
        for check in result["checks"]
    )


def test_validation_rejects_self_consistent_markdown_module_without_sentinel(tmp_path: Path) -> None:
    copied = _copy_candidate(tmp_path)
    relative_path = "runtime/modules/runtime/AIR RUNTIME MODULE - CODING REPOSITORY AND RELEASE.md"
    module_path = copied / relative_path
    module_path.write_text("arbitrary coding module\n", encoding="utf-8")
    manifest_path = copied / "runtime/boot/AIR BOOT MODULE MANIFEST.json"
    manifest = _load_json(manifest_path)
    modules = manifest["modules"]
    assert isinstance(modules, list)
    module = next(item for item in modules if isinstance(item, dict) and item.get("relative_path") == relative_path)
    module.pop("terminal_sentinel")
    data = module_path.read_bytes()
    module["sha256"] = hashlib.sha256(data).hexdigest()
    module["size_bytes"] = len(data)
    _write_json(manifest_path, manifest)

    result = compiler_for(tmp_path / "state", copied).validate()
    assert result["decision"] == "FAIL"
    assert any(check["name"].endswith("_SENTINEL") and check["status"] == "FAIL" for check in result["checks"])


def test_validation_rejects_reduced_starter_document(tmp_path: Path) -> None:
    copied = _copy_candidate(tmp_path)
    starter_path = copied / "runtime/boot/AIR BOOT STARTER PROFILE.json"
    _write_json(starter_path, {"SYSTEM_DESIGNATION": "AIR_BOOT_STARTER_PROFILE_V1", "version": "2.0.0"})
    _refresh_declared_resource(copied, "runtime/boot/AIR BOOT STARTER PROFILE.json")
    result = compiler_for(tmp_path / "state", copied).validate()
    assert result["decision"] == "FAIL"
    assert any(check["name"] == "STARTER_STRUCTURE" and check["status"] == "FAIL" for check in result["checks"])


def test_validation_rejects_relaxed_semantic_contract(tmp_path: Path) -> None:
    copied = _copy_candidate(tmp_path)
    semantic_path = copied / "runtime/boot/AIR BOOT SEMANTIC CLOSURE.json"
    semantic = _load_json(semantic_path)
    q1d = semantic["q1d"]
    assert isinstance(q1d, dict)
    q1d["project_activation_allowed"] = True
    semantic["unknown_trigger_behavior"] = "SILENT_EXECUTION"
    _write_json(semantic_path, semantic)
    _refresh_declared_resource(copied, "runtime/boot/AIR BOOT SEMANTIC CLOSURE.json")
    result = compiler_for(tmp_path / "state", copied).validate()
    assert result["decision"] == "FAIL"
    failed = {check["name"] for check in result["checks"] if check["status"] == "FAIL"}
    assert {"Q1D_SEMANTIC_CONTRACT", "UNKNOWN_TRIGGER_CONTRACT"}.issubset(failed)


def test_validation_rejects_missing_complete_prompt_set_declaration(tmp_path: Path) -> None:
    copied = _copy_candidate(tmp_path)
    manifest_path = copied / "runtime/boot/AIR BOOT MODULE MANIFEST.json"
    manifest = _load_json(manifest_path)
    manifest.pop("canonical_monolith")
    _write_json(manifest_path, manifest)
    result = compiler_for(tmp_path / "state", copied).validate()
    assert result["decision"] == "FAIL"
    assert any(
        check["name"] == "CANONICAL_PROMPT_SET_DECLARATION" and check["status"] == "FAIL"
        for check in result["checks"]
    )


def test_bundle_frames_hash_exact_embedded_resource_bytes(tmp_path: Path) -> None:
    copied = _copy_candidate(tmp_path)
    starter_relative = "runtime/boot/AIR BOOT STARTER PROFILE.json"
    starter_path = copied / starter_relative
    starter_path.write_bytes(starter_path.read_bytes() + b"\n\n")
    _refresh_declared_resource(copied, starter_relative)

    compiler = compiler_for(tmp_path / "state", copied)
    compiled = compiler.compile(["NEW_PROJECT"])
    frames = _extract_length_framed_resources(compiled["bundle_bytes"])
    assert len(frames) == compiled["resource_count"]
    for metadata, data in frames:
        assert len(data) == metadata["size_bytes"]
        assert hashlib.sha256(data).hexdigest() == metadata["sha256"]
    starter_frame = next(data for metadata, data in frames if metadata["relative_path"] == starter_relative)
    assert starter_frame.endswith(b"\n\n")


def test_concurrent_bundle_and_receipt_writes_remain_matched(tmp_path: Path) -> None:
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    output = tmp_path / "bundle.md"
    receipt = tmp_path / "receipt.json"
    barrier = Barrier(2)

    def write(triggers: list[str]) -> dict[str, object]:
        compiler = compiler_for(tmp_path / ("state-" + triggers[0].lower()))
        barrier.wait()
        return compiler.write_bundle(output, triggers, receipt_output=receipt, overwrite=True)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(write, [["NEW_PROJECT"], ["CODING", "REPOSITORY"]]))

    assert all(result["decision"] == "PASS" for result in results)
    final_receipt = _load_json(receipt)
    assert final_receipt["bundle_sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()


def test_fallback_plan_id_is_bound_to_complete_resource_identity(tmp_path: Path) -> None:
    baseline = compiler_for(tmp_path / "baseline").plan(["UNKNOWN_TRIGGER"])
    copied = _copy_candidate(tmp_path)
    prompt_relative = "prompts/AIR CORE RUNTIME.md"
    prompt_path = copied / prompt_relative
    text = prompt_path.read_text(encoding="utf-8")
    sentinel = "AIR_LOAD_SENTINEL :: AIR_CORE_RUNTIME :: END_OF_FILE :: LOAD_INTEGRITY_V1"
    assert sentinel in text
    prompt_path.write_text(text.replace(sentinel, "REMediation identity marker\n\n" + sentinel), encoding="utf-8")
    _refresh_declared_resource(copied, prompt_relative)

    changed = compiler_for(tmp_path / "changed", copied).plan(["UNKNOWN_TRIGGER"])
    assert changed["source_tree_digest"] != baseline["source_tree_digest"]
    assert changed["resource_set_version"] != baseline["resource_set_version"]
    assert changed["plan_id"] != baseline["plan_id"]
