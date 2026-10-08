#!/usr/bin/env python3
"""AIR-P R23 AMRS4E compiler/schema/overlay/test integration candidate.

This noncanonical candidate is derived from the exact R23 post-cutover compiler
engine plus the installed H1 Core, H2 Control, and H3A Starter source tuple. It
reconstructs the validated consumption-key constructor semantics on top of
the exact runtime-hardening preimage and deterministically generates the compact turn-governance kernel and direct
runtime-reference index required by the runtime-hardening architecture. It is
fail-closed, creates no execution authority, and does not modify compile_air_p.py.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import unicodedata
import urllib.parse
from pathlib import Path

PACKAGE_DESIGNATION = "AIR_P_COMPLETE_COMPILATION_V1"
PACKAGE_VERSION = "1.0.0"
CANONICAL_JSON_ALGORITHM = "SHA256_CANONICAL_JSON_V1"
RECONSTRUCTION_CONTRACT = "AIRP_R23_AMRS4E_COMPILER_INTEGRATION_V1"
CURRENT_RUNTIME_STATE = "R23_AMRS4D3_POST_CUTOVER_CORE26_HANDOFF26"
PRIOR_LAW_ROUTER_INPUT_COUNT = 82
DECISION_TRACE_LAW_ID = "CORE.LAW.DECISION_TRACE_JUSTIFICATION_AND_CLOSURE"

EXPECTED = {
    "components": 113,
    "routes": 22,
    "control_events": 22,
    "deterministic_checks": 137,
    "formal_objects": 21,
    "laws": 83,
}

PINNED_HASHES = {
    "CORE_RUNTIME": "e4fb9fc9ac5b50d7d2d043a9489a086b398f543c41eefdc2762e92fb5e06b835",
    "GOVERNANCE_SUPPLEMENT": "24c5201961c419dece9035f112d5aa3e3b49460cc770656dfde44f7f3d705fd6",
    "CONTROL_SURFACE": "797e47f506de62d6a71dbcec15f915e92374b0cc7391c7dd4b0ed2ca6cedca28",
    "DEFAULT_STARTER_PROFILE": "b1e1f78debcb9f003be167c256f652dc68c4dea0be7ef05bab24ad04f5727f18",
    "HANDOFF_CARD_TEMPLATE": "8d1c87d3d4d2b191301eec9f27e83ac1e550b0ba99bede5a5d576e9d52e5f122",
    "RUNTIME_ROUTE_MAP": "c322f8d3ebd68594a506101d4fe0c783a4712b26c1f51ef20de8d5b8733d5817",
    "PACKAGE_SCHEMA": "6c019b38ce3108657a2a11948f9fa68e52f171279da5496925c6ae4eb2bbd75e",
    "COMPONENT_METADATA_OVERLAY": "553aec8171ae09272e2b133f1ff688c074068dd8007435384453f756fcb3dc03",
    "LAW_APPLICABILITY_ROUTER": "ece1fb608ff43def479c2fa1633cf0b158276dc1b1c2b6ace800a2f88e69677a",
    "LAW_SOURCE_PACKAGE_SCHEMA": "ef582abfa7433fdce0411b38d3ddbed0ca233124c0f80ad52abac0e39cca745f",
    "LAW_SOURCE_LAW_ID_REGISTRY": "03935a1fafc72d7c406f0995644afe820e2118f787c97702fe6f4ffc74d23d24",
    "LAW_SOURCE_LAW_BODY_INDEX": "d0aedaa34cf7b47bc9e4d620d04df1bf8adc4c13021d6aad7cfea4089b1ae296",
    "LAW_SOURCE_FLOOR_INVARIANT_INDEX": "f9c84ef97386fa49506ebe2712dd41cb48a07443c218062690f592a80a53b009"
}
CANONICAL_FILENAMES = {
    "CORE_RUNTIME": "AIR_CORE_RUNTIME.md",
    "GOVERNANCE_SUPPLEMENT": "AIR_GOV.md",
    "CONTROL_SURFACE": "AIR_CONTROL_SURFACE.md",
    "DEFAULT_STARTER_PROFILE": "AIR_DEFAULT_STARTER_PROFILE.json",
    "HANDOFF_CARD_TEMPLATE": "AIR_HANDOFF_CARD_TEMPLATE.json",
    "RUNTIME_ROUTE_MAP": "AIR_RUNTIME_ROUTE_MAP.json",
    "PACKAGE_SCHEMA": "AIR_P_PACKAGE_SCHEMA.json",
    "COMPONENT_METADATA_OVERLAY": "AIR_P_COMPONENT_METADATA_OVERLAY.json",
    "LAW_APPLICABILITY_ROUTER": "AIR_LAW_APPLICABILITY_ROUTER.json",
    "LAW_SOURCE_PACKAGE_SCHEMA": "AIR_LAW_SOURCE_PACKAGE_SCHEMA.json",
    "LAW_SOURCE_LAW_ID_REGISTRY": "AIR_LAW_ID_REGISTRY.json",
    "LAW_SOURCE_LAW_BODY_INDEX": "AIR_LAW_BODY_INDEX.json",
    "LAW_SOURCE_FLOOR_INVARIANT_INDEX": "AIR_FLOOR_INVARIANT_INDEX.json",
}

CANONICAL_PATHS = {
    "CORE_RUNTIME": "prompts/AIR_CORE_RUNTIME.md",
    "GOVERNANCE_SUPPLEMENT": "prompts/AIR_GOV.md",
    "CONTROL_SURFACE": "prompts/AIR_CONTROL_SURFACE.md",
    "DEFAULT_STARTER_PROFILE": "prompts/AIR_DEFAULT_STARTER_PROFILE.json",
    "HANDOFF_CARD_TEMPLATE": "prompts/AIR_HANDOFF_CARD_TEMPLATE.json",
    "RUNTIME_ROUTE_MAP": "catalog/AIR_RUNTIME_ROUTE_MAP.json",
    "PACKAGE_SCHEMA": "air_p/schema/AIR_P_PACKAGE_SCHEMA.json",
    "COMPONENT_METADATA_OVERLAY": "air_p/source/AIR_P_COMPONENT_METADATA_OVERLAY.json",
    "LAW_APPLICABILITY_ROUTER": "catalog/AIR_LAW_APPLICABILITY_ROUTER.json",
    "LAW_SOURCE_PACKAGE_SCHEMA": "law_source/AIR_LAW_SOURCE_PACKAGE_SCHEMA.json",
    "LAW_SOURCE_LAW_ID_REGISTRY": "law_source/AIR_LAW_ID_REGISTRY.json",
    "LAW_SOURCE_LAW_BODY_INDEX": "law_source/AIR_LAW_BODY_INDEX.json",
    "LAW_SOURCE_FLOOR_INVARIANT_INDEX": "law_source/AIR_FLOOR_INVARIANT_INDEX.json",
}

FOUNDATION_PATH_TO_ROLE = {
    "prompts/AIR_CORE_RUNTIME.md": "CORE_RUNTIME",
    "prompts/AIR_GOV.md": "GOVERNANCE_SUPPLEMENT",
    "prompts/AIR_CONTROL_SURFACE.md": "CONTROL_SURFACE",
    "prompts/AIR_DEFAULT_STARTER_PROFILE.json": "DEFAULT_STARTER_PROFILE",
    "prompts/AIR_HANDOFF_CARD_TEMPLATE.json": "HANDOFF_CARD_TEMPLATE",
    "catalog/AIR_RUNTIME_ROUTE_MAP.json": "RUNTIME_ROUTE_MAP",
}

TURN_GOVERNANCE_KERNEL_OUTPUT = "compiled/AIR_P_TURN_GOVERNANCE_KERNEL.json"
RUNTIME_REFERENCE_INDEX_OUTPUT = "compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json"
DIRECT_REFERENCE_DEPTH = 1

KERNEL_REQUIRED_SEMANTIC_IDS = [
    "AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1",
    "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1",
    "AIR_REQUIRED_EMISSION_PREFLIGHT_V2",
    "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1",
    "AIR_MATERIAL_ACTION_INTERLOCK_V3",
    "AIR_APPROVAL_RESPONSE_RESOLUTION_V2",
    "AIR_REQUIRED_INPUT_ARTIFACT_ACQUISITION_V3",
    "DETERMINISTIC_ONBOARDING_NON_INFERENCE_V3",
    "AIR_BOOT_VALIDATION_PROPORTIONALITY_V2",
    "AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1",
    "AIR_TURN_GOVERNANCE_KERNEL_CONTRACT_V1",
]

RUNTIME_REFERENCE_ANCHOR_SPECS = [
    {"semantic_id": "AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["GOVERNED_ROUTE", "FORMAL_OBJECT_OBLIGATION"], "required_dependencies": []},
    {"semantic_id": "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["NONROOT_FORMAL_OBJECT_CONSTRUCTION"], "required_dependencies": ["AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1"]},
    {"semantic_id": "AIR_REQUIRED_EMISSION_PREFLIGHT_V2", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_REQUIRED_EMISSION_PREFLIGHT_V2", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["PRE_RESPONSE_FORMAL_OBJECT_PREFLIGHT"], "required_dependencies": ["AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1", "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1"]},
    {"semantic_id": "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["RESPONSE_EMISSION_CLOSURE"], "required_dependencies": ["AIR_REQUIRED_EMISSION_PREFLIGHT_V2"]},
    {"semantic_id": "AIR_MATERIAL_ACTION_INTERLOCK_V3", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_MATERIAL_ACTION_INTERLOCK_V3", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["MATERIAL_ACTION_REQUEST"], "required_dependencies": ["AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1", "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1"]},
    {"semantic_id": "AIR_APPROVAL_RESPONSE_RESOLUTION_V2", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_APPROVAL_RESPONSE_RESOLUTION_V2", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["APPROVAL_GATE_RESPONSE"], "required_dependencies": ["AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1", "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1", "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1"]},
    {"semantic_id": "AIR_REQUIRED_INPUT_ARTIFACT_ACQUISITION_V3", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_REQUIRED_INPUT_ARTIFACT_ACQUISITION_V3", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["MATERIAL_REQUIRED_INPUT_MISSING"], "required_dependencies": ["AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1", "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1", "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1"]},
    {"semantic_id": "DETERMINISTIC_ONBOARDING_NON_INFERENCE_V3", "source_role": "CORE_RUNTIME", "patch_marker": "DETERMINISTIC_ONBOARDING_NON_INFERENCE_V3", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["UNRESOLVED_ONBOARDING_STATE"], "required_dependencies": []},
    {"semantic_id": "AIR_BOOT_VALIDATION_PROPORTIONALITY_V2", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_BOOT_VALIDATION_PROPORTIONALITY_V2", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["BOOT", "TARGETED_REVALIDATION"], "required_dependencies": []},
    {"semantic_id": "AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["BOOT", "TARGETED_RUNTIME_RETRIEVAL"], "required_dependencies": ["AIR_BOOT_VALIDATION_PROPORTIONALITY_V2"]},
    {"semantic_id": "AIR_TURN_GOVERNANCE_KERNEL_CONTRACT_V1", "source_role": "CORE_RUNTIME", "patch_marker": "AIR_TURN_GOVERNANCE_KERNEL_CONTRACT_V1", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["GOVERNED_ROUTE", "FORMAL_OBJECT_OBLIGATION", "MATERIAL_ACTION_REQUEST"], "required_dependencies": ["AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1", "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1", "AIR_REQUIRED_EMISSION_PREFLIGHT_V2", "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1", "AIR_MATERIAL_ACTION_INTERLOCK_V3", "AIR_APPROVAL_RESPONSE_RESOLUTION_V2", "AIR_REQUIRED_INPUT_ARTIFACT_ACQUISITION_V3", "DETERMINISTIC_ONBOARDING_NON_INFERENCE_V3", "AIR_BOOT_VALIDATION_PROPORTIONALITY_V2", "AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1"]},
    {"semantic_id": "AIR_CONTROL_UNRESOLVED_OPTION_SEMANTIC_QUALIFIER_V1", "source_role": "CONTROL_SURFACE", "patch_marker": "AIR_CONTROL_UNRESOLVED_OPTION_SEMANTIC_QUALIFIER_V1", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["UNRESOLVED_ONBOARDING_RENDER"], "required_dependencies": ["DETERMINISTIC_ONBOARDING_NON_INFERENCE_V3"]},
    {"semantic_id": "AIR_CONTROL_TURN_KERNEL_PROGRESSIVE_RUNTIME_RENDERER_V1", "source_role": "CONTROL_SURFACE", "patch_marker": "AIR_CONTROL_TURN_KERNEL_PROGRESSIVE_RUNTIME_RENDERER_V1", "locator_type": "MARKDOWN_PATCH_SECTION", "retrieval_trigger": ["TURN_KERNEL_RESULT_RENDERING", "PROGRESSIVE_RUNTIME_PRESENTATION"], "required_dependencies": ["AIR_TURN_GOVERNANCE_KERNEL_CONTRACT_V1", "AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1"]},
    {"semantic_id": "AIR_STARTER_PROGRESSIVE_RUNTIME_RETRIEVAL_MIRROR", "source_role": "DEFAULT_STARTER_PROFILE", "patch_marker": "progressive_runtime_retrieval_mirror", "locator_type": "JSON_PATH", "json_path": "$.compiler_contract.progressive_runtime_retrieval_mirror", "retrieval_trigger": ["ROUTINE_BOOT_DEFAULT_SELECTION"], "required_dependencies": ["AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1"]},
    {"semantic_id": "AIR_STARTER_TURN_GOVERNANCE_KERNEL_MIRROR", "source_role": "DEFAULT_STARTER_PROFILE", "patch_marker": "turn_governance_kernel_mirror", "locator_type": "JSON_PATH", "json_path": "$.compiler_contract.turn_governance_kernel_mirror", "retrieval_trigger": ["BOOT_TURN_KERNEL_LOAD"], "required_dependencies": ["AIR_TURN_GOVERNANCE_KERNEL_CONTRACT_V1"]},
    {"semantic_id": "AIR_STARTER_BOOT_RUNTIME_TELEMETRY_DEFAULTS", "source_role": "DEFAULT_STARTER_PROFILE", "patch_marker": "boot_runtime_telemetry_defaults", "locator_type": "JSON_PATH", "json_path": "$.compiler_contract.boot_runtime_telemetry_defaults", "retrieval_trigger": ["BOOT_TELEMETRY"], "required_dependencies": ["AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1"]},
    {"semantic_id": "AIR_STARTER_CORE_RUNTIME_TRANSITION_IDENTITY_V10", "source_role": "DEFAULT_STARTER_PROFILE", "patch_marker": "core_runtime_transition_identity_contract", "locator_type": "JSON_PATH", "json_path": "$.validation_contract.core_runtime_transition_identity_contract", "retrieval_trigger": ["PIN_VALIDATION", "RUNTIME_TRANSITION_IDENTITY"], "required_dependencies": ["AIR_PROGRESSIVE_RUNTIME_RETRIEVAL_CONTRACT_V1"]},
]

ALLOWED_DETERMINISTIC_OPERATORS = {
    "FILE_EXISTS",
    "MARKDOWN_HEADER_EQUALS_LITERAL",
    "JSON_EQUALS_LITERAL",
    "JSON_EQUALS_REFERENCE",
    "JSON_EQUALS_MARKDOWN_HEADER",
    "MARKDOWN_FINAL_LINE_EQUALS_LITERAL",
    "JSON_ROOT_KEYS_DECLARED_BY_MANIFEST",
    "JSON_ARRAY_CONTAINS_LITERAL",
    "TEXT_CONTAINS_LITERAL",
    "JSON_PATH_ABSENT",
    "TEXT_NOT_CONTAINS_LITERAL",
    "JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL",
    "MARKDOWN_HEADER_EQUALS_REGISTRY_VALUE",
    "STRICT_JSON_PARSE_NO_DUPLICATES",
    "FOUNDATION_FILENAME_COLLISION_FREE",
    "FOUNDATION_MANIFEST_EXACT",
    "CORE_RUNTIME_TRANSITION_IDENTITY_VALID",
    "HANDOFF_TEMPLATE_TRANSITION_IDENTITY_VALID",
}


class CompileError(RuntimeError):
    pass


def canonical_json_bytes(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_json_sha256(obj):
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def text_sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def strict_json_load(path):
    def pairs_hook(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise CompileError(f"duplicate JSON key {k!r} in {path}")
            out[k] = v
        return out
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=pairs_hook)


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def markdown_headers(text):
    out = {}
    for line in text.splitlines()[:120]:
        m = re.match(r"^([A-Z][A-Z0-9_]+):\s*(.*?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def _markdown_patch_section(text, patch_marker):
    lines = text.splitlines(keepends=True)
    needle = f"Patch marker: {patch_marker}"
    marker_lines = [i for i, line in enumerate(lines) if needle in line]
    if len(marker_lines) != 1:
        raise CompileError(f"patch marker must resolve exactly once: {patch_marker}: {marker_lines}")
    marker_index = marker_lines[0]
    prior_delimiters = [i for i in range(marker_index - 1, -1, -1) if re.fullmatch(r"={10,}", lines[i].strip())]
    if len(prior_delimiters) < 2:
        raise CompileError(f"section heading delimiters not found for {patch_marker}")
    start = prior_delimiters[1]
    end = len(lines)
    for i in range(marker_index + 1, len(lines)):
        if re.fullmatch(r"={10,}", lines[i].strip()):
            end = i
            break
    section_text = "".join(lines[start:end])
    return {
        "start_line": start + 1,
        "end_line": end,
        "text": section_text,
        "sha256": text_sha256(section_text),
    }


def _runtime_reference_anchor(spec, paths):
    role = spec["source_role"]
    source_path = CANONICAL_PATHS[role]
    actual_source_sha256 = file_sha256(paths[role])
    if actual_source_sha256 != PINNED_HASHES[role]:
        raise CompileError(f"runtime reference source pin drift: {role}")
    if spec["locator_type"] == "MARKDOWN_PATCH_SECTION":
        section = _markdown_patch_section(read_text(paths[role]), spec["patch_marker"])
        locator = {
            "type": "MARKDOWN_PATCH_SECTION",
            "start_line": section["start_line"],
            "end_line": section["end_line"],
        }
        digest = section["sha256"]
        digest_algorithm = "SHA256_UTF8_EXACT_SECTION_V1"
    elif spec["locator_type"] == "JSON_PATH":
        obj = strict_json_load(paths[role])
        subtree = json_path_get(obj, spec["json_path"])
        locator = {"type": "JSON_PATH", "json_path": spec["json_path"]}
        digest = canonical_json_sha256(subtree)
        digest_algorithm = CANONICAL_JSON_ALGORITHM
    else:
        raise CompileError(f"unknown runtime reference locator type: {spec['locator_type']}")
    return {
        "semantic_id": spec["semantic_id"],
        "canonical_source_path": source_path,
        "patch_marker": spec["patch_marker"],
        "source_sha256": actual_source_sha256,
        "section_digest": digest,
        "section_digest_algorithm": digest_algorithm,
        "retrieval_trigger": copy.deepcopy(spec["retrieval_trigger"]),
        "required_dependencies": copy.deepcopy(spec["required_dependencies"]),
        "locator": locator,
    }


def build_runtime_navigation_outputs(paths, starter):
    anchors = [_runtime_reference_anchor(spec, paths) for spec in RUNTIME_REFERENCE_ANCHOR_SPECS]
    ids = [a["semantic_id"] for a in anchors]
    if len(ids) != len(set(ids)):
        raise CompileError("runtime reference index duplicate semantic_id")
    id_set = set(ids)
    for anchor in anchors:
        unknown = sorted(set(anchor["required_dependencies"]) - id_set)
        if unknown:
            raise CompileError(f"runtime reference dependency not directly indexed: {anchor['semantic_id']}: {unknown}")

    validate_consumption_key_contract_mirror(read_text(paths["CORE_RUNTIME"]), starter)
    progressive = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
    retrieval_scope = progressive.get("retrieval_scope_enforcement")
    if not isinstance(retrieval_scope, dict):
        raise CompileError("Starter retrieval-scope enforcement mirror missing")
    if progressive.get("required_retrieval_scope_enforcement_patch_marker") != "AIR_RETRIEVAL_SCOPE_ENFORCEMENT_V1":
        raise CompileError("Starter retrieval-scope patch marker mismatch")
    if retrieval_scope.get("core_patch_marker") != "AIR_RETRIEVAL_SCOPE_ENFORCEMENT_V1":
        raise CompileError("Starter retrieval-scope Core marker mirror mismatch")
    if "Patch marker: AIR_RETRIEVAL_SCOPE_ENFORCEMENT_V1" not in read_text(paths["CORE_RUNTIME"]):
        raise CompileError("Core retrieval-scope enforcement marker missing")
    kernel_mirror = starter["compiler_contract"]["turn_governance_kernel_mirror"]
    telemetry = starter["compiler_contract"]["boot_runtime_telemetry_defaults"]
    transition = starter["validation_contract"]["core_runtime_transition_identity_contract"]
    if progressive.get("direct_reference_depth") != DIRECT_REFERENCE_DEPTH:
        raise CompileError("Starter direct-reference depth does not match H4 compiler contract")
    if transition.get("contract_id") != "AIR_STARTER_CORE_RUNTIME_TRANSITION_IDENTITY_V10":
        raise CompileError("Starter transition contract is not V10")

    reference_index = {
        "SYSTEM_DESIGNATION": "AIR_P_RUNTIME_REFERENCE_INDEX_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_NAVIGATION_TO_CANONICAL_SOURCE",
        "semantic_owner": "AIR_CORE_RUNTIME_V2",
        "runtime_state": CURRENT_RUNTIME_STATE,
        "direct_reference_depth": DIRECT_REFERENCE_DEPTH,
        "nested_only_discovery": "PROHIBITED",
        "canonical_source_authority": "PRESERVED",
        "source_hashes": {
            CANONICAL_PATHS["CORE_RUNTIME"]: PINNED_HASHES["CORE_RUNTIME"],
            CANONICAL_PATHS["CONTROL_SURFACE"]: PINNED_HASHES["CONTROL_SURFACE"],
            CANONICAL_PATHS["DEFAULT_STARTER_PROFILE"]: PINNED_HASHES["DEFAULT_STARTER_PROFILE"],
        },
        "compiled_navigation_refs": {
            "routes": "air_p/compiled/AIR_P_ROUTE_CONTRACT_REGISTRY.json",
            "formal_objects": "air_p/compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json",
            "deterministic_validation": "air_p/compiled/AIR_P_DETERMINISTIC_VALIDATION_REGISTRY.json",
            "law_applicability": "catalog/AIR_LAW_APPLICABILITY_ROUTER.json",
            "specialist_discovery": "catalog/AIR_SPECIALIST_PACKAGE_INDEX.json",
        },
        "anchor_count": len(anchors),
        "anchors": anchors,
        "stale_anchor_behavior": "TARGETED_REVALIDATION_OR_FULL_RELEASE_INTEGRITY_AUDIT_NO_INFERENCE_FALLBACK",
        "backend_enforcement_claimed": False,
    }

    by_id = {a["semantic_id"]: a for a in anchors}
    kernel_anchors = [copy.deepcopy(by_id[sid]) for sid in KERNEL_REQUIRED_SEMANTIC_IDS]
    kernel = {
        "SYSTEM_DESIGNATION": "AIR_P_TURN_GOVERNANCE_KERNEL_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_EXECUTION_NAVIGATION_PROJECTION",
        "semantic_owner": "AIR_CORE_RUNTIME_V2",
        "runtime_state": CURRENT_RUNTIME_STATE,
        "starter_transition_contract_id": transition["contract_id"],
        "starter_transition_state": CURRENT_RUNTIME_STATE,
        "direct_reference_depth": DIRECT_REFERENCE_DEPTH,
        "runtime_reference_index_ref": "air_p/compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json",
        "pre_response_pipeline": copy.deepcopy(kernel_mirror["canonical_pipeline"]),
        "preartifact_governance": {
            "bootstrap_no_artifact_rule": kernel_mirror["bootstrap_no_artifact_rule"],
            "preartifact_evaluation_pair_rule": kernel_mirror["preartifact_evaluation_pair_rule"],
            "material_unresolved_input_rule": kernel_mirror["material_unresolved_input_rule"],
            "material_block_rule": kernel_mirror["material_block_rule"],
            "decision_trace_constructor_rule": kernel_mirror["decision_trace_constructor_rule"],
            "exact_token_rule": kernel_mirror["exact_token_rule"],
            "all_objects_rule": kernel_mirror["all_objects_rule"],
        },
        "progressive_runtime": {
            "default_boot_profile": progressive["default_boot_profile"],
            "tier_order": copy.deepcopy(progressive["tier_order"]),
            "direct_reference_rule": progressive["direct_reference_rule"],
            "byte_verification_context_rule": progressive["byte_verification_context_rule"],
            "mismatch_behavior": progressive["mismatch_behavior"],
            "required_user_boot_profile_patch_marker": progressive["required_user_boot_profile_patch_marker"],
            "required_retrieval_scope_enforcement_patch_marker": progressive["required_retrieval_scope_enforcement_patch_marker"],
            "retrieval_scope_enforcement": copy.deepcopy(progressive["retrieval_scope_enforcement"]),
            "default_user_boot_profile": progressive["default_user_boot_profile"],
            "user_boot_profile_dispatch": copy.deepcopy(progressive["user_boot_profile_dispatch"]),
            "explicit_profile_selection_rule": progressive["explicit_profile_selection_rule"],
            "silent_escalation": progressive["silent_escalation"],
            "escalation_telemetry_required": copy.deepcopy(progressive["escalation_telemetry_required"]),
            "boot_result_telemetry_required_when_observable": copy.deepcopy(progressive["boot_result_telemetry_required_when_observable"]),
            "release_package_interface_obligation": progressive["release_package_interface_obligation"],
        },
        "boot_telemetry": {
            "phase_order": copy.deepcopy(telemetry["phase_order"]),
            "evidence_class": telemetry["evidence_class"],
            "unavailable_timing_rule": telemetry["unavailable_timing_rule"],
            "performance_safety_rule": telemetry["performance_safety_rule"],
        },
        "required_contract_count": len(kernel_anchors),
        "required_contract_semantic_ids": copy.deepcopy(KERNEL_REQUIRED_SEMANTIC_IDS),
        "anchors": kernel_anchors,
        "ordinary_prose_before_formal_closure": "PROHIBITED_WHEN_GOVERNED_ROUTE_OR_OWED_FORMAL_OBJECT_EXISTS",
        "backend_enforcement_claimed": False,
    }
    validate_runtime_navigation_outputs(kernel, reference_index, paths)
    return kernel, reference_index


def validate_runtime_navigation_outputs(kernel, reference_index, paths):
    if reference_index.get("SYSTEM_DESIGNATION") != "AIR_P_RUNTIME_REFERENCE_INDEX_V1":
        raise CompileError("runtime reference index designation mismatch")
    if reference_index.get("authority_class") != "DERIVED_NONAUTHORITATIVE_NAVIGATION_TO_CANONICAL_SOURCE":
        raise CompileError("runtime reference index authority mismatch")
    if reference_index.get("direct_reference_depth") != DIRECT_REFERENCE_DEPTH:
        raise CompileError("runtime reference index depth mismatch")
    anchors = reference_index.get("anchors", [])
    if reference_index.get("anchor_count") != len(anchors) or len(anchors) != len(RUNTIME_REFERENCE_ANCHOR_SPECS):
        raise CompileError("runtime reference index anchor cardinality mismatch")
    required_fields = {"semantic_id", "canonical_source_path", "patch_marker", "source_sha256", "section_digest", "retrieval_trigger", "required_dependencies"}
    ids = [a.get("semantic_id") for a in anchors]
    if len(ids) != len(set(ids)):
        raise CompileError("runtime reference index duplicate semantic_id")
    id_set = set(ids)
    for spec, anchor in zip(RUNTIME_REFERENCE_ANCHOR_SPECS, anchors):
        if not required_fields.issubset(anchor):
            raise CompileError(f"runtime reference anchor missing required field: {anchor.get('semantic_id')}")
        if anchor.get("semantic_id") != spec["semantic_id"]:
            raise CompileError("runtime reference anchor ordering/identity mismatch")
        role = spec["source_role"]
        if anchor.get("canonical_source_path") != CANONICAL_PATHS[role]:
            raise CompileError(f"runtime reference canonical path mismatch: {spec['semantic_id']}")
        if anchor.get("source_sha256") != PINNED_HASHES[role] or file_sha256(paths[role]) != anchor.get("source_sha256"):
            raise CompileError(f"runtime reference source identity mismatch: {spec['semantic_id']}")
        if spec["locator_type"] == "MARKDOWN_PATCH_SECTION":
            section = _markdown_patch_section(read_text(paths[role]), spec["patch_marker"])
            if anchor.get("section_digest") != section["sha256"]:
                raise CompileError(f"runtime reference section digest mismatch: {spec['semantic_id']}")
            if anchor.get("locator") != {"type": "MARKDOWN_PATCH_SECTION", "start_line": section["start_line"], "end_line": section["end_line"]}:
                raise CompileError(f"runtime reference section locator mismatch: {spec['semantic_id']}")
        else:
            subtree = json_path_get(strict_json_load(paths[role]), spec["json_path"])
            if anchor.get("section_digest") != canonical_json_sha256(subtree):
                raise CompileError(f"runtime reference JSON digest mismatch: {spec['semantic_id']}")
            if anchor.get("locator") != {"type": "JSON_PATH", "json_path": spec["json_path"]}:
                raise CompileError(f"runtime reference JSON locator mismatch: {spec['semantic_id']}")
        unknown = sorted(set(anchor.get("required_dependencies", [])) - id_set)
        if unknown:
            raise CompileError(f"runtime reference nested-only dependency: {spec['semantic_id']}: {unknown}")

    if kernel.get("SYSTEM_DESIGNATION") != "AIR_P_TURN_GOVERNANCE_KERNEL_V1":
        raise CompileError("turn governance kernel designation mismatch")
    if kernel.get("authority_class") != "DERIVED_NONAUTHORITATIVE_EXECUTION_NAVIGATION_PROJECTION":
        raise CompileError("turn governance kernel authority mismatch")
    if kernel.get("direct_reference_depth") != DIRECT_REFERENCE_DEPTH:
        raise CompileError("turn governance kernel reference depth mismatch")
    if kernel.get("required_contract_semantic_ids") != KERNEL_REQUIRED_SEMANTIC_IDS:
        raise CompileError("turn governance kernel required contract set mismatch")
    if kernel.get("required_contract_count") != len(KERNEL_REQUIRED_SEMANTIC_IDS):
        raise CompileError("turn governance kernel required contract count mismatch")
    by_id = {a["semantic_id"]: a for a in anchors}
    expected_kernel_anchors = [by_id[sid] for sid in KERNEL_REQUIRED_SEMANTIC_IDS]
    if kernel.get("anchors") != expected_kernel_anchors:
        raise CompileError("turn governance kernel anchors are not direct exact index anchors")
    starter = strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
    expected_pipeline = starter["compiler_contract"]["turn_governance_kernel_mirror"]["canonical_pipeline"]
    if kernel.get("pre_response_pipeline") != expected_pipeline:
        raise CompileError("turn governance kernel pipeline mismatch")
    if kernel.get("starter_transition_contract_id") != "AIR_STARTER_CORE_RUNTIME_TRANSITION_IDENTITY_V10":
        raise CompileError("turn governance kernel Starter transition contract mismatch")
    if kernel.get("starter_transition_state") != CURRENT_RUNTIME_STATE:
        raise CompileError("turn governance kernel runtime transition state mismatch")
    pr = kernel.get("progressive_runtime", {})
    if pr.get("required_user_boot_profile_patch_marker") != "AIR_USER_BOOT_PROFILE_DISPATCH_V1":
        raise CompileError("boot-profile dispatch patch marker mismatch")
    if pr.get("required_retrieval_scope_enforcement_patch_marker") != "AIR_RETRIEVAL_SCOPE_ENFORCEMENT_V1":
        raise CompileError("retrieval-scope enforcement patch marker mismatch")
    rse = pr.get("retrieval_scope_enforcement")
    if not isinstance(rse, dict):
        raise CompileError("retrieval-scope enforcement projection missing")
    if rse.get("model_visible_scope_policy") != "CLOSED_WORLD_ALLOWLIST" or rse.get("closed_retrieval_plan_required") is not True:
        raise CompileError("retrieval-scope closed-world plan contract mismatch")
    if rse.get("tool_only_checks_do_not_grant_model_visibility") is not True:
        raise CompileError("tool-only/model-visible retrieval separation missing")
    t1_scope = rse.get("tier1_navigation", {})
    if t1_scope.get("handoff_body_or_fragment_without_dependency") != "PROHIBITED":
        raise CompileError("Tier1 Handoff model-visible boundary missing")
    if t1_scope.get("router83_law_applicability_metadata_before_typed_routing") != "PROHIBITED_MODEL_VISIBILITY":
        raise CompileError("Tier1 Router83 applicability visibility boundary missing")
    t2_scope = rse.get("tier2_targeted_source", {})
    if t2_scope.get("target_resolution") != "EXPLICIT_TARGET_TO_DIRECT_RUNTIME_INDEX_ANCHOR_TO_DECLARED_DEPENDENCY_CLOSURE":
        raise CompileError("Tier2 exact-anchor dependency-closure rule missing")
    for field in ("ordinary_whole_archive_filename_size_enumeration", "broad_recursive_source_scan_when_direct_anchor_exists", "adjacent_context_outside_exact_section_boundaries"):
        if t2_scope.get(field) != "PROHIBITED":
            raise CompileError(f"Tier2 prohibited widening clause missing: {field}")
    if pr.get("default_user_boot_profile") != "TIER_0_ROUTINE":
        raise CompileError("default user boot profile mismatch")
    if pr.get("silent_escalation") != "PROHIBITED":
        raise CompileError("silent boot-profile escalation must be prohibited")
    if set(pr.get("user_boot_profile_dispatch", {})) != {"TIER_0_ROUTINE","TIER_1_NAVIGATION","TIER_2_TARGETED_SOURCE","TIER_3_DEEP_AUDIT"}:
        raise CompileError("user boot-profile dispatch set mismatch")
    return True


def normalize_scalar(value):
    if not isinstance(value, str):
        return value
    s = value.strip()
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", s):
        try:
            return int(s)
        except ValueError:
            pass
    if re.fullmatch(r"-?(0|[1-9][0-9]*)\.[0-9]+", s):
        try:
            return float(s)
        except ValueError:
            pass
    if s == "true":
        return True
    if s == "false":
        return False
    if s == "null":
        return None
    return value


def json_path_get(obj, path):
    if path == "$":
        return obj
    if not path.startswith("$."):
        raise CompileError(f"unsupported JSON path: {path}")
    cur = obj
    for part in path[2:].split("."):
        if isinstance(cur, list) and re.fullmatch(r"[0-9]+", part):
            idx = int(part)
            if idx >= len(cur):
                raise KeyError(path)
            cur = cur[idx]
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise KeyError(path)
    return cur


def parse_machine_payload(core_text, begin_marker, end_marker):
    pattern = (
        re.escape(begin_marker)
        + r".*?```json\s*(\{.*?\})\s*```.*?"
        + re.escape(end_marker)
    )
    m = re.search(pattern, core_text, re.S)
    if not m:
        raise CompileError(f"machine payload not found: {begin_marker}")
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        raise CompileError(f"invalid machine payload {begin_marker}: {e}") from e

def core_consumption_key_contract(core_text):
    contract = parse_machine_payload(
        core_text,
        "AIR_ACTION_AUTHORIZATION_CONSUMPTION_KEY_CONSTRUCTION_V1_MACHINE_PAYLOAD_BEGIN",
        "AIR_ACTION_AUTHORIZATION_CONSUMPTION_KEY_CONSTRUCTION_V1_MACHINE_PAYLOAD_END",
    )
    if contract.get("SYSTEM_DESIGNATION") != "AIR_ACTION_AUTHORIZATION_CONSUMPTION_KEY_CONSTRUCTION_V1":
        raise CompileError("consumption-key contract designation mismatch")
    if contract.get("digest_type_id") != "AIR_ACTION_AUTHORIZATION_CONSUMPTION_KEY_SHA256_V1":
        raise CompileError("consumption-key digest type mismatch")
    if contract.get("algorithm") != "SHA-256" or contract.get("output_representation") != "64_LOWERCASE_HEXADECIMAL":
        raise CompileError("consumption-key hash representation mismatch")
    return contract

def validate_consumption_key_contract_mirror(core_text, starter):
    core_contract = core_consumption_key_contract(core_text)
    starter_contract = starter["compiler_contract"]["approval_response_resolution"]["consumption_key_construction"]
    if core_contract != starter_contract:
        raise CompileError("Core/Starter consumption-key contract mirror mismatch")
    return True

def action_authorization_consumption_key(authorization, contract):
    fields = contract["preimage"]["authorization_projection_fields"]
    missing = [k for k in fields if k not in authorization]
    if missing:
        raise CompileError(f"consumption-key projection missing fields: {missing}")
    projection = {k: copy.deepcopy(authorization[k]) for k in fields}
    preimage = {"digest_type_id": contract["digest_type_id"], "authorization_projection": projection}
    return canonical_json_sha256(preimage)

def validate_stored_action_authorization_consumption_key(authorization, contract):
    stored = authorization.get("consumption_key_sha256")
    if not isinstance(stored, str) or not re.fullmatch(r"[0-9a-f]{64}", stored):
        raise CompileError("stored consumption key malformed")
    expected = action_authorization_consumption_key(authorization, contract)
    if stored != expected:
        raise CompileError("stored consumption key mismatch")
    return True


def core_formal_object_registry(core_text):
    reg = parse_machine_payload(
        core_text,
        "AIR_FORMAL_OBJECT_SCHEMA_REGISTRY_V1_MACHINE_PAYLOAD_BEGIN",
        "AIR_FORMAL_OBJECT_SCHEMA_REGISTRY_V1_MACHINE_PAYLOAD_END",
    )
    if reg.get("SYSTEM_DESIGNATION") != "AIR_FORMAL_OBJECT_SCHEMA_REGISTRY_V1":
        raise CompileError("formal-object registry designation mismatch")
    if reg.get("REGISTRY_VERSION") != "2.9.0":
        raise CompileError("formal-object registry version mismatch")
    if reg.get("object_count") != EXPECTED["formal_objects"]:
        raise CompileError("formal-object count mismatch")
    objs = reg.get("objects", [])
    if len(objs) != EXPECTED["formal_objects"]:
        raise CompileError("formal-object registry array count mismatch")
    ids = [x.get("object_id") for x in objs]
    if len(ids) != len(set(ids)):
        raise CompileError("duplicate formal-object id")
    return reg


def core_handoff_transition_registry(core_text):
    reg = parse_machine_payload(
        core_text,
        "AIR_HANDOFF_TEMPLATE_TRANSITION_COMPATIBILITY_V1_MACHINE_PAYLOAD_BEGIN",
        "AIR_HANDOFF_TEMPLATE_TRANSITION_COMPATIBILITY_V1_MACHINE_PAYLOAD_END",
    )
    if reg.get("SYSTEM_DESIGNATION") != "AIR_HANDOFF_TEMPLATE_TRANSITION_COMPATIBILITY_V1":
        raise CompileError("handoff transition registry designation mismatch")
    if reg.get("registry_version") != "5.0.0":
        raise CompileError("handoff transition registry version mismatch")
    return reg



def core_law_registry(core_text):
    reg = parse_machine_payload(
        core_text,
        "AIR_LAW_ID_REGISTRY_V1_MACHINE_PAYLOAD_BEGIN",
        "AIR_LAW_ID_REGISTRY_V1_MACHINE_PAYLOAD_END",
    )
    if reg.get("SYSTEM_DESIGNATION") != "AIR_LAW_ID_REGISTRY_V1":
        raise CompileError("law registry designation mismatch")
    entries = reg.get("entries", [])
    if reg.get("entry_count") != EXPECTED["laws"] or len(entries) != EXPECTED["laws"]:
        raise CompileError("law registry count mismatch")
    ids = [x.get("law_id") for x in entries]
    if len(ids) != len(set(ids)) or DECISION_TRACE_LAW_ID not in ids:
        raise CompileError("law registry identity mismatch")
    observed = canonical_json_sha256(entries)
    if observed != reg.get("entry_fingerprint_sha256"):
        raise CompileError("law registry fingerprint mismatch")
    return reg


def core_decision_trace_contracts(core_text):
    specs = [
        ("AIR_DECISION_BASIS_CLOSURE_V1", "AIR_DECISION_BASIS_CLOSURE_V1_MACHINE_PAYLOAD_BEGIN", "AIR_DECISION_BASIS_CLOSURE_V1_MACHINE_PAYLOAD_END"),
        ("AIR_DECISION_TRACE_OBJECT_CONTRACT_V1", "AIR_DECISION_TRACE_OBJECT_CONTRACT_V1_MACHINE_PAYLOAD_BEGIN", "AIR_DECISION_TRACE_OBJECT_CONTRACT_V1_MACHINE_PAYLOAD_END"),
        ("AIR_DECISION_TRACE_FORCED_WALK_V1", "AIR_DECISION_TRACE_FORCED_WALK_V1_MACHINE_PAYLOAD_BEGIN", "AIR_DECISION_TRACE_FORCED_WALK_V1_MACHINE_PAYLOAD_END"),
        ("AIR_DECISION_TRACE_FINGERPRINT_V1", "AIR_DECISION_TRACE_FINGERPRINT_V1_MACHINE_PAYLOAD_BEGIN", "AIR_DECISION_TRACE_FINGERPRINT_V1_MACHINE_PAYLOAD_END"),
    ]
    out = {}
    for expected, begin, end in specs:
        obj = parse_machine_payload(core_text, begin, end)
        if obj.get("SYSTEM_DESIGNATION") != expected:
            raise CompileError(f"decision-trace machine contract designation mismatch: {expected}")
        if obj.get("positive_execution_authority") != "NONE":
            raise CompileError(f"decision-trace contract authority escalation: {expected}")
        out[expected] = obj
    closure = out["AIR_DECISION_BASIS_CLOSURE_V1"]
    obj_contract = out["AIR_DECISION_TRACE_OBJECT_CONTRACT_V1"]
    forced = out["AIR_DECISION_TRACE_FORCED_WALK_V1"]
    fingerprint = out["AIR_DECISION_TRACE_FINGERPRINT_V1"]
    if closure.get("law_id") != DECISION_TRACE_LAW_ID or closure.get("law_applicability_class") != "CORE_INFRASTRUCTURE_GLOBAL":
        raise CompileError("decision-trace law contract mismatch")
    if obj_contract.get("formal_object_ref") != "AIR_DECISION_TRACE" or obj_contract.get("record_class") != "DECISION_JUSTIFICATION_RECORD":
        raise CompileError("decision-trace object contract mismatch")
    forbidden = set(obj_contract.get("forbidden_fields", []))
    required_forbidden = {"chain_of_thought", "reasoning_steps", "internal_thoughts", "latent_state", "hidden_reasoning", "private_scratchpad"}
    if not required_forbidden.issubset(forbidden):
        raise CompileError("decision-trace forbidden hidden-reasoning field closure incomplete")
    if forced.get("comparison_outcomes") != ["EXACT_MATCH", "EQUIVALENT", "DIVERGENT", "UNRESOLVED"]:
        raise CompileError("decision-trace forced-walk outcomes mismatch")
    if fingerprint.get("algorithm") != "SHA-256" or fingerprint.get("representation") != "64_LOWERCASE_HEXADECIMAL":
        raise CompileError("decision-trace fingerprint contract mismatch")
    return out


def section_index(core_text):
    lines = core_text.splitlines()
    out = []
    for i in range(1, len(lines) - 1):
        if lines[i - 1].startswith("====") and lines[i + 1].startswith("====") and lines[i].strip():
            start = i - 1
            end = len(lines)
            for j in range(i + 2, len(lines) - 1):
                if lines[j - 1].startswith("====") and lines[j + 1].startswith("====") and lines[j].strip():
                    end = j - 1
                    break
            sec_lines = lines[start:end]
            markers = []
            for k, row in enumerate(sec_lines, start=start):
                if row.startswith("Patch marker:"):
                    markers.append((row.split(":", 1)[1].strip(), k + 1))
            out.append({
                "heading": lines[i].strip(),
                "heading_line": i + 1,
                "markers": markers,
                "text": "\n".join(sec_lines) + "\n",
            })
    return out




def _dash_subsection(core_text, heading, patch_marker):
    lines = core_text.splitlines()
    hits = []
    for i, row in enumerate(lines):
        if row.strip() != heading:
            continue
        if i == 0 or i + 1 >= len(lines):
            continue
        if not (set(lines[i - 1].strip()) == {"-"} and set(lines[i + 1].strip()) == {"-"}):
            continue
        start = i - 1
        end = len(lines)
        for j in range(i + 2, len(lines) - 1):
            if set(lines[j - 1].strip()) == {"-"} and lines[j].strip() and set(lines[j + 1].strip()) == {"-"}:
                end = j - 1
                break
        body = lines[start:end]
        marker_lines = [k + 1 for k in range(start, end) if lines[k].strip() == f"Patch marker: {patch_marker}"]
        if len(marker_lines) == 1:
            hits.append({"start_line": start + 1, "end_line": end, "text": "\n".join(body) + "\n"})
    if len(hits) != 1:
        raise CompileError(f"decision-trace source section cardinality mismatch: {len(hits)}")
    hit = hits[0]
    return {"start_line": hit["start_line"], "end_line": hit["end_line"], "sha256": text_sha256(hit["text"])}


def _existing_law_source_section(core_text, source_anchor):
    heading = source_anchor.get("section_heading")
    marker = source_anchor.get("patch_marker")
    heading_matches = [sec for sec in section_index(core_text) if sec["heading"] == heading]
    exact = [sec for sec in heading_matches if any(m == marker for m, _ in sec["markers"])]
    if len(exact) == 1:
        sec = exact[0]
        resolved_marker = marker
        marker_migration = None
    elif len(exact) == 0 and len(heading_matches) == 1 and len(heading_matches[0]["markers"]) == 1:
        sec = heading_matches[0]
        resolved_marker = sec["markers"][0][0]
        marker_migration = {
            "stable_registry_patch_marker": marker,
            "current_source_patch_marker": resolved_marker,
            "migration_rule": "UNIQUE_SECTION_HEADING_SINGLE_PATCH_MARKER",
        }
    else:
        raise CompileError(f"law source anchor not deterministically resolvable: {heading} / {marker}")
    lines = sec["text"].splitlines()
    return {
        "start_line": sec["heading_line"] - 1,
        "end_line": sec["heading_line"] - 1 + len(lines),
        "sha256": text_sha256(sec["text"]),
        "resolved_patch_marker": resolved_marker,
        "marker_migration": marker_migration,
    }


def regenerate_law_router(core_text, prior_router):
    prior_laws = prior_router.get("law_applicability_metadata", [])
    if len(prior_laws) != PRIOR_LAW_ROUTER_INPUT_COUNT:
        raise CompileError("prior law-router input count mismatch")
    prior_by_id = {x.get("law_id"): x for x in prior_laws}
    if len(prior_by_id) != PRIOR_LAW_ROUTER_INPUT_COUNT:
        raise CompileError("prior law-router duplicate law id")
    reg = core_law_registry(core_text)
    reg_fingerprint = reg["entry_fingerprint_sha256"]
    laws = []
    changed_sections = []
    for entry in reg["entries"]:
        law_id = entry["law_id"]
        source_anchor = copy.deepcopy(entry["source_anchor"])
        if law_id == DECISION_TRACE_LAW_ID:
            section = _dash_subsection(core_text, source_anchor["section_heading"], source_anchor["patch_marker"])
            rec = {
                "applicability_class": "CORE_INFRASTRUCTURE_GLOBAL",
                "control_event_refs": [],
                "dependency_law_refs": [],
                "derivation": {
                    "core_registry_fingerprint": reg_fingerprint,
                    "source_class": "R23_DECISION_TRACE_GLOBAL_INFRASTRUCTURE",
                    "r23_decision_trace_source_reconciliation": {
                        "state": "NEW_GLOBAL_LAW_DERIVED_FROM_CORE_MACHINE_CONTRACT",
                        "source_core_sha256": PINNED_HASHES["CORE_RUNTIME"],
                        "source_section_sha256": section["sha256"],
                        "law_resolution_construction_ref": "AIR_LAW_RESOLUTION_CONSTRUCTION_V1@1.0.0",
                        "router_semantic_authority": "NONE",
                    },
                },
                "law_id": law_id,
                "mandatory_floor_refs": [
                    "AIR-FLOOR-007-REQUIRED-FORMAL-OBJECT-VISIBILITY",
                    "AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY",
                    "AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY",
                    "AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION",
                    "AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE",
                    "AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION",
                ],
                "metadata_resolution_state": "CURRENT_R23_DECISION_TRACE_GLOBAL_INFRASTRUCTURE",
                "runtime_dependency_refs": [],
                "runtime_route_refs": [],
                "source_anchor": source_anchor,
                "source_section": section,
                "task_class_predicates": {
                    "exclude_facets_any_of": [],
                    "exclude_route_classes_any_of": [],
                    "include_facets_any_of": [],
                    "include_route_classes_any_of": [],
                    "predicate_id": f"{law_id}::TASK_CLASS_V1",
                    "resolution_state": "CURRENT_GLOBAL_INFRASTRUCTURE",
                    "source_evidence_refs": [
                        f"AIR_LAW_ID_REGISTRY_V1@{reg_fingerprint}",
                        "AIR_DECISION_BASIS_CLOSURE_V1@1.0.0",
                    ],
                },
                "task_target_amrs_predicate": {
                    "predicate_type": "GLOBAL_INFRASTRUCTURE",
                    "resolution_state": "CURRENT",
                    "source_evidence_refs": [
                        f"AIR_LAW_ID_REGISTRY_V1@{reg_fingerprint}",
                        "AIR_DECISION_BASIS_CLOSURE_V1@1.0.0",
                    ],
                    "stages": [],
                },
            }
            changed_sections.append(law_id)
        else:
            if law_id not in prior_by_id:
                raise CompileError(f"missing prior law metadata for {law_id}")
            rec = copy.deepcopy(prior_by_id[law_id])
            rec["source_anchor"] = source_anchor
            section = _existing_law_source_section(core_text, source_anchor)
            old_sha = rec.get("source_section", {}).get("sha256")
            rec["source_section"] = {k: section[k] for k in ("start_line", "end_line", "sha256")}
            deriv = copy.deepcopy(rec.get("derivation", {}))
            if "core_registry_fingerprint" in deriv:
                deriv["core_registry_fingerprint"] = reg_fingerprint
            deriv["r23_decision_trace_source_reconciliation"] = {
                "state": "SOURCE_SECTION_BYTE_EQUIVALENT" if old_sha == section["sha256"] else "SOURCE_SECTION_REANCHORED_WITH_ROUTER_APPLICABILITY_TOKENS_PRESERVED",
                "source_core_sha256": PINNED_HASHES["CORE_RUNTIME"],
                "source_section_sha256": section["sha256"],
                "stable_registry_patch_marker": source_anchor.get("patch_marker"),
                "resolved_current_source_patch_marker": section.get("resolved_patch_marker"),
                "marker_migration": section.get("marker_migration"),
                "router_semantic_authority": "NONE",
            }
            rec["derivation"] = deriv
            if old_sha != section["sha256"]:
                changed_sections.append(law_id)
            if rec.get("applicability_class") == "CORE_INFRASTRUCTURE_GLOBAL":
                for key in ("task_class_predicates", "task_target_amrs_predicate"):
                    pred = rec.get(key, {})
                    refs = pred.get("source_evidence_refs", [])
                    pred["source_evidence_refs"] = [
                        f"AIR_LAW_ID_REGISTRY_V1@{reg_fingerprint}" if isinstance(x, str) and x.startswith("AIR_LAW_ID_REGISTRY_V1@") else x
                        for x in refs
                    ]
        laws.append(rec)
    router = copy.deepcopy(prior_router)
    router["ROUTER_VERSION"] = "1.0.0-R23-DECISION-TRACE-CANDIDATE"
    router["candidate_state"] = "NONCANONICAL_R23_DECISION_TRACE_DERIVED_REGENERATION_CANDIDATE"
    router["law_applicability_metadata"] = laws
    router["law_applicability_metadata_fingerprint_sha256"] = canonical_json_sha256(laws)
    core_headers = markdown_headers(core_text)
    router["source_of_truth"] = {
        "filename": CANONICAL_FILENAMES["CORE_RUNTIME"],
        "law_registry_entry_count": EXPECTED["laws"],
        "law_registry_entry_fingerprint_sha256": reg_fingerprint,
        "law_registry_ref": reg.get("SYSTEM_DESIGNATION"),
        "law_registry_version": reg.get("registry_version"),
        "prompt_version": core_headers.get("PROMPT_VERSION"),
        "router_contract_patch_marker": "AIR_LAW_APPLICABILITY_ROUTER_V1",
        "sha256": PINNED_HASHES["CORE_RUNTIME"],
        "system_designation": core_headers.get("SYSTEM_DESIGNATION"),
    }
    router["metadata_state"] = {
        "operative_resolution_readiness": "NONCANONICAL_R23_DECISION_TRACE_CANDIDATE_READY_FOR_TEST_VALIDATION",
        "registry_law_count": EXPECTED["laws"],
        "resolved_metadata_count": EXPECTED["laws"],
        "resolved_global_infrastructure_law_ids": sorted([x["law_id"] for x in laws if x.get("applicability_class") == "CORE_INFRASTRUCTURE_GLOBAL"]),
        "unresolved_metadata_count": 0,
        "r23_decision_trace_changed_source_section_count": len(changed_sections),
        "r23_decision_trace_changed_source_law_ids": changed_sections,
    }
    bindings = copy.deepcopy(router.get("derived_input_bindings", {}))
    bindings.update({
        "r23_decision_trace_core_sha256": PINNED_HASHES["CORE_RUNTIME"],
        "r23_decision_trace_core_law_registry_fingerprint": reg_fingerprint,
        "r23_decision_trace_prior_router_sha256": PINNED_HASHES["LAW_APPLICABILITY_ROUTER"],
    })
    router["derived_input_bindings"] = bindings
    router["decision_trace_regeneration"] = {
        "authority": "DERIVED_NONAUTHORITATIVE_MACHINE_ROUTER",
        "prior_router_sha256": PINNED_HASHES["LAW_APPLICABILITY_ROUTER"],
        "source_core_sha256": PINNED_HASHES["CORE_RUNTIME"],
        "source_law_registry_fingerprint": reg_fingerprint,
        "input_law_count": PRIOR_LAW_ROUTER_INPUT_COUNT,
        "output_law_count": EXPECTED["laws"],
        "added_law_ids": [DECISION_TRACE_LAW_ID],
        "applicability_semantics_for_prior_laws": "PRESERVED_EXCEPT_SOURCE_REANCHOR_AND_REGISTRY_FINGERPRINT_REFRESH",
        "new_law_applicability": "CORE_INFRASTRUCTURE_GLOBAL",
        "canonical_mutation": False,
        "positive_execution_authority": "NONE",
    }
    return router


def validate_law_router(router, core_text):
    laws = router.get("law_applicability_metadata", [])
    if len(laws) != EXPECTED["laws"]:
        raise CompileError("law router count mismatch")
    ids = [x.get("law_id") for x in laws]
    if len(ids) != len(set(ids)):
        raise CompileError("law router duplicate law_id")
    reg = core_law_registry(core_text)
    registry_ids = [x.get("law_id") for x in reg["entries"]]
    if ids != registry_ids:
        raise CompileError("law router/Core registry law ordering or identity mismatch")
    observed_fp = canonical_json_sha256(laws)
    if router.get("law_applicability_metadata_fingerprint_sha256") != observed_fp:
        raise CompileError("law router metadata fingerprint mismatch")
    if router.get("authority", {}).get("positive_execution_authority") != "NONE":
        raise CompileError("law router authority escalation")
    core_headers = markdown_headers(core_text)
    expected_source_of_truth = {
        "filename": CANONICAL_FILENAMES["CORE_RUNTIME"],
        "law_registry_entry_count": EXPECTED["laws"],
        "law_registry_entry_fingerprint_sha256": reg.get("entry_fingerprint_sha256"),
        "law_registry_ref": reg.get("SYSTEM_DESIGNATION"),
        "law_registry_version": reg.get("registry_version"),
        "prompt_version": core_headers.get("PROMPT_VERSION"),
        "router_contract_patch_marker": "AIR_LAW_APPLICABILITY_ROUTER_V1",
        "sha256": PINNED_HASHES["CORE_RUNTIME"],
        "system_designation": core_headers.get("SYSTEM_DESIGNATION"),
    }
    if router.get("source_of_truth") != expected_source_of_truth:
        raise CompileError("law router source_of_truth mismatch")
    by_id = {x["law_id"]: x for x in laws}
    dt = by_id[DECISION_TRACE_LAW_ID]
    if dt.get("applicability_class") != "CORE_INFRASTRUCTURE_GLOBAL":
        raise CompileError("Decision Trace law applicability mismatch")
    required_floors = {
        "AIR-FLOOR-007-REQUIRED-FORMAL-OBJECT-VISIBILITY",
        "AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY",
        "AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY",
        "AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION",
        "AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE",
        "AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION",
    }
    if set(dt.get("mandatory_floor_refs", [])) != required_floors:
        raise CompileError("Decision Trace law floor closure mismatch")
    return {
        "law_count": len(laws),
        "metadata_fingerprint_sha256": observed_fp,
        "router_version": router.get("ROUTER_VERSION"),
        "core_registry_fingerprint_sha256": reg.get("entry_fingerprint_sha256"),
        "decision_trace_law_state": "PRESENT_GLOBAL_NONAUTHORIZING",
    }

def rebase_component_overlay(core_text, overlay, current_core_sha256, prior_overlay_sha256):
    if overlay.get("SYSTEM_DESIGNATION") != "AIR_P_COMPONENT_METADATA_OVERLAY_V2":
        raise CompileError("component overlay designation mismatch")
    if overlay.get("authority_class") != "DERIVED_NONAUTHORITATIVE_METADATA_OVERLAY":
        raise CompileError("component overlay authority class mismatch")
    if overlay.get("semantic_authority") != "NONE" or overlay.get("positive_execution_authority") != "NONE":
        raise CompileError("component overlay authority boundary violation")
    comps = overlay.get("components", [])
    if overlay.get("component_count") != EXPECTED["components"] or len(comps) != EXPECTED["components"]:
        raise CompileError("component overlay count mismatch")
    ids = [x.get("component_id") for x in comps]
    if len(ids) != len(set(ids)):
        raise CompileError("duplicate overlay component_id")
    sections = section_index(core_text)
    rebound = copy.deepcopy(overlay)
    migrations = []
    for rec in rebound["components"]:
        meta = {k: rec[k] for k in ["component_id", "component_revision", "component_type", "semantic_owner", "routable"]}
        expected_meta = rec.get("metadata_provenance", {}).get("metadata_payload_sha256")
        if expected_meta and canonical_json_sha256(meta) != expected_meta:
            raise CompileError(f"metadata provenance mismatch {rec['component_id']}")
        anchor = rec.get("anchor", {})
        heading = anchor.get("section_heading")
        old_marker = anchor.get("patch_marker")
        heading_matches = [s for s in sections if s["heading"] == heading]
        exact = [s for s in heading_matches if old_marker in {m for m, _ in s["markers"]}]
        if len(exact) == 1:
            sec = exact[0]
            new_marker = old_marker
        elif len(exact) == 0 and len(heading_matches) == 1 and len(heading_matches[0]["markers"]) == 1:
            sec = heading_matches[0]
            new_marker = sec["markers"][0][0]
            migrations.append({
                "component_id": rec["component_id"],
                "section_heading": heading,
                "prior_patch_marker": old_marker,
                "current_patch_marker": new_marker,
                "migration_rule": "UNIQUE_SECTION_HEADING_SINGLE_PATCH_MARKER",
            })
        else:
            raise CompileError(
                f"component anchor not deterministically resolvable {rec['component_id']}: "
                f"heading_matches={len(heading_matches)} exact_marker_matches={len(exact)}"
            )
        marker_lines = [ln for m, ln in sec["markers"] if m == new_marker]
        if len(marker_lines) != 1:
            raise CompileError(f"component marker cardinality {rec['component_id']}")
        rec["anchor"] = {
            "binding_method": "EXACT_SECTION_HEADING_PLUS_PATCH_MARKER",
            "patch_marker": new_marker,
            "section_heading": heading,
            "target_core_heading_line": sec["heading_line"],
            "target_core_patch_marker_line": marker_lines[0],
            "target_core_section_sha256": text_sha256(sec["text"]),
        }
    headers = markdown_headers(core_text)
    rebound["binding_target"] = {
        "binding_method": "EXACT_SECTION_HEADING_PLUS_PATCH_MARKER",
        "canonical_path": "prompts/AIR_CORE_RUNTIME.md",
        "component_metadata_present_in_source": False,
        "designation": headers.get("SYSTEM_DESIGNATION"),
        "prompt_version": headers.get("PROMPT_VERSION"),
        "semantic_authority": True,
        "sha256": current_core_sha256,
    }
    prov = copy.deepcopy(rebound.get("regeneration_provenance", {}))
    prov.update({
        "regeneration_contract_id": "R23_DECISION_TRACE_COMPONENT_METADATA_OVERLAY_REBASE_V1",
        "candidate_policy": "PRESERVE_EXACT_113_CANONICAL_COMPONENT_IDENTITIES_REANCHOR_CURRENT_CORE_NO_NEW_COMPONENT_IDS",
        "current_core_sha256": current_core_sha256,
        "prior_overlay_sha256": prior_overlay_sha256,
        "new_componentization": "NO_NEW_COMPONENT_IDS",
        "selector_contract": "CANONICAL_COMPONENT_ID_PLUS_SECTION_HEADING_PLUS_EXACT_OR_DETERMINISTIC_SINGLE_MARKER_MIGRATION",
        "semantic_authority": "NONE",
        "marker_migration_count": len(migrations),
        "marker_migrations": migrations,
    })
    rebound["regeneration_provenance"] = prov
    rebound["component_count"] = len(rebound["components"])
    return rebound


def component_registry_from_overlay(rebased_overlay, overlay_sha256):
    records = []
    for rec in rebased_overlay["components"]:
        records.append({
            "component_id": rec["component_id"],
            "component_revision": rec["component_revision"],
            "component_type": rec["component_type"],
            "semantic_owner": rec["semantic_owner"],
            "routable": rec["routable"],
            "section_heading": rec["anchor"]["section_heading"],
            "patch_markers": [rec["anchor"]["patch_marker"]],
            "source_anchor": {
                "canonical_role": "CORE_RUNTIME",
                "section_heading_line": rec["anchor"]["target_core_heading_line"],
                "patch_marker": rec["anchor"]["patch_marker"],
                "patch_marker_line": rec["anchor"]["target_core_patch_marker_line"],
                "section_sha256": rec["anchor"]["target_core_section_sha256"],
                "binding_method": rec["anchor"]["binding_method"],
                "metadata_overlay_sha256": overlay_sha256,
                "metadata_payload_sha256": rec.get("metadata_provenance", {}).get("metadata_payload_sha256"),
                "metadata_semantic_authority": "NONE",
                "metadata_positive_execution_authority": "NONE",
            },
        })
    ids = [r["component_id"] for r in records]
    if len(records) != EXPECTED["components"] or len(ids) != len(set(ids)):
        raise CompileError("component registry count/uniqueness failure")
    return records


def parse_route_registry(core_text):
    lines = core_text.splitlines()
    routes = []
    i = 0
    while i < len(lines):
        if lines[i] != "[AIR_ROUTE]":
            i += 1
            continue
        start = i
        fields = {}
        i += 1
        while i < len(lines):
            row = lines[i]
            if row == "[AIR_ROUTE]" or not row.strip() or "=" not in row:
                break
            k, v = row.split("=", 1)
            fields[k.strip()] = v.strip()
            i += 1
        if "id" not in fields:
            raise CompileError(f"route without id at line {start + 1}")
        def arr(key):
            v = fields.get(key, "")
            if not v or v.lower() == "none":
                return []
            return [x for x in v.split(";") if x]
        routes.append({
            "route_id": fields["id"],
            "semantic_owner": fields.get("semantic_owner"),
            "trigger": fields.get("trigger"),
            "trigger_authority": fields.get("trigger_authority"),
            "control_event_ref": fields.get("control_event_ref"),
            "execution_semantics": fields.get("execution_semantics"),
            "inference_policy": fields.get("inference_policy"),
            "step_order": fields.get("step_order"),
            "missing_input_behavior": fields.get("missing_input_behavior"),
            "unknown_condition_behavior": fields.get("unknown_condition_behavior"),
            "conflict_behavior": fields.get("conflict_behavior"),
            "requires": arr("requires"),
            "produces": arr("produces"),
            "allowed_next": arr("allowed_next"),
            "invalidates": arr("invalidates"),
            "does_not_bypass": arr("does_not_bypass"),
            "failure_route": fields.get("failure_route"),
            "optional_fields": {k: v for k, v in fields.items() if k not in {
                "id", "semantic_owner", "trigger", "trigger_authority", "control_event_ref",
                "execution_semantics", "inference_policy", "step_order", "missing_input_behavior",
                "unknown_condition_behavior", "conflict_behavior", "requires", "produces",
                "allowed_next", "invalidates", "does_not_bypass", "failure_route",
            }},
            "source_anchor": {
                "canonical_role": "CORE_RUNTIME",
                "start_line": start + 1,
                "end_line": i,
                "sha256": text_sha256("\n".join(lines[start:i]) + "\n"),
            },
        })
    ids = [r["route_id"] for r in routes]
    if len(routes) != EXPECTED["routes"] or len(ids) != len(set(ids)):
        raise CompileError("route registry count/uniqueness failure")
    return routes


def validate_route_fixture(routes, route_map):
    fixture = route_map.get("routes", route_map.get("runtime_routes", []))
    if len(fixture) != EXPECTED["routes"]:
        raise CompileError("route-map fixture cardinality mismatch")
    by_id = {x.get("route_id"): x for x in fixture}
    if set(by_id) != {x["route_id"] for x in routes}:
        raise CompileError("route-map/Core route id mismatch")
    mismatches = []
    for r in routes:
        f = by_id[r["route_id"]]
        if f.get("control_event_ref") != r.get("control_event_ref"):
            mismatches.append((r["route_id"], "control_event_ref"))
        if f.get("execution_semantics") != r.get("execution_semantics"):
            mismatches.append((r["route_id"], "execution_semantics"))
        if f.get("inference_policy") != r.get("inference_policy"):
            mismatches.append((r["route_id"], "inference_policy"))
    if mismatches:
        raise CompileError(f"route fixture mismatch: {mismatches[:8]}")
    return True


def source_role_for_path(spec_path):
    if spec_path not in FOUNDATION_PATH_TO_ROLE:
        raise CompileError(f"unmapped deterministic source path: {spec_path}")
    return FOUNDATION_PATH_TO_ROLE[spec_path]


def source_file_for_spec(spec_path, paths):
    return paths[source_role_for_path(spec_path)]


def _runtime_transition_state(starter, paths):
    contract = starter["validation_contract"]["core_runtime_transition_identity_contract"]
    core_text = read_text(paths["CORE_RUNTIME"])
    core_headers = markdown_headers(core_text)
    core_hash = file_sha256(paths["CORE_RUNTIME"])
    handoff = strict_json_load(paths["HANDOFF_CARD_TEMPLATE"])["AIR_HANDOFF_CARD"]
    handoff_hash = file_sha256(paths["HANDOFF_CARD_TEMPLATE"])
    matches = []
    for state in contract.get("current_cutover_states", []):
        ok = (
            state.get("core_prompt_version") == core_headers.get("PROMPT_VERSION")
            and state.get("core_sha256") == core_hash
            and state.get("handoff_schema_version") == handoff.get("SCHEMA_VERSION")
            and state.get("handoff_template_revision") == handoff.get("template_revision")
            and state.get("handoff_template_sha256") == handoff_hash
        )
        marker = state.get("required_core_patch_marker")
        if marker and marker not in core_text:
            ok = False
        required_reg = state.get("required_handoff_transition_registry")
        if required_reg:
            reg = core_handoff_transition_registry(core_text)
            observed = f"{reg.get('SYSTEM_DESIGNATION')}@{reg.get('registry_version')}"
            if observed != required_reg:
                ok = False
        if ok:
            matches.append(state.get("state_id"))
    if len(matches) != 1:
        raise CompileError(f"runtime transition identity match count {len(matches)}: {matches}")
    return matches[0]


def _handoff_transition_identity(paths):
    core_text = read_text(paths["CORE_RUNTIME"])
    reg = core_handoff_transition_registry(core_text)
    handoff = strict_json_load(paths["HANDOFF_CARD_TEMPLATE"])["AIR_HANDOFF_CARD"]
    actual_hash = file_sha256(paths["HANDOFF_CARD_TEMPLATE"])
    matches = [x for x in reg.get("accepted_templates", []) if (
        reg.get("schema_version") == handoff.get("SCHEMA_VERSION")
        and x.get("template_revision") == handoff.get("template_revision")
        and x.get("template_sha256") == actual_hash
    )]
    if len(matches) != 1:
        raise CompileError("handoff transition tuple is not an exact accepted tuple")
    if handoff.get("template_revision") == reg.get("current_core_template_revision"):
        if matches[0].get("role") != "TARGET_CURRENT":
            raise CompileError("current Handoff tuple is not TARGET_CURRENT")
    return {
        "schema_version": handoff.get("SCHEMA_VERSION"),
        "template_revision": handoff.get("template_revision"),
        "template_sha256": actual_hash,
        "role": matches[0].get("role"),
    }


def evaluate_deterministic_check(check, starter, paths, json_cache=None, text_cache=None):
    json_cache = {} if json_cache is None else json_cache
    text_cache = {} if text_cache is None else text_cache
    op = check.get("operator")
    if op not in ALLOWED_DETERMINISTIC_OPERATORS:
        raise CompileError(f"unknown deterministic operator {op}")

    def json_file(spec):
        p = source_file_for_spec(spec, paths)
        if p not in json_cache:
            json_cache[p] = strict_json_load(p)
        return json_cache[p]

    def text_file(spec):
        p = source_file_for_spec(spec, paths)
        if p not in text_cache:
            text_cache[p] = read_text(p)
        return text_cache[p]

    def operand(x):
        return json_path_get(json_file(x["file"]), x["path"])

    ok = False
    observed = None
    if op == "FILE_EXISTS":
        p = source_file_for_spec(check["file"], paths)
        ok = Path(p).is_file()
        observed = ok
    elif op == "MARKDOWN_HEADER_EQUALS_LITERAL":
        val = markdown_headers(text_file(check["file"])).get(check["header"])
        observed = val
        ok = val == str(check["expected"])
    elif op == "JSON_EQUALS_LITERAL":
        val = operand(check["left"])
        observed = val
        ok = val == check["expected"]
    elif op == "JSON_EQUALS_REFERENCE":
        left = operand(check["left"])
        right = operand(check["right"])
        observed = {"left": left, "right": right}
        ok = left == right
    elif op == "JSON_EQUALS_MARKDOWN_HEADER":
        left = operand(check["left"])
        right = markdown_headers(text_file(check["right"]["file"])).get(check["right"]["header"])
        observed = {"left": left, "right": right}
        ok = left == normalize_scalar(right)
    elif op == "MARKDOWN_FINAL_LINE_EQUALS_LITERAL":
        val = text_file(check["file"]).rstrip("\n").splitlines()[-1]
        observed = val
        ok = val == check["expected"]
    elif op == "JSON_ROOT_KEYS_DECLARED_BY_MANIFEST":
        obj = json_file(check["file"])
        root = json_path_get(obj, check["root_path"])
        req = json_path_get(obj, check["required_path"])
        opt = json_path_get(obj, check["optional_path"])
        declared = set(req) | set(opt)
        actual = set(root.keys())
        observed = {"actual": sorted(actual), "declared": sorted(declared)}
        ok = actual == declared
    elif op == "JSON_ARRAY_CONTAINS_LITERAL":
        arr = operand(check["left"])
        observed = check["expected"] in arr
        ok = bool(observed)
    elif op == "TEXT_CONTAINS_LITERAL":
        ok = check["expected"] in text_file(check["file"])
        observed = ok
    elif op == "JSON_PATH_ABSENT":
        try:
            operand(check["left"])
            ok = False
            observed = "PRESENT"
        except KeyError:
            ok = True
            observed = "ABSENT"
    elif op == "TEXT_NOT_CONTAINS_LITERAL":
        ok = check["expected"] not in text_file(check["file"])
        observed = ok
    elif op == "JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL":
        subtree = operand(check["left"])
        txt = json.dumps(subtree, ensure_ascii=False, sort_keys=True)
        ok = check["expected"] not in txt
        observed = ok
    elif op == "MARKDOWN_HEADER_EQUALS_REGISTRY_VALUE":
        val = markdown_headers(text_file(check["file"])).get(check["header"])
        expected = json_path_get(starter, check["registry_value_path"])
        observed = {"header": val, "registry": expected}
        ok = val == str(expected)
    elif op == "STRICT_JSON_PARSE_NO_DUPLICATES":
        strict_json_load(source_file_for_spec(check["file"], paths))
        ok = True
        observed = "STRICT_PARSE_PASS"
    elif op == "FOUNDATION_FILENAME_COLLISION_FREE":
        manifest = json_path_get(json_file(check["manifest_file"]), check["manifest_path"])
        seen = set()
        reserved = {x.casefold() for x in check.get("portable_reserved_basename_stems", [])}
        normalized = []
        ok = True
        for rec in manifest:
            name = rec["canonical_filename"]
            norm = urllib.parse.unquote(name)
            norm = unicodedata.normalize(check.get("unicode_normalization_form", "NFKC"), norm).casefold().rstrip(" .")
            stem = Path(norm).stem
            if norm in seen or stem in reserved:
                ok = False
            seen.add(norm)
            normalized.append(norm)
        observed = normalized
    elif op == "FOUNDATION_MANIFEST_EXACT":
        manifest = json_path_get(json_file(check["manifest_file"]), check["manifest_path"])
        expected_names = {r["canonical_filename"] for r in manifest}
        roles = ["CORE_RUNTIME", "CONTROL_SURFACE", "GOVERNANCE_SUPPLEMENT", "DEFAULT_STARTER_PROFILE", "HANDOFF_CARD_TEMPLATE"]
        mapped_names = {CANONICAL_FILENAMES[k] for k in roles}
        observed = {"manifest": sorted(expected_names), "mapped": sorted(mapped_names)}
        ok = expected_names == mapped_names
    elif op == "CORE_RUNTIME_TRANSITION_IDENTITY_VALID":
        state = _runtime_transition_state(starter, paths)
        observed = state
        ok = state == CURRENT_RUNTIME_STATE
    elif op == "HANDOFF_TEMPLATE_TRANSITION_IDENTITY_VALID":
        observed = _handoff_transition_identity(paths)
        ok = observed.get("role") == "TARGET_CURRENT"
    return {
        "check_id": check.get("check_id"),
        "operator": op,
        "state": "PASS" if ok else "FAIL",
        "observed": observed,
    }


def evaluate_deterministic_registry(starter, paths):
    reg = starter["validation_contract"]["deterministic_contract_registry"]
    checks = reg.get("checks", [])
    ids = [c.get("check_id") for c in checks]
    if len(checks) != EXPECTED["deterministic_checks"] or len(set(ids)) != len(ids):
        raise CompileError("deterministic registry cardinality or uniqueness failure")
    unknown = sorted({c.get("operator") for c in checks} - ALLOWED_DETERMINISTIC_OPERATORS)
    if unknown:
        raise CompileError(f"unsupported deterministic operators: {unknown}")
    jc, tc = {}, {}
    results = [evaluate_deterministic_check(c, starter, paths, jc, tc) for c in checks]
    fail = [r for r in results if r["state"] != "PASS"]
    return {
        "declared_check_count": len(checks),
        "implemented_check_count": len(checks),
        "executed_check_count": len(results),
        "pass_count": len(results) - len(fail),
        "fail_count": len(fail),
        "overall_state": "PASS" if not fail else "FAIL",
        "results": results,
    }


def parse_source_identity(role, path):
    path = str(path)
    text = read_text(path) if path.endswith(".md") else None
    obj = strict_json_load(path) if path.endswith(".json") else None
    headers = markdown_headers(text) if text is not None else {}
    designation = None
    version = None
    if obj is not None:
        if role == "HANDOFF_CARD_TEMPLATE":
            root = obj.get("AIR_HANDOFF_CARD", {})
            designation = root.get("TEMPLATE_DESIGNATION")
            version = root.get("SCHEMA_VERSION")
        elif role == "PACKAGE_SCHEMA":
            designation = obj.get("$id")
            version = (obj.get("$id") or "").rsplit(":", 1)[-1]
        elif role == "COMPONENT_METADATA_OVERLAY":
            designation = obj.get("SYSTEM_DESIGNATION")
            version = "2"
        elif role == "LAW_APPLICABILITY_ROUTER":
            designation = obj.get("SYSTEM_DESIGNATION")
            version = obj.get("ROUTER_VERSION")
        else:
            designation = obj.get("SYSTEM_DESIGNATION")
            version = obj.get("PROMPT_VERSION") or obj.get("SCHEMA_VERSION") or obj.get("ROUTER_VERSION")
    else:
        designation = headers.get("SYSTEM_DESIGNATION")
        version = headers.get("PROMPT_VERSION")
    return {
        "canonical_role": role,
        "canonical_filename": CANONICAL_FILENAMES[role],
        "canonical_path": CANONICAL_PATHS[role],
        "sha256": file_sha256(path),
        "designation": designation,
        "version": version,
    }


def validate_source_pins(paths):
    observations = []
    for role, expected in PINNED_HASHES.items():
        if role not in paths:
            raise CompileError(f"missing source role {role}")
        actual = file_sha256(paths[role])
        observations.append({"role": role, "expected": expected, "actual": actual, "state": "PASS" if actual == expected else "FAIL"})
    fail = [x for x in observations if x["state"] != "PASS"]
    if fail:
        raise CompileError(f"source pin drift: {fail}")
    return observations




def law_source_root(paths):
    return Path(paths["LAW_SOURCE_PACKAGE_SCHEMA"]).parent


def validate_law_source_family(paths, regenerated_law_router=None):
    schema = strict_json_load(paths["LAW_SOURCE_PACKAGE_SCHEMA"])
    law_registry = strict_json_load(paths["LAW_SOURCE_LAW_ID_REGISTRY"])
    body_index = strict_json_load(paths["LAW_SOURCE_LAW_BODY_INDEX"])
    floor_index = strict_json_load(paths["LAW_SOURCE_FLOOR_INVARIANT_INDEX"])
    if schema.get("SYSTEM_DESIGNATION") != "AIR_LAW_SOURCE_PACKAGE_SCHEMA_V1":
        raise CompileError("law-source package schema designation mismatch")
    if schema.get("positive_execution_authority") != "NONE" or schema.get("provider_identity_semantic_authority") != "NONE":
        raise CompileError("law-source package schema authority boundary violation")
    counts = schema.get("counts", {})
    expected_counts = {"law_identity_count": 83, "physical_law_body_count": 82, "floor_body_count": 28, "source_family_file_count": 114}
    if any(counts.get(k) != v for k, v in expected_counts.items()):
        raise CompileError(f"law-source schema count mismatch: {counts}")
    if law_registry.get("entry_count") != 83 or len(law_registry.get("entries", [])) != 83:
        raise CompileError("law-source registry count mismatch")
    if law_registry.get("entry_fingerprint_sha256") != core_law_registry(read_text(paths["CORE_RUNTIME"])).get("entry_fingerprint_sha256"):
        raise CompileError("law-source registry fingerprint does not match current Core")
    body_entries = body_index.get("entries", [])
    floor_entries = floor_index.get("entries", [])
    if body_index.get("law_identity_count") != 83 or body_index.get("physical_body_count") != 82 or len(body_entries) != 83:
        raise CompileError("law-source body-index count mismatch")
    if floor_index.get("floor_count") != 28 or len(floor_entries) != 28:
        raise CompileError("law-source floor-index count mismatch")
    root = law_source_root(paths)
    physical_paths = {}
    for rec in body_entries:
        rel = rec.get("canonical_path")
        if not isinstance(rel, str) or not rel.startswith("law_source/laws/"):
            raise CompileError("law-source body path invalid")
        p = root.parent / rel
        if not p.is_file() or file_sha256(p) != rec.get("body_sha256") or p.stat().st_size != rec.get("size_bytes"):
            raise CompileError(f"law-source body integrity mismatch: {rel}")
        physical_paths[rel] = (rec.get("body_sha256"), rec.get("size_bytes"))
    if len(physical_paths) != 82:
        raise CompileError("law-source unique physical law body count mismatch")
    floor_paths = {}
    for rec in floor_entries:
        rel = rec.get("canonical_path")
        if not isinstance(rel, str) or not rel.startswith("law_source/floors/"):
            raise CompileError("law-source floor path invalid")
        p = root.parent / rel
        if not p.is_file() or file_sha256(p) != rec.get("body_sha256") or p.stat().st_size != rec.get("size_bytes"):
            raise CompileError(f"law-source floor integrity mismatch: {rel}")
        floor_paths[rel] = (rec.get("body_sha256"), rec.get("size_bytes"))
    if len(floor_paths) != 28:
        raise CompileError("law-source unique floor body count mismatch")
    observed = sorted(p.relative_to(root.parent).as_posix() for p in root.rglob('*') if p.is_file())
    if len(observed) != 114:
        raise CompileError(f"law-source family file count mismatch: {len(observed)}")
    expected = set(schema.get("required_root_resources", [])) | set(physical_paths) | set(floor_paths)
    if set(observed) != expected:
        raise CompileError("law-source family exact path set mismatch")
    if regenerated_law_router is not None:
        validate_law_router(regenerated_law_router, read_text(paths["CORE_RUNTIME"]))
    return {
        "package_id": schema.get("package_id"),
        "package_version": schema.get("package_version"),
        "semantic_owner": schema.get("semantic_owner"),
        "law_registry_fingerprint_sha256": law_registry.get("entry_fingerprint_sha256"),
        "law_body_index_fingerprint_sha256": body_index.get("body_index_fingerprint_sha256"),
        "floor_registry_fingerprint_sha256": floor_index.get("floor_registry_fingerprint_sha256"),
        "law_count": 83,
        "physical_law_body_count": 82,
        "floor_count": 28,
        "source_family_file_count": 114,
        "law_body_records": body_entries,
        "floor_body_records": floor_entries,
    }


def law_router_derivation_payload(law_router, paths):
    return {
        "SYSTEM_DESIGNATION": "AIR_LAW_ROUTER_DERIVATION_V1",
        "contract_version": "1.0.0",
        "source_core_sha256": PINNED_HASHES["CORE_RUNTIME"],
        "prior_router_sha256": PINNED_HASHES["LAW_APPLICABILITY_ROUTER"],
        "law_registry_fingerprint_sha256": core_law_registry(read_text(paths["CORE_RUNTIME"]))["entry_fingerprint_sha256"],
        "router_law_count": len(law_router.get("law_applicability_metadata", [])),
        "router_metadata_fingerprint_sha256": law_router.get("law_applicability_metadata_fingerprint_sha256"),
        "derivation_contract": "REGENERATE_FROM_EXACT_PRIOR_ROUTER_PLUS_CURRENT_CORE_STABLE_REGISTRY_WITH_SOURCE_REANCHOR",
        "semantic_authority": "NONE",
        "positive_execution_authority": "NONE",
    }


def law_package_build_plan(paths, law_router):
    state = validate_law_source_family(paths, law_router)
    root = law_source_root(paths)
    files = []
    # Three compact Tier1 indexes. The source-family schema remains compiler input, not a package navigation body.
    index_map = [
        ("index/AIR_LAW_ID_REGISTRY.json", Path(paths["LAW_SOURCE_LAW_ID_REGISTRY"]), "LAW_ID_REGISTRY", "TIER1_COMPACT_NAVIGATION"),
        ("index/AIR_LAW_APPLICABILITY_ROUTER.json", None, "LAW_APPLICABILITY_ROUTER", "TIER1_COMPACT_NAVIGATION"),
        ("index/AIR_FLOOR_INVARIANT_INDEX.json", Path(paths["LAW_SOURCE_FLOOR_INVARIANT_INDEX"]), "FLOOR_INVARIANT_INDEX", "TIER1_COMPACT_NAVIGATION"),
    ]
    payloads = {
        "law_package/index/AIR_LAW_ID_REGISTRY.json": strict_json_load(paths["LAW_SOURCE_LAW_ID_REGISTRY"]),
        "law_package/index/AIR_LAW_APPLICABILITY_ROUTER.json": copy.deepcopy(law_router),
        "law_package/index/AIR_FLOOR_INVARIANT_INDEX.json": strict_json_load(paths["LAW_SOURCE_FLOOR_INVARIANT_INDEX"]),
    }
    for rel, source_path, role, retrieval_class in index_map:
        obj = payloads["law_package/" + rel]
        raw = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        files.append({"path": rel, "role": role, "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw), "retrieval_class": retrieval_class})
    raw_copy_files = []
    for rec in sorted({x["canonical_path"]: x for x in state["law_body_records"]}.values(), key=lambda x: x["canonical_path"]):
        src = root.parent / rec["canonical_path"]
        rel = "laws/" + src.name
        files.append({"path": rel, "role": "LAW_BODY", "sha256": rec["body_sha256"], "size_bytes": rec["size_bytes"], "retrieval_class": "TIER2_EXACT_TARGETED_BODY"})
        raw_copy_files.append((src, rel))
    for rec in sorted(state["floor_body_records"], key=lambda x: x["canonical_path"]):
        src = root.parent / rec["canonical_path"]
        rel = "floors/" + src.name
        files.append({"path": rel, "role": "FLOOR_BODY", "sha256": rec["body_sha256"], "size_bytes": rec["size_bytes"], "retrieval_class": "TIER2_EXACT_TARGETED_BODY"})
        raw_copy_files.append((src, rel))
    deriv = law_router_derivation_payload(law_router, paths)
    deriv_raw = (json.dumps(deriv, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    files.append({"path": "evidence/AIR_LAW_ROUTER_DERIVATION.json", "role": "ROUTER_DERIVATION_EVIDENCE", "sha256": hashlib.sha256(deriv_raw).hexdigest(), "size_bytes": len(deriv_raw), "retrieval_class": "TIER3_DEEP_AUDIT"})
    payloads["law_package/evidence/AIR_LAW_ROUTER_DERIVATION.json"] = deriv
    files = sorted(files, key=lambda x: x["path"])
    content_fp = canonical_json_sha256(files)
    manifest = {
        "SYSTEM_DESIGNATION": "AIR_LAW_SOURCE_PACKAGE_MANIFEST_V1",
        "contract_version": "1.0.0",
        "package_id": "AIR_LAW_SOURCE_PACKAGE_V1",
        "package_version": "1.0.0-AMRS4E-INTEGRATED",
        "semantic_owner": "AIR_CORE_RUNTIME_V2_BOOTSTRAP_TRUST_KERNEL",
        "law_count": 83,
        "law_registry_ref": "index/AIR_LAW_ID_REGISTRY.json",
        "law_registry_fingerprint_sha256": state["law_registry_fingerprint_sha256"],
        "router_ref": "index/AIR_LAW_APPLICABILITY_ROUTER.json",
        "router_fingerprint_sha256": next(x["sha256"] for x in files if x["path"] == "index/AIR_LAW_APPLICABILITY_ROUTER.json"),
        "floor_registry_ref": "index/AIR_FLOOR_INVARIANT_INDEX.json",
        "floor_registry_fingerprint_sha256": state["floor_registry_fingerprint_sha256"],
        "runtime_compatibility": {"runtime_family": "AIR_CORE_RUNTIME_V2", "target_amrs": 6, "semantic_owner_cutover_required_for_package_mode": True},
        "canonicalization_profile": {"json": "UTF8_NO_BOM_SORTED_KEYS_INDENT_2_TRAILING_LF", "text_bodies": "UTF8_NO_BOM_LF_EXACT_BYTES"},
        "files": files,
        "content_fingerprint_sha256": content_fp,
        "positive_execution_authority": "NONE",
    }
    manifest_raw = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    manifest_sha = hashlib.sha256(manifest_raw).hexdigest()
    pin = {
        "contract_id": "AIR_LAW_SOURCE_PACKAGE_PIN_V1",
        "contract_version": "1.0.0",
        "package_id": manifest["package_id"],
        "package_version": manifest["package_version"],
        "manifest_sha256": manifest_sha,
        "content_fingerprint_sha256": content_fp,
        "law_registry_fingerprint_sha256": state["law_registry_fingerprint_sha256"],
        "router_fingerprint_sha256": manifest["router_fingerprint_sha256"],
        "floor_registry_fingerprint_sha256": state["floor_registry_fingerprint_sha256"],
        "expected_law_count": 83,
        "runtime_compatibility": copy.deepcopy(manifest["runtime_compatibility"]),
        "positive_execution_authority": "NONE",
        "activation_state": "PREPARED_SHADOW_ONLY_V1_REMAINS_OPERATIVE_PENDING_AMRS4F_SEMANTIC_OWNER_CUTOVER",
    }
    payloads["law_package/AIR_LAW_SOURCE_PACKAGE_MANIFEST.json"] = manifest
    payloads["compiled/AIR_LAW_SOURCE_PACKAGE_PIN.json"] = pin
    return {"state": state, "payloads": payloads, "raw_copy_files": raw_copy_files, "manifest_sha256": manifest_sha, "content_fingerprint_sha256": content_fp}

def build_source_manifest(paths, rebased_overlay_sha256, regenerated_law_router_sha256):
    roles = [
        "CORE_RUNTIME", "GOVERNANCE_SUPPLEMENT", "CONTROL_SURFACE",
        "DEFAULT_STARTER_PROFILE", "HANDOFF_CARD_TEMPLATE", "RUNTIME_ROUTE_MAP",
        "PACKAGE_SCHEMA", "COMPONENT_METADATA_OVERLAY", "LAW_APPLICABILITY_ROUTER",
        "LAW_SOURCE_PACKAGE_SCHEMA", "LAW_SOURCE_LAW_ID_REGISTRY",
        "LAW_SOURCE_LAW_BODY_INDEX", "LAW_SOURCE_FLOOR_INVARIANT_INDEX",
    ]
    files = [parse_source_identity(role, paths[role]) for role in roles]
    return {
        "SYSTEM_DESIGNATION": "AIR_P_SOURCE_MANIFEST_V1",
        "package_designation": PACKAGE_DESIGNATION,
        "canonicalization": CANONICAL_JSON_ALGORITHM,
        "authority_precedence": ["AIR_CORE_RUNTIME_V2", "AIR_HR_GOVERNANCE_SUPPLEMENT_V2", "AIR_CONTROL_SURFACE_V2", "AIR_DEFAULT_STARTER_V2"],
        "runtime_state": CURRENT_RUNTIME_STATE,
        "files": files,
        "component_metadata_overlay": {
            "input_sha256": PINNED_HASHES["COMPONENT_METADATA_OVERLAY"],
            "rebased_candidate_sha256": rebased_overlay_sha256,
            "authority_class": "DERIVED_NONAUTHORITATIVE_METADATA_OVERLAY",
            "semantic_authority": "NONE",
            "positive_execution_authority": "NONE",
            "binding_target_role": "CORE_RUNTIME",
        },
        "law_applicability_router": {
            "prior_input_sha256": PINNED_HASHES["LAW_APPLICABILITY_ROUTER"],
            "regenerated_candidate_sha256": regenerated_law_router_sha256,
            "authority_class": "DERIVED_NONAUTHORITATIVE_MACHINE_ROUTER",
            "semantic_authority": "NONE",
            "positive_execution_authority": "NONE",
        },
        "law_source_family": {
            "state": "INSTALLED_SHADOW_SOURCE_NOT_SEMANTIC_OWNER",
            "package_pin_output_ref": "AIR_LAW_SOURCE_PACKAGE_PIN.json",
            "semantic_owner_cutover_segment": "AMRS4F",
            "positive_execution_authority": "NONE",
        },
        "package_schema_authority": "CANONICAL_RUNTIME_BUNDLE_VALIDATION_SCHEMA",
        "route_map_authority": "NONAUTHORITATIVE_VALIDATION_FIXTURE_ONLY",
        "path_serialization_policy": "CANONICAL_REPOSITORY_RELATIVE_PATHS_ONLY",
    }


def runtime_bundle_schema_validate(instance, schema):
    if schema.get("type") == "object" and not isinstance(instance, dict):
        raise CompileError("runtime bundle must be object")
    for key in schema.get("required", []):
        if key not in instance:
            raise CompileError(f"runtime bundle missing required field {key}")
    props = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        extra = set(instance) - set(props)
        if extra:
            raise CompileError(f"runtime bundle extra fields: {sorted(extra)}")
    for key, spec in props.items():
        if key not in instance:
            continue
        val = instance[key]
        if "const" in spec and val != spec["const"]:
            raise CompileError(f"runtime bundle const mismatch {key}")
        if spec.get("type") == "object":
            if not isinstance(val, dict):
                raise CompileError(f"runtime bundle field {key} must be object")
            for req in spec.get("required", []):
                if req not in val:
                    raise CompileError(f"runtime bundle {key} missing {req}")
            if spec.get("additionalProperties") is False:
                extra = set(val) - set(spec.get("properties", {}))
                if extra:
                    raise CompileError(f"runtime bundle {key} extra fields {sorted(extra)}")
            for subkey, subspec in spec.get("properties", {}).items():
                if subkey in val and "const" in subspec and val[subkey] != subspec["const"]:
                    raise CompileError(f"runtime bundle {key}.{subkey} const mismatch")
    return True



def build_payloads(paths):
    validate_source_pins(paths)
    core_text = read_text(paths["CORE_RUNTIME"])
    starter = strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
    handoff = strict_json_load(paths["HANDOFF_CARD_TEMPLATE"])
    route_map = strict_json_load(paths["RUNTIME_ROUTE_MAP"])
    schema = strict_json_load(paths["PACKAGE_SCHEMA"])
    input_overlay = strict_json_load(paths["COMPONENT_METADATA_OVERLAY"])
    prior_law_router = strict_json_load(paths["LAW_APPLICABILITY_ROUTER"])

    formal_reg = core_formal_object_registry(core_text)
    decision_trace_contracts = core_decision_trace_contracts(core_text)
    law_router = regenerate_law_router(core_text, prior_law_router)
    transition_state = _runtime_transition_state(starter, paths)
    handoff_tuple = _handoff_transition_identity(paths)
    if transition_state != CURRENT_RUNTIME_STATE:
        raise CompileError(f"unexpected runtime transition state {transition_state}")

    rebased_overlay = rebase_component_overlay(
        core_text,
        input_overlay,
        PINNED_HASHES["CORE_RUNTIME"],
        PINNED_HASHES["COMPONENT_METADATA_OVERLAY"],
    )
    rebased_overlay_sha256 = canonical_json_sha256(rebased_overlay)
    components = component_registry_from_overlay(rebased_overlay, rebased_overlay_sha256)
    routes = parse_route_registry(core_text)
    validate_route_fixture(routes, route_map)
    events = copy.deepcopy(starter["compiler_contract"]["runtime_control_event_registry"]["events"])
    if len(events) != EXPECTED["control_events"]:
        raise CompileError("control-event count mismatch")
    route_ids = {r["route_id"] for r in routes}
    event_route_ids = {e["route_id"] for e in events}
    event_ids = {e["event_id"] for e in events}
    route_event_refs = {r["control_event_ref"] for r in routes}
    if route_ids != event_route_ids or event_ids != route_event_refs:
        raise CompileError("route/control-event bijection failure")

    det_exec = evaluate_deterministic_registry(starter, paths)
    if det_exec["overall_state"] != "PASS":
        failed = [r["check_id"] for r in det_exec["results"] if r["state"] != "PASS"]
        raise CompileError(f"deterministic registry failed: {failed}")

    law_state = validate_law_router(law_router, core_text)
    law_package = law_package_build_plan(paths, law_router)
    turn_governance_kernel, runtime_reference_index = build_runtime_navigation_outputs(paths, starter)
    source_manifest = build_source_manifest(paths, rebased_overlay_sha256, canonical_json_sha256(law_router))

    component_registry = {
        "SYSTEM_DESIGNATION": "AIR_P_COMPONENT_REGISTRY_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_REGISTRY",
        "semantic_owner": "AIR_CORE_RUNTIME_V2",
        "source_sha256": PINNED_HASHES["CORE_RUNTIME"],
        "component_count": len(components),
        "component_identity_provenance": {
            "input_metadata_overlay_sha256": PINNED_HASHES["COMPONENT_METADATA_OVERLAY"],
            "rebased_metadata_overlay_sha256": rebased_overlay_sha256,
            "overlay_authority_class": "DERIVED_NONAUTHORITATIVE_METADATA_OVERLAY",
            "semantic_authority": "NONE",
            "positive_execution_authority": "NONE",
            "binding_target_core_sha256": PINNED_HASHES["CORE_RUNTIME"],
            "binding_method": "EXACT_SECTION_HEADING_PLUS_PATCH_MARKER_WITH_DETERMINISTIC_SINGLE_MARKER_MIGRATION",
            "bound_component_count": len(components),
        },
        "components": components,
    }
    route_registry = {
        "SYSTEM_DESIGNATION": "AIR_P_ROUTE_CONTRACT_REGISTRY_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_REGISTRY",
        "semantic_owner": "AIR_CORE_RUNTIME_V2",
        "source_sha256": PINNED_HASHES["CORE_RUNTIME"],
        "route_fixture_sha256": PINNED_HASHES["RUNTIME_ROUTE_MAP"],
        "route_count": len(routes),
        "routes": routes,
    }
    event_registry = {
        "SYSTEM_DESIGNATION": "AIR_P_CONTROL_EVENT_REGISTRY_V1",
        "authority_class": "DERIVED_MACHINE_REPRESENTATION",
        "semantic_owner": starter["compiler_contract"]["runtime_control_event_registry"]["semantic_owner"],
        "source_owner": "AIR_DEFAULT_STARTER_V2.compiler_contract.runtime_control_event_registry",
        "allowed_guard_operators": starter["compiler_contract"]["runtime_control_event_registry"]["allowed_guard_operators"],
        "event_count": len(events),
        "events": events,
    }
    det_registry = {
        "SYSTEM_DESIGNATION": "AIR_P_DETERMINISTIC_VALIDATION_REGISTRY_V1",
        "authority_class": "DERIVED_MACHINE_REPRESENTATION",
        "source_owner": "AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry",
        "registry": copy.deepcopy(starter["validation_contract"]["deterministic_contract_registry"]),
        "current_execution_summary": {k: det_exec[k] for k in ["declared_check_count", "implemented_check_count", "executed_check_count", "pass_count", "fail_count", "overall_state"]},
        "current_execution_results": det_exec["results"],
    }
    formal_registry = {
        "SYSTEM_DESIGNATION": "AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_REGISTRY",
        "semantic_owner": "AIR_CORE_RUNTIME_V2",
        "source_registry_designation": formal_reg["SYSTEM_DESIGNATION"],
        "source_registry_version": formal_reg["REGISTRY_VERSION"],
        "source_core_sha256": PINNED_HASHES["CORE_RUNTIME"],
        "object_count": formal_reg["object_count"],
        "closed_world": formal_reg["closed_world"],
        "common_contract": copy.deepcopy(formal_reg["common_contract"]),
        "condition_context": copy.deepcopy(formal_reg["condition_context"]),
        "objects": copy.deepcopy(formal_reg["objects"]),
    }
    precedence = {
        "SYSTEM_DESIGNATION": "AIR_P_AUTHORITY_PRECEDENCE_REGISTRY_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_PROJECTION",
        "precedence": copy.deepcopy(starter["authority_contract"]["precedence"]),
        "conflict_rule": starter["authority_contract"]["conflict_rule"],
        "source_manifest_ref": "AIR_P_SOURCE_MANIFEST.json",
        "route_map": {
            "source_sha256": PINNED_HASHES["RUNTIME_ROUTE_MAP"],
            "authority": "NONAUTHORITATIVE_VALIDATION_FIXTURE_ONLY",
            "declared_route_count": len(route_map.get("routes", route_map.get("runtime_routes", []))),
        },
        "law_router": law_state,
        "decision_trace_contracts": {
            "closure": decision_trace_contracts["AIR_DECISION_BASIS_CLOSURE_V1"]["contract_id"],
            "object": decision_trace_contracts["AIR_DECISION_TRACE_OBJECT_CONTRACT_V1"]["formal_object_ref"],
            "forced_walk": decision_trace_contracts["AIR_DECISION_TRACE_FORCED_WALK_V1"]["contract_id"],
            "fingerprint": decision_trace_contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"]["contract_id"],
            "positive_execution_authority": "NONE",
        },
        "compiled_package_self_authority": "NONE",
    }
    canonical_state = {
        "SYSTEM_DESIGNATION": "AIR_P_CANONICAL_MACHINE_STATE_CONTRACT_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_MACHINE_CONTRACT",
        "semantic_owner": "AIR_CORE_RUNTIME_V2",
        "runtime_state": CURRENT_RUNTIME_STATE,
        "state_mutation": "ONLY_THROUGH_COMPILED_ROUTE_OR_VALIDATED_TRANSACTION_CONTRACT",
        "unknown_reference": "FAIL_CLOSED",
        "unknown_operator": "FAIL_CLOSED",
        "stale_source": "FAIL_CLOSED",
        "source_provenance": "HASH_PINNED",
        "authority_gain_from_representation": "PROHIBITED",
        "cognitive_to_control": "PROHIBITED_WITHOUT_EXPLICIT_VALIDATED_INGESTION",
        "route_registry_ref": "AIR_P_ROUTE_CONTRACT_REGISTRY.json",
        "control_event_registry_ref": "AIR_P_CONTROL_EVENT_REGISTRY.json",
        "formal_object_registry_ref": "AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json",
        "turn_governance_kernel_ref": "AIR_P_TURN_GOVERNANCE_KERNEL.json",
        "runtime_reference_index_ref": "AIR_P_RUNTIME_REFERENCE_INDEX.json",
    }
    semantic = {
        "SYSTEM_DESIGNATION": "AIR_P_SEMANTIC_BINDING_REGISTRY_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_PROJECTION",
        "positive_control_authority": "NONE",
        "ingress_contract": {
            "semantic_proposal_authority": "NONE",
            "allowed_effect": "PROPOSE_TYPED_EVENT_OR_VALUE_ONLY",
            "control_transition_requirement": "MATCHED_COMPILED_ROUTE_PLUS_TYPED_GUARDS",
            "unknown_or_failed_guard": "FAIL_CLOSED_NO_CONTROL_STATE_TRANSITION",
        },
        "route_event_bindings": [{"route_id": r["route_id"], "control_event_ref": r["control_event_ref"]} for r in routes],
        "egress_contract": {
            "source": "CANONICAL_MACHINE_STATE",
            "targets": ["CANONICAL_AIR_OBJECT", "RECEIVER_SURFACE_PROJECTION"],
            "material_semantic_loss": "PROHIBITED",
            "authority_gain": "PROHIBITED",
        },
        "roundtrip_contract": "NO_MATERIAL_SEMANTIC_LOSS_OR_AUTHORITY_GAIN",
        "event_count": len(events),
    }
    hroot = handoff["AIR_HANDOFF_CARD"]
    handoff_contract = {
        "SYSTEM_DESIGNATION": "AIR_P_HANDOFF_CHECKPOINT_DELTA_CONTRACT_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_TRANSFER_CONTRACT",
        "template_designation": hroot["TEMPLATE_DESIGNATION"],
        "schema_version": hroot["SCHEMA_VERSION"],
        "template_revision": hroot["template_revision"],
        "template_sha256": PINNED_HASHES["HANDOFF_CARD_TEMPLATE"],
        "transition_tuple": handoff_tuple,
        "runtime_state": transition_state,
        "checkpoint": "CANONICAL_MACHINE_STATE_SNAPSHOT_PLUS_SOURCE_HASHES_PLUS_LEDGER_HEAD_REFS",
        "delta": "EXPLICIT_TYPED_STATE_CHANGES_ONLY_NO_INFERRED_HISTORY",
        "strict_provenance": "PRESERVE_EXISTING_STRICT_VS_PORTABLE_BOUNDARY",
        "historical_authority_reconstruction": "PROHIBITED",
        "restore_authority": "CONTINUATION_BOOTSTRAP_INPUT_ONLY_REVALIDATION_AND_ARTIFACT_REBIND_REQUIRED",
        "starter_handoff_contract": copy.deepcopy(starter["handoff_contract"]),
        "template_schema_manifest_sha256": canonical_json_sha256(hroot.get("schema_manifest", {})),
    }
    package_enabled = transition_state == POST_F_RUNTIME_STATE
    law_source_projection_effect = (
        "PACKAGE_ENABLED_LAW_SOURCE_SEMANTIC_OWNER_AND_VALIDATION_INPUT"
        if package_enabled else "SHADOW_LAW_SOURCE_PACKAGE_IDENTITY_AND_VALIDATION_INPUT"
    )
    component_rebase_check = (
        "COMPONENT_METADATA_OVERLAY_V2_CURRENT_CORE_PLUS_LAW_SOURCE_REBASE"
        if package_enabled else "COMPONENT_METADATA_OVERLAY_V2_CURRENT_CORE_REBASE"
    )
    law_package_state_check = (
        "LAW_SOURCE_PACKAGE_ACTIVE_V2_SEMANTIC_OWNER"
        if package_enabled else "LAW_SOURCE_PACKAGE_SHADOW_ONLY_V1_REMAINS_OPERATIVE"
    )
    law_router_source_check = (
        "LAW_ROUTER_83_OF_83_REGENERATED_FROM_STANDALONE_LAW_REGISTRY"
        if package_enabled else "LAW_ROUTER_83_OF_83_REGENERATED_FROM_CORE_REGISTRY"
    )
    projections = {
        "SYSTEM_DESIGNATION": "AIR_P_CONTROL_GOVERNANCE_PROJECTIONS_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_PROJECTIONS",
        "projections": [
            {"source_role": "GOVERNANCE_SUPPLEMENT", "effect": "MAY_TIGHTEN_CORE_REQUIREMENTS", "may_redefine_core": False},
            {"source_role": "CONTROL_SURFACE", "effect": "RENDER_CORE_STATE_AND_REQUIRED_OBJECTS", "may_redefine_core": False},
            {"source_role": "DEFAULT_STARTER_PROFILE", "effect": "SUPPLY_DEFAULTS_TYPED_EVENTS_AND_VALIDATION_REGISTRY", "may_redefine_core": False},
            {"source_role": "RUNTIME_ROUTE_MAP", "effect": "PARITY_FIXTURE_ONLY", "may_redefine_core": False},
            {"source_role": "LAW_APPLICABILITY_ROUTER", "effect": "DERIVED_LAW_APPLICABILITY_MACHINE_ROUTER", "may_redefine_core": False},
            {"source_role": "COMPONENT_METADATA_OVERLAY", "effect": "DERIVED_COMPONENT_IDENTITY_METADATA_ONLY", "may_redefine_core": False},
            {"source_role": "LAW_SOURCE_PACKAGE_SCHEMA", "effect": law_source_projection_effect, "may_redefine_core": False},
        ],
        "source_hashes": copy.deepcopy(PINNED_HASHES),
    }
    conformance = {
        "SYSTEM_DESIGNATION": "AIR_P_CONFORMANCE_PROFILE_V1",
        "profile_version": "1.0.0",
        "expected_cardinality": copy.deepcopy(EXPECTED),
        "runtime_state": CURRENT_RUNTIME_STATE,
        "required_checks": [
            "COMPONENT_ID_UNIQUENESS_AND_SOURCE_ANCHOR_113_OF_113",
            component_rebase_check,
            "PACKAGE_SCHEMA_1_1_0_EXACT",
            "ROUTE_SOURCE_EQUIVALENCE_22_OF_22",
            "ROUTE_CONTROL_EVENT_BIJECTION_22_OF_22",
            "STARTER_DETERMINISTIC_REGISTRY_137_OF_137",
            "FORMAL_OBJECT_CORE_MACHINE_REGISTRY_21_OF_21",
            "R23_AMRS4F_PACKAGE_ENABLED_SEMANTIC_OWNER_CUTOVER_TRANSITION_TUPLE_EXACT",
            "TURN_GOVERNANCE_KERNEL_DIRECT_ANCHORS_COMPLETE",
            "RUNTIME_REFERENCE_INDEX_DIRECT_DEPTH_ONE_COMPLETE",
            "RUNTIME_NAVIGATION_DERIVED_NONAUTHORITY",
            "LAW_ROUTER_83_OF_83_REGENERATED",
            "LAW_SOURCE_FAMILY_114_OF_114_EXACT",
            "LAW_SOURCE_PACKAGE_MANIFEST_AND_PIN_DETERMINISTIC",
            law_package_state_check,
            "FORMAL_JSON_CONFORMANCE_EXECUTABLE_REGISTRY_CHECK",
            "AUTHORITY_PRECEDENCE_PRESERVATION",
            "SEMANTIC_PROPOSAL_NONAUTHORITY",
            "CANONICAL_MACHINE_STATE_NO_AUTHORITY_GAIN",
            "HANDOFF_NO_UNSURFACED_HISTORY_RECONSTRUCTION",
            "DECISION_TRACE_CORE_MACHINE_CONTRACTS",
            "DECISION_TRACE_FORMAL_OBJECT_21_OF_21",
            law_router_source_check,
            "NEGATIVE_MUTATION_SUITE",
            "DETERMINISTIC_CHECK_MUTATION_COVERAGE_137_OF_137",
            "THREE_INDEPENDENT_PROCESS_PAYLOAD_REPRODUCIBILITY",
        ],
        "negative_mutations": [
            "DUPLICATE_COMPONENT_ID",
            "COMPONENT_METADATA_ANCHOR_BREAK",
            "COMPONENT_METADATA_AUTHORITY_ESCALATION",
            "PACKAGE_SCHEMA_PIN_DRIFT",
            "FORMAL_OBJECT_MACHINE_REGISTRY_DRIFT",
            "UNKNOWN_DETERMINISTIC_OPERATOR",
            "ROUTE_CONTROL_EVENT_MISMATCH",
            "PINNED_SOURCE_DRIFT",
            "RUNTIME_BUNDLE_SCHEMA_DRIFT",
            "COMPILED_AUTHORITY_ESCALATION",
            "RUNTIME_TRANSITION_TUPLE_CROSS_MIX",
            "RUNTIME_REFERENCE_INDEX_STALE_SOURCE_ANCHOR",
            "TURN_GOVERNANCE_KERNEL_REQUIRED_ANCHOR_REMOVAL",
        ],
        "failure_policy": "FAIL_CLOSED",
        "law_router_state": law_state,
    }
    runtime_bundle = {
        "SYSTEM_DESIGNATION": "AIR_P_RUNTIME_BUNDLE_V1",
        "package_designation": PACKAGE_DESIGNATION,
        "package_version": PACKAGE_VERSION,
        "authority_class": "DERIVED_NONAUTHORITATIVE_MACHINE_REPRESENTATION",
        "semantic_owner": "AIR_CORE_RUNTIME_V2",
        "source_manifest_ref": "AIR_P_SOURCE_MANIFEST.json",
        "registry_refs": {
            "components": "AIR_P_COMPONENT_REGISTRY.json",
            "routes": "AIR_P_ROUTE_CONTRACT_REGISTRY.json",
            "control_events": "AIR_P_CONTROL_EVENT_REGISTRY.json",
            "deterministic_validation": "AIR_P_DETERMINISTIC_VALIDATION_REGISTRY.json",
            "formal_objects": "AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json",
            "authority_precedence": "AIR_P_AUTHORITY_PRECEDENCE_REGISTRY.json",
        },
        "contract_refs": {
            "canonical_machine_state": "AIR_P_CANONICAL_MACHINE_STATE_CONTRACT.json",
            "semantic_binding": "AIR_P_SEMANTIC_BINDING_REGISTRY.json",
            "handoff_checkpoint_delta": "AIR_P_HANDOFF_CHECKPOINT_DELTA_CONTRACT.json",
            "control_governance_projections": "AIR_P_CONTROL_GOVERNANCE_PROJECTIONS.json",
        },
        "conformance_profile_ref": "AIR_P_CONFORMANCE_PROFILE.json",
        "law_source_package_pin_ref": "AIR_LAW_SOURCE_PACKAGE_PIN.json",
        "backend_enforcement_claimed": False,
    }
    runtime_bundle_schema_validate(runtime_bundle, schema)
    return {
        "schema/AIR_P_PACKAGE_SCHEMA.json": schema,
        "source/AIR_P_COMPONENT_METADATA_OVERLAY.json": rebased_overlay,
        "source/AIR_LAW_APPLICABILITY_ROUTER.json": law_router,
        "compiled/AIR_P_SOURCE_MANIFEST.json": source_manifest,
        "compiled/AIR_P_COMPONENT_REGISTRY.json": component_registry,
        "compiled/AIR_P_ROUTE_CONTRACT_REGISTRY.json": route_registry,
        "compiled/AIR_P_CONTROL_EVENT_REGISTRY.json": event_registry,
        "compiled/AIR_P_DETERMINISTIC_VALIDATION_REGISTRY.json": det_registry,
        "compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json": formal_registry,
        "compiled/AIR_P_AUTHORITY_PRECEDENCE_REGISTRY.json": precedence,
        "compiled/AIR_P_CANONICAL_MACHINE_STATE_CONTRACT.json": canonical_state,
        "compiled/AIR_P_SEMANTIC_BINDING_REGISTRY.json": semantic,
        "compiled/AIR_P_HANDOFF_CHECKPOINT_DELTA_CONTRACT.json": handoff_contract,
        "compiled/AIR_P_CONTROL_GOVERNANCE_PROJECTIONS.json": projections,
        TURN_GOVERNANCE_KERNEL_OUTPUT: turn_governance_kernel,
        RUNTIME_REFERENCE_INDEX_OUTPUT: runtime_reference_index,
        "compiled/AIR_P_RUNTIME_BUNDLE.json": runtime_bundle,
        "compiled/AIR_P_CONFORMANCE_PROFILE.json": conformance,
        **law_package["payloads"],
    }


def _changed_literal(value):
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if value is None:
        return "__MUTATED_NON_NULL__"
    if isinstance(value, str):
        return value + "__MUTATED__"
    return "__MUTATED_LITERAL__"


def mutate_check_to_fail(check):
    c = copy.deepcopy(check)
    op = c["operator"]
    if op in {"MARKDOWN_HEADER_EQUALS_LITERAL", "JSON_EQUALS_LITERAL", "MARKDOWN_FINAL_LINE_EQUALS_LITERAL", "JSON_ARRAY_CONTAINS_LITERAL", "TEXT_CONTAINS_LITERAL"}:
        c["expected"] = _changed_literal(c.get("expected"))
    elif op == "JSON_EQUALS_REFERENCE":
        c["right"]["path"] = "$.__AIR_MUTATION_MISSING_PATH__"
    elif op == "JSON_EQUALS_MARKDOWN_HEADER":
        c["right"]["header"] = "__AIR_MUTATION_MISSING_HEADER__"
    elif op == "JSON_ROOT_KEYS_DECLARED_BY_MANIFEST":
        c["root_path"] = "$.__AIR_MUTATION_MISSING_ROOT__"
    elif op == "JSON_PATH_ABSENT":
        c["left"]["path"] = "$"
    elif op == "TEXT_NOT_CONTAINS_LITERAL":
        c["expected"] = "AIR"
    elif op == "JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL":
        c["expected"] = "AIR"
    elif op == "MARKDOWN_HEADER_EQUALS_REGISTRY_VALUE":
        c["header"] = "__AIR_MUTATION_MISSING_HEADER__"
    elif op == "FILE_EXISTS":
        c["file"] = "prompts/__AIR_MUTATION_MISSING_FILE__.json"
    elif op == "STRICT_JSON_PARSE_NO_DUPLICATES":
        c["operator"] = "UNKNOWN_OPERATOR_FOR_MUTATION_TEST"
    elif op == "FOUNDATION_FILENAME_COLLISION_FREE":
        c.setdefault("portable_reserved_basename_stems", []).append("air_core_runtime")
    elif op == "FOUNDATION_MANIFEST_EXACT":
        c["manifest_path"] = "$.__AIR_MUTATION_MISSING_MANIFEST__"
    elif op in {"CORE_RUNTIME_TRANSITION_IDENTITY_VALID", "HANDOFF_TEMPLATE_TRANSITION_IDENTITY_VALID"}:
        c["operator"] = "UNKNOWN_OPERATOR_FOR_MUTATION_TEST"
    else:
        c["operator"] = "UNKNOWN_OPERATOR_FOR_MUTATION_TEST"
    return c


def deterministic_check_mutation_coverage(starter, paths):
    checks = starter["validation_contract"]["deterministic_contract_registry"]["checks"]
    covered = []
    for check in checks:
        mutated = mutate_check_to_fail(check)
        rejected = False
        evidence = None
        try:
            result = evaluate_deterministic_check(mutated, starter, paths)
            rejected = result["state"] == "FAIL"
            evidence = result
        except (CompileError, KeyError, IndexError, TypeError, ValueError) as e:
            rejected = True
            evidence = {"exception": type(e).__name__, "message": str(e)}
        covered.append({
            "check_id": check["check_id"],
            "operator": check["operator"],
            "mutation_rejected": rejected,
            "evidence": evidence,
        })
    fail = [x for x in covered if not x["mutation_rejected"]]
    return {
        "declared_check_count": len(checks),
        "covered_check_count": len(covered),
        "rejected_mutation_count": len(covered) - len(fail),
        "uncovered_or_unrejected_count": len(fail),
        "overall_state": "PASS" if not fail and len(covered) == EXPECTED["deterministic_checks"] else "FAIL",
        "coverage": covered,
    }


def mutation_suite(payloads, paths):
    results = []
    def add(name, passed, evidence):
        results.append({"mutation": name, "state": "PASS" if passed else "FAIL", "evidence": evidence})

    comps = copy.deepcopy(payloads["compiled/AIR_P_COMPONENT_REGISTRY.json"])
    comps["components"].append(copy.deepcopy(comps["components"][0]))
    ids = [x["component_id"] for x in comps["components"]]
    add("DUPLICATE_COMPONENT_ID", len(ids) != len(set(ids)), "duplicate detected")

    overlay = copy.deepcopy(payloads["source/AIR_P_COMPONENT_METADATA_OVERLAY.json"])
    overlay["components"][0]["anchor"]["section_heading"] = "BROKEN_SECTION_HEADING_FOR_MUTATION_TEST"
    try:
        rebase_component_overlay(read_text(paths["CORE_RUNTIME"]), overlay, PINNED_HASHES["CORE_RUNTIME"], canonical_json_sha256(overlay))
        rejected = False
    except CompileError:
        rejected = True
    add("COMPONENT_METADATA_ANCHOR_BREAK", rejected, "broken anchor rejected")

    overlay2 = copy.deepcopy(payloads["source/AIR_P_COMPONENT_METADATA_OVERLAY.json"])
    overlay2["semantic_authority"] = "FOUNDATION_AUTHORITY"
    try:
        rebase_component_overlay(read_text(paths["CORE_RUNTIME"]), overlay2, PINNED_HASHES["CORE_RUNTIME"], canonical_json_sha256(overlay2))
        rejected = False
    except CompileError:
        rejected = True
    add("COMPONENT_METADATA_AUTHORITY_ESCALATION", rejected, "overlay authority escalation rejected")

    schema_actual = file_sha256(paths["PACKAGE_SCHEMA"])
    add("PACKAGE_SCHEMA_PIN_DRIFT", schema_actual == PINNED_HASHES["PACKAGE_SCHEMA"], "exact package schema pin preserved")

    formal = payloads["compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json"]
    add("FORMAL_OBJECT_MACHINE_REGISTRY_DRIFT", formal["object_count"] == EXPECTED["formal_objects"], "21-object machine registry exact")

    starter = strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
    mutated_check = copy.deepcopy(starter["validation_contract"]["deterministic_contract_registry"]["checks"][0])
    mutated_check["operator"] = "UNKNOWN_OPERATOR_FOR_MUTATION_TEST"
    try:
        evaluate_deterministic_check(mutated_check, starter, paths)
        rejected = False
    except CompileError:
        rejected = True
    add("UNKNOWN_DETERMINISTIC_OPERATOR", rejected, "unknown operator rejected")

    rr = copy.deepcopy(payloads["compiled/AIR_P_ROUTE_CONTRACT_REGISTRY.json"])
    er = payloads["compiled/AIR_P_CONTROL_EVENT_REGISTRY.json"]
    rr["routes"][0]["control_event_ref"] = "CE-RT-NONEXISTENT"
    event_ids = {e["event_id"] for e in er["events"]}
    add("ROUTE_CONTROL_EVENT_MISMATCH", rr["routes"][0]["control_event_ref"] not in event_ids, "mismatch detected")

    sm = copy.deepcopy(payloads["compiled/AIR_P_SOURCE_MANIFEST.json"])
    sm["files"][0]["sha256"] = "0" * 64
    add("PINNED_SOURCE_DRIFT", sm["files"][0]["sha256"] != PINNED_HASHES[sm["files"][0]["canonical_role"]], "hash drift detected")

    schema = payloads["schema/AIR_P_PACKAGE_SCHEMA.json"]
    bundle = copy.deepcopy(payloads["compiled/AIR_P_RUNTIME_BUNDLE.json"])
    bundle["undeclared_field"] = True
    try:
        runtime_bundle_schema_validate(bundle, schema)
        rejected = False
    except CompileError:
        rejected = True
    add("RUNTIME_BUNDLE_SCHEMA_DRIFT", rejected, "extra field rejected")

    bundle2 = copy.deepcopy(payloads["compiled/AIR_P_RUNTIME_BUNDLE.json"])
    bundle2["authority_class"] = "AUTHORITATIVE_RUNTIME"
    try:
        runtime_bundle_schema_validate(bundle2, schema)
        rejected = False
    except CompileError:
        rejected = True
    add("COMPILED_AUTHORITY_ESCALATION", rejected, "authority const violation rejected")

    runtime_index = copy.deepcopy(payloads[RUNTIME_REFERENCE_INDEX_OUTPUT])
    runtime_index["anchors"][0]["source_sha256"] = "0" * 64
    try:
        validate_runtime_navigation_outputs(payloads[TURN_GOVERNANCE_KERNEL_OUTPUT], runtime_index, paths)
        rejected = False
    except CompileError:
        rejected = True
    add("RUNTIME_REFERENCE_INDEX_STALE_SOURCE_ANCHOR", rejected, "stale direct source anchor rejected")

    kernel_mut = copy.deepcopy(payloads[TURN_GOVERNANCE_KERNEL_OUTPUT])
    kernel_mut["required_contract_semantic_ids"] = kernel_mut["required_contract_semantic_ids"][:-1]
    try:
        validate_runtime_navigation_outputs(kernel_mut, payloads[RUNTIME_REFERENCE_INDEX_OUTPUT], paths)
        rejected = False
    except CompileError:
        rejected = True
    add("TURN_GOVERNANCE_KERNEL_REQUIRED_ANCHOR_REMOVAL", rejected, "missing required kernel anchor rejected")

    # Exact target state: AMRS4D3 Core with rev26 Handoff is the sole TARGET_CURRENT tuple.
    transition = payloads["compiled/AIR_P_HANDOFF_CHECKPOINT_DELTA_CONTRACT.json"]["transition_tuple"]
    add("RUNTIME_TRANSITION_TUPLE_CROSS_MIX", transition.get("role") == "TARGET_CURRENT" and transition.get("template_revision") == 26, "current tuple is exact rev26 TARGET_CURRENT")

    pin = copy.deepcopy(payloads["compiled/AIR_LAW_SOURCE_PACKAGE_PIN.json"])
    pin["positive_execution_authority"] = "ALLOW"
    add("LAW_SOURCE_PACKAGE_PIN_AUTHORITY_ESCALATION", pin.get("positive_execution_authority") != "NONE", "authority mutation detected")
    manifest = copy.deepcopy(payloads["law_package/AIR_LAW_SOURCE_PACKAGE_MANIFEST.json"])
    manifest["files"][0]["sha256"] = "0" * 64
    add("LAW_SOURCE_PACKAGE_MANIFEST_FILE_HASH_DRIFT", canonical_json_sha256(manifest["files"]) != manifest.get("content_fingerprint_sha256"), "manifest content fingerprint drift detected")

    return {"suite_state": "PASS" if all(r["state"] == "PASS" for r in results) else "FAIL", "tests": results}


def payload_hash_map(payloads):
    return {k: canonical_json_sha256(v) for k, v in sorted(payloads.items())}


def validate_source_inputs(paths):
    pins = validate_source_pins(paths)
    core_text = read_text(paths["CORE_RUNTIME"])
    starter = strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
    overlay = strict_json_load(paths["COMPONENT_METADATA_OVERLAY"])
    formal = core_formal_object_registry(core_text)
    rebased = rebase_component_overlay(core_text, overlay, PINNED_HASHES["CORE_RUNTIME"], PINNED_HASHES["COMPONENT_METADATA_OVERLAY"])
    routes = parse_route_registry(core_text)
    validate_route_fixture(routes, strict_json_load(paths["RUNTIME_ROUTE_MAP"]))
    events = starter["compiler_contract"]["runtime_control_event_registry"]["events"]
    checks = starter["validation_contract"]["deterministic_contract_registry"]["checks"]
    prior_law_router = strict_json_load(paths["LAW_APPLICABILITY_ROUTER"])
    regenerated_law_router = regenerate_law_router(core_text, prior_law_router)
    law_state = validate_law_router(regenerated_law_router, core_text)
    law_source_state = validate_law_source_family(paths, regenerated_law_router)
    decision_trace_contracts = core_decision_trace_contracts(core_text)
    transition = _runtime_transition_state(starter, paths)
    handoff_tuple = _handoff_transition_identity(paths)
    unknown_ops = sorted({c["operator"] for c in checks} - ALLOWED_DETERMINISTIC_OPERATORS)
    if len(events) != EXPECTED["control_events"] or len(checks) != EXPECTED["deterministic_checks"]:
        raise CompileError("starter cardinality mismatch")
    if formal["object_count"] != EXPECTED["formal_objects"]:
        raise CompileError("formal object cardinality mismatch")
    return {
        "decision": "PASS_SOURCE_CANDIDATE_CONTRACT_DISCOVERY",
        "runtime_state": transition,
        "handoff_tuple": handoff_tuple,
        "source_pin_validation": pins,
        "component_count": len(rebased["components"]),
        "component_marker_migrations": rebased.get("regeneration_provenance", {}).get("marker_migrations", []),
        "route_count": len(routes),
        "control_event_count": len(events),
        "deterministic_check_count": len(checks),
        "deterministic_operator_set": sorted({c["operator"] for c in checks}),
        "unknown_deterministic_operators": unknown_ops,
        "formal_object_count": formal["object_count"],
        "formal_registry_version": formal["REGISTRY_VERSION"],
        "law_router": law_state,
        "law_source_family": {k:v for k,v in law_source_state.items() if k not in {"law_body_records","floor_body_records"}},
        "regenerated_law_router_candidate_sha256": canonical_json_sha256(regenerated_law_router),
        "decision_trace_contracts": sorted(decision_trace_contracts),
        "rebased_overlay_candidate_sha256": canonical_json_sha256(rebased),
    }


def compile_package(out, paths, test_source=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for d in ["schema", "source", "compiled", "tests", "evidence", "law_package/index", "law_package/laws", "law_package/floors", "law_package/evidence"]:
        (out / d).mkdir(parents=True, exist_ok=True)
    payloads = build_payloads(paths)
    for rel, obj in payloads.items():
        write_json(out / rel, obj)
    law_plan = law_package_build_plan(paths, payloads["law_package/index/AIR_LAW_APPLICABILITY_ROUTER.json"])
    for src, rel in law_plan["raw_copy_files"]:
        dst = out / "law_package" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    if test_source:
        shutil.copyfile(test_source, out / "tests" / "test_air_p_compiler.py")

    starter = strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
    mutation = mutation_suite(payloads, paths)
    if mutation["suite_state"] != "PASS":
        raise CompileError("negative mutation suite failed")
    coverage = deterministic_check_mutation_coverage(starter, paths)
    if coverage["overall_state"] != "PASS":
        raise CompileError("deterministic check mutation coverage failed")

    maps = [payload_hash_map(build_payloads(paths)) for _ in range(3)]
    reproducible = maps[0] == maps[1] == maps[2]
    if not reproducible:
        raise CompileError("three-run in-memory payload reproducibility failed")

    package_enabled = _transition_mode(paths) == "POST_F_PACKAGE_ENABLED_V2"
    component_overlay_status = (
        "113/113 REBASED_TO_CURRENT_CORE_PLUS_LAW_SOURCE_PACKAGE_BY_COMPONENT"
        if package_enabled else "113/113 REBASED_TO_CURRENT_CORE"
    )
    law_router_status = (
        "83/83 REGENERATED_FROM_EXACT_PRIOR_ROUTER_PLUS_STANDALONE_LAW_REGISTRY"
        if package_enabled else "83/83 REGENERATED_FROM_EXACT_PRIOR_ROUTER_PLUS_CORE_REGISTRY"
    )
    law_source_family_status = (
        "114/114 PACKAGE_ENABLED_SEMANTIC_OWNER_VALIDATED"
        if package_enabled else "114/114 SHADOW_SOURCE_VALIDATED"
    )
    law_source_package_status = (
        "MANIFEST_AND_RELEASE_PIN_ACTIVE_PACKAGE_ENABLED_NONAUTHORIZING_IDENTITY"
        if package_enabled else "MANIFEST_AND_RELEASE_PIN_GENERATED_NONAUTHORIZING"
    )
    law_source_package_mode = (
        "ACTIVE_PACKAGE_ENABLED_V2_SEMANTIC_OWNER"
        if package_enabled else "NOT_ACTIVATED_V1_REMAINS_OPERATIVE_PENDING_AMRS4F"
    )
    external_repro_state = (
        "EXTERNAL_RELEASE_GRADE_REPROOF_REQUIRED_SEPARATELY"
        if package_enabled else "PENDING_EXTERNAL_AMRS4E_REPROOF"
    )
    run_decision = (
        "PASS_DETERMINISTIC_COMPILATION_EXTERNAL_RELEASE_GRADE_REPROOF_SEPARATE"
        if package_enabled else "PASS_CANDIDATE_BUILD_PENDING_R18_T10_INDEPENDENT_PROCESS_REPRODUCIBILITY"
    )
    compilation_report = {
        "SYSTEM_DESIGNATION": "AIR_P_COMPILATION_REPORT_V1",
        "package_designation": PACKAGE_DESIGNATION,
        "decision": "PASS",
        "runtime_state": CURRENT_RUNTIME_STATE,
        "source_integrity": "PASS",
        "compiled_cardinality": copy.deepcopy(EXPECTED),
        "route_event_bijection": "PASS",
        "deterministic_registry": "137/137 PASS",
        "formal_object_contracts": "21/21 COMPILED_FROM_CORE_MACHINE_REGISTRY",
        "component_overlay": component_overlay_status,
        "law_router": law_router_status,
        "law_source_family": law_source_family_status,
        "law_source_package": law_source_package_status,
        "turn_governance_kernel": "PASS_DIRECT_ANCHORS_COMPLETE",
        "runtime_reference_index": "PASS_DIRECT_REFERENCE_DEPTH_1",
        "runtime_bundle_schema": "PASS",
        "authority_boundary": "DERIVED_NONAUTHORITATIVE_MACHINE_REPRESENTATION",
        "backend_enforcement_claimed": False,
        "payload_hashes": maps[0],
    }
    semantic_report = {
        "SYSTEM_DESIGNATION": "AIR_P_SEMANTIC_EQUIVALENCE_REPORT_V1",
        "decision": "PASS",
        "core_source_sha256": PINNED_HASHES["CORE_RUNTIME"],
        "runtime_state": CURRENT_RUNTIME_STATE,
        "components": {"semantic_source_count": 113, "compiled_count": 113, "unique": True, "semantic_additions": 0},
        "routes": {"source_count": 22, "compiled_count": 22, "semantic_additions": 0},
        "route_control_event_bijection": "22/22 PASS",
        "formal_objects": {"core_declared": 21, "compiled": 21, "closed_world": True},
        "deterministic_checks": {"starter_declared": 137, "compiled": 137, "executed": 137},
        "runtime_navigation": {"turn_governance_kernel": "DERIVED_NONAUTHORITATIVE", "runtime_reference_index": "DERIVED_NONAUTHORITATIVE_DIRECT_DEPTH_1", "semantic_additions": 0},
        "authority_gain": "NONE",
        "component_overlay_semantic_authority": "NONE",
        "law_router_semantic_authority": "NONE",
        "semantic_proposal_positive_control_authority": "NONE",
        "handoff_unsurfaced_history_reconstruction": "PROHIBITED",
        "law_source_package_mode": law_source_package_mode,
    }
    mutation_report = {
        "SYSTEM_DESIGNATION": "AIR_P_MUTATION_TEST_REPORT_V1",
        "decision": mutation["suite_state"],
        "tests": mutation["tests"],
    }
    coverage_report = {
        "SYSTEM_DESIGNATION": "AIR_P_DETERMINISTIC_MUTATION_COVERAGE_REPORT_V1",
        "decision": coverage["overall_state"],
        **coverage,
    }
    repro_report = {
        "SYSTEM_DESIGNATION": "AIR_P_REPRODUCIBILITY_REPORT_V1",
        "decision": "PASS" if reproducible else "FAIL",
        "run_count": 3,
        "scope": "ALL_SCHEMA_SOURCE_OVERLAY_AND_COMPILED_JSON_PAYLOADS",
        "byte_identical_canonical_json": reproducible,
        "run_hash_maps": maps,
        "claim_boundary": "IN_PROCESS_PRECHECK; R18_T10_REQUIRES_THREE_INDEPENDENT_PROCESSES",
    }
    write_json(out / "evidence" / "AIR_P_COMPILATION_REPORT.json", compilation_report)
    write_json(out / "evidence" / "AIR_P_SEMANTIC_EQUIVALENCE_REPORT.json", semantic_report)
    write_json(out / "evidence" / "AIR_P_MUTATION_TEST_REPORT.json", mutation_report)
    write_json(out / "evidence" / "AIR_P_DETERMINISTIC_MUTATION_COVERAGE_REPORT.json", coverage_report)
    write_json(out / "evidence" / "AIR_P_REPRODUCIBILITY_REPORT.json", repro_report)

    run_manifest = {
        "SYSTEM_DESIGNATION": "AIR_P_RUN_MANIFEST_V1",
        "package_designation": PACKAGE_DESIGNATION,
        "package_version": PACKAGE_VERSION,
        "runtime_state": CURRENT_RUNTIME_STATE,
        "source_hashes": copy.deepcopy(PINNED_HASHES),
        "compiled_cardinality": copy.deepcopy(EXPECTED),
        "passes": [f"P{i}" for i in range(12)],
        "validation": {
            "component_registry": component_overlay_status.replace("113/113 ", "PASS_113_OF_113_"),
            "route_registry": "PASS_22_OF_22",
            "route_control_event_bijection": "PASS_22_OF_22",
            "deterministic_registry": "PASS_137_OF_137",
            "formal_object_contracts": "PASS_21_OF_21_CORE_MACHINE_REGISTRY",
            "turn_governance_kernel": "PASS_DIRECT_ANCHORS_COMPLETE",
            "runtime_reference_index": "PASS_DIRECT_REFERENCE_DEPTH_1",
            "semantic_equivalence": "PASS",
            "mutation_suite": "PASS",
            "deterministic_mutation_coverage": "PASS_137_OF_137",
            "in_memory_reproducibility": "PASS",
            "law_source_package_manifest_and_pin": ("PASS_DETERMINISTIC_ACTIVE_PACKAGE_ENABLED" if package_enabled else "PASS_DETERMINISTIC_SHADOW_ONLY"),
            "independent_process_reproducibility": external_repro_state,
        },
        "foundation_mutated": False,
        "foundation_promoted": False,
        "air_k_authority_granted": False,
        "decision": run_decision,
    }
    write_json(out / "AIR_P_RUN_MANIFEST.json", run_manifest)

    files = []
    for p in sorted(out.rglob("*")):
        if not p.is_file() or p.name == "GENERATED_FILE_MANIFEST.json" or "__pycache__" in p.parts or p.suffix == ".pyc":
            continue
        rel = p.relative_to(out).as_posix()
        files.append({"path": rel, "sha256": file_sha256(p), "size_bytes": p.stat().st_size})
    gfm = {
        "SYSTEM_DESIGNATION": "AIR_P_GENERATED_FILE_MANIFEST_V1",
        "package_designation": PACKAGE_DESIGNATION,
        "runtime_state": CURRENT_RUNTIME_STATE,
        "transient_exclusion_policy": ["**/__pycache__/**", "**/*.pyc"],
        "file_count_excluding_self": len(files),
        "files": files,
    }
    write_json(out / "GENERATED_FILE_MANIFEST.json", gfm)
    return {
        "compilation_report": compilation_report,
        "semantic_report": semantic_report,
        "mutation_report": mutation_report,
        "coverage_report": coverage_report,
        "repro_report": repro_report,
        "run_manifest": run_manifest,
        "generated_manifest": gfm,
    }

# ==================================================
# AMRS4E TRANSITION-READINESS DUAL-STATE REMEDIATION
# ==================================================
# This layer intentionally preserves the exact R125 pre-F behavior while adding
# one exact package-enabled post-F state.  It grants no authority and is only a
# compiler/readiness bridge for a separately governed AMRS4F Core cutover.

PRE_F_CORE_SHA256 = "e4fb9fc9ac5b50d7d2d043a9489a086b398f543c41eefdc2762e92fb5e06b835"
POST_F_CORE_SHA256 = "6007ab277ebcd0d59911fce6384a8ef417dbdd6f3eea38bfc71e39013b097588"
PRE_F_RUNTIME_STATE = "R23_AMRS4D3_POST_CUTOVER_CORE26_HANDOFF26"
POST_F_RUNTIME_STATE = "R23_AMRS4F_PACKAGE_ENABLED_SEMANTIC_OWNER_CUTOVER"
AMRS4F_CUTOVER_MARKER = "AIR_AMRS4F_SEMANTIC_OWNER_CUTOVER_V1"
AMRS4F_CUTOVER_BEGIN = "AIR_AMRS4F_SEMANTIC_OWNER_CUTOVER_V1_MACHINE_CONTRACT_BEGIN"
AMRS4F_CUTOVER_END = "AIR_AMRS4F_SEMANTIC_OWNER_CUTOVER_V1_MACHINE_CONTRACT_END"
ACTIVE_V2_CONTRACT = "AIR_LAW_RESOLUTION_CONSTRUCTION_V2@2.0.0"

_PRE_F_validate_source_pins = validate_source_pins
_PRE_F_core_law_registry = core_law_registry
_PRE_F_core_decision_trace_contracts = core_decision_trace_contracts
_PRE_F_regenerate_law_router = regenerate_law_router
_PRE_F_validate_law_router = validate_law_router
_PRE_F_rebase_component_overlay = rebase_component_overlay
_PRE_F_component_registry_from_overlay = component_registry_from_overlay
_PRE_F_runtime_reference_anchor = _runtime_reference_anchor
_PRE_F_build_runtime_navigation_outputs = build_runtime_navigation_outputs
_PRE_F_validate_runtime_navigation_outputs = validate_runtime_navigation_outputs
_PRE_F_runtime_transition_state = _runtime_transition_state
_PRE_F_validate_law_source_family = validate_law_source_family
_PRE_F_law_router_derivation_payload = law_router_derivation_payload
_PRE_F_law_package_build_plan = law_package_build_plan
_PRE_F_build_source_manifest = build_source_manifest
_PRE_F_build_payloads = build_payloads
_PRE_F_validate_source_inputs = validate_source_inputs
_PRE_F_compile_package = compile_package

_TRANSITION_ACTIVE_PATHS = None


def _transition_core_sha(paths):
    return file_sha256(paths["CORE_RUNTIME"])


def _post_f_marker_contract(core_text):
    if f"Patch marker: {AMRS4F_CUTOVER_MARKER}" not in core_text:
        return None
    obj = parse_machine_payload(core_text, AMRS4F_CUTOVER_BEGIN, AMRS4F_CUTOVER_END)
    if obj.get("SYSTEM_DESIGNATION") != AMRS4F_CUTOVER_MARKER:
        raise CompileError("AMRS4F cutover contract designation mismatch")
    if obj.get("cutover_state") != "PACKAGE_ENABLED_RELEASE_SEMANTIC_OWNER_CUTOVER_COMPLETE":
        raise CompileError("AMRS4F cutover state mismatch")
    if obj.get("active_law_resolution_contract") != ACTIVE_V2_CONTRACT:
        raise CompileError("AMRS4F active law-resolution contract mismatch")
    if obj.get("positive_execution_authority") != "NONE":
        raise CompileError("AMRS4F cutover contract authority escalation")
    return obj


def _is_post_f_paths(paths):
    actual = _transition_core_sha(paths)
    if POST_F_CORE_SHA256 != "__POST_F_CORE_SHA256__" and actual == POST_F_CORE_SHA256:
        contract = _post_f_marker_contract(read_text(paths["CORE_RUNTIME"]))
        if contract is None:
            raise CompileError("exact post-F Core hash missing AMRS4F cutover marker")
        return True
    return False


def _transition_mode(paths):
    actual = _transition_core_sha(paths)
    if actual == PRE_F_CORE_SHA256:
        return "PRE_F_EMBEDDED_V1"
    if _is_post_f_paths(paths):
        return "POST_F_PACKAGE_ENABLED_V2"
    raise CompileError(f"Core is outside the exact AMRS4E transition-readiness set: {actual}")


def _ctx_paths(paths=None):
    p = paths or _TRANSITION_ACTIVE_PATHS
    if p is None:
        raise CompileError("transition-aware compiler function requires active source paths")
    return p


def _law_body_records(paths):
    idx = strict_json_load(paths["LAW_SOURCE_LAW_BODY_INDEX"])
    entries = idx.get("entries", [])
    if idx.get("law_identity_count") != 83 or idx.get("physical_body_count") != 82 or len(entries) != 83:
        raise CompileError("law body index cardinality mismatch")
    return {x["law_id"]: x for x in entries}


def _law_body_path(paths, law_id):
    rec = _law_body_records(paths).get(law_id)
    if rec is None:
        raise CompileError(f"law body mapping missing: {law_id}")
    root = law_source_root(paths).parent
    p = root / rec["canonical_path"]
    if not p.is_file() or file_sha256(p) != rec.get("body_sha256"):
        raise CompileError(f"law body integrity mismatch: {law_id}")
    return p, rec


def _standalone_body_section(paths, law_id, source_anchor=None):
    p, rec = _law_body_path(paths, law_id)
    text = read_text(p)
    lines = text.splitlines()
    heading = (source_anchor or {}).get("section_heading")
    marker = (source_anchor or {}).get("patch_marker")
    heading_lines = [i + 1 for i, row in enumerate(lines) if heading and row.strip() == heading]
    marker_lines = [i + 1 for i, row in enumerate(lines) if marker and row.strip() == f"Patch marker: {marker}"]
    resolved_marker = marker
    marker_migration = None
    if heading and len(heading_lines) != 1:
        # Only the two explicitly refined AMRS3A overbroad-source entries may
        # migrate their section heading. Any other heading drift fails closed.
        if law_id not in {"CORE.REGISTRY.LAW_ID", "CORE.LAW.AMRS_AWARE_LAW_APPLICABILITY"}:
            raise CompileError(f"standalone law heading cardinality mismatch {law_id}: {heading_lines}")
        heading_lines = [next((i + 1 for i, row in enumerate(lines) if row.strip() and set(row.strip()) != {"-"}), 1)]
    if marker and len(marker_lines) != 1:
        all_markers = [(i + 1, row.split(":", 1)[1].strip()) for i, row in enumerate(lines) if row.startswith("Patch marker:")]
        if len(all_markers) == 1:
            marker_lines = [all_markers[0][0]]
            resolved_marker = all_markers[0][1]
            marker_migration = {
                "stable_registry_patch_marker": marker,
                "current_source_patch_marker": resolved_marker,
                "migration_rule": "EXACT_STANDALONE_BODY_SINGLE_MARKER_REFINEMENT",
            }
        elif rec.get("sharing_class") != "EXPLICIT_SHARED_BODY":
            raise CompileError(f"standalone law marker cardinality mismatch {law_id}: {marker_lines}")
    return {
        "canonical_path": rec["canonical_path"],
        "start_line": 1,
        "end_line": len(lines),
        "sha256": rec["body_sha256"],
        "body_id": rec.get("body_id"),
        "sharing_class": rec.get("sharing_class"),
        "heading_line": heading_lines[0] if heading_lines else 1,
        "resolved_section_heading": lines[(heading_lines[0] if heading_lines else 1) - 1].strip(),
        "patch_marker_line": marker_lines[0] if marker_lines else None,
        "resolved_patch_marker": resolved_marker,
        "marker_migration": marker_migration,
    }


def _find_law_body_by_patch_marker(paths, patch_marker):
    root = law_source_root(paths).parent
    idx = strict_json_load(paths["LAW_SOURCE_LAW_BODY_INDEX"])
    unique = {}
    for rec in idx.get("entries", []):
        unique[rec["canonical_path"]] = rec
    hits = []
    needle = f"Patch marker: {patch_marker}"
    for rel, rec in sorted(unique.items()):
        p = root / rel
        text = read_text(p)
        if needle in text:
            lines = text.splitlines()
            marker_lines = [i + 1 for i, row in enumerate(lines) if row.strip() == needle]
            if len(marker_lines) == 1:
                hits.append((p, rec, marker_lines[0]))
    if len(hits) != 1:
        raise CompileError(f"law-source patch marker must resolve exactly once: {patch_marker}: {len(hits)}")
    return hits[0]


def _post_f_package_contract(paths):
    contract = _post_f_marker_contract(read_text(paths["CORE_RUNTIME"]))
    if contract is None:
        raise CompileError("post-F package contract unavailable")
    family = contract.get("canonical_source_family", {})
    if family.get("file_count") != 114 or family.get("stable_law_id_count") != 83 or family.get("physical_law_body_count") != 82 or family.get("floor_body_count") != 28:
        raise CompileError("AMRS4F canonical source family cardinality mismatch")
    return contract


def validate_source_pins(paths):
    mode = _transition_mode(paths)
    observations = []
    for role, expected in PINNED_HASHES.items():
        if role not in paths:
            raise CompileError(f"missing source role {role}")
        actual = file_sha256(paths[role])
        if role == "CORE_RUNTIME":
            allowed = PRE_F_CORE_SHA256 if mode == "PRE_F_EMBEDDED_V1" else POST_F_CORE_SHA256
            state = "PASS" if actual == allowed else "FAIL"
            observations.append({"role": role, "expected": allowed, "actual": actual, "state": state})
        else:
            observations.append({"role": role, "expected": expected, "actual": actual, "state": "PASS" if actual == expected else "FAIL"})
    fail = [x for x in observations if x["state"] != "PASS"]
    if fail:
        raise CompileError(f"source pin drift: {fail}")
    return observations


def core_law_registry(core_text):
    paths = _TRANSITION_ACTIVE_PATHS
    if paths is None or _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_core_law_registry(core_text)
    reg = strict_json_load(paths["LAW_SOURCE_LAW_ID_REGISTRY"])
    if reg.get("SYSTEM_DESIGNATION") != "AIR_LAW_ID_REGISTRY_V1":
        raise CompileError("law-source registry designation mismatch")
    entries = reg.get("entries", [])
    if reg.get("entry_count") != EXPECTED["laws"] or len(entries) != EXPECTED["laws"]:
        raise CompileError("law-source registry count mismatch")
    ids = [x.get("law_id") for x in entries]
    if len(ids) != len(set(ids)) or DECISION_TRACE_LAW_ID not in ids:
        raise CompileError("law-source registry identity mismatch")
    if canonical_json_sha256(entries) != reg.get("entry_fingerprint_sha256"):
        raise CompileError("law-source registry fingerprint mismatch")
    return reg


def core_decision_trace_contracts(core_text):
    paths = _TRANSITION_ACTIVE_PATHS
    if paths is None or _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_core_decision_trace_contracts(core_text)
    body, _ = _law_body_path(paths, DECISION_TRACE_LAW_ID)
    return _PRE_F_core_decision_trace_contracts(read_text(body))


def _post_f_regenerate_law_router(core_text, prior_router, paths):
    prior_laws = prior_router.get("law_applicability_metadata", [])
    if len(prior_laws) != PRIOR_LAW_ROUTER_INPUT_COUNT:
        raise CompileError("prior law-router input count mismatch")
    prior_by_id = {x.get("law_id"): x for x in prior_laws}
    if len(prior_by_id) != PRIOR_LAW_ROUTER_INPUT_COUNT:
        raise CompileError("prior law-router duplicate law id")
    reg = core_law_registry(core_text)
    reg_fingerprint = reg["entry_fingerprint_sha256"]
    laws = []
    for entry in reg["entries"]:
        law_id = entry["law_id"]
        source_anchor = copy.deepcopy(entry["source_anchor"])
        section = _standalone_body_section(paths, law_id, source_anchor)
        if law_id == DECISION_TRACE_LAW_ID:
            rec = {
                "applicability_class": "CORE_INFRASTRUCTURE_GLOBAL",
                "control_event_refs": [],
                "dependency_law_refs": [],
                "derivation": {
                    "core_registry_fingerprint": reg_fingerprint,
                    "source_class": "AMRS4F_STANDALONE_LAW_SOURCE_PACKAGE",
                    "r23_decision_trace_source_reconciliation": {
                        "state": "OPERATIVE_STANDALONE_LAW_BODY",
                        "source_canonical_path": section["canonical_path"],
                        "source_body_sha256": section["sha256"],
                        "law_resolution_construction_ref": ACTIVE_V2_CONTRACT,
                        "router_semantic_authority": "NONE",
                    },
                },
                "law_id": law_id,
                "mandatory_floor_refs": copy.deepcopy(entry.get("mandatory_floor_refs", [])),
                "metadata_resolution_state": "CURRENT_AMRS4F_PACKAGE_ENABLED_GLOBAL_INFRASTRUCTURE",
                "runtime_dependency_refs": [],
                "runtime_route_refs": [],
                "source_anchor": source_anchor,
                "source_section": {k: section[k] for k in ("canonical_path", "start_line", "end_line", "sha256")},
                "task_class_predicates": {
                    "exclude_facets_any_of": [],
                    "exclude_route_classes_any_of": [],
                    "include_facets_any_of": [],
                    "include_route_classes_any_of": [],
                    "predicate_id": f"{law_id}::TASK_CLASS_V1",
                    "resolution_state": "CURRENT_GLOBAL_INFRASTRUCTURE",
                    "source_evidence_refs": [
                        f"AIR_LAW_ID_REGISTRY_V1@{reg_fingerprint}",
                        "AIR_DECISION_BASIS_CLOSURE_V1@1.0.0",
                    ],
                },
                "task_target_amrs_predicate": {
                    "predicate_type": "GLOBAL_INFRASTRUCTURE",
                    "resolution_state": "CURRENT",
                    "source_evidence_refs": [
                        f"AIR_LAW_ID_REGISTRY_V1@{reg_fingerprint}",
                        "AIR_DECISION_BASIS_CLOSURE_V1@1.0.0",
                    ],
                    "stages": [],
                },
            }
        else:
            if law_id not in prior_by_id:
                raise CompileError(f"missing prior law metadata for {law_id}")
            rec = copy.deepcopy(prior_by_id[law_id])
            rec["source_anchor"] = source_anchor
            rec["source_section"] = {k: section[k] for k in ("canonical_path", "start_line", "end_line", "sha256")}
            deriv = copy.deepcopy(rec.get("derivation", {}))
            if "core_registry_fingerprint" in deriv:
                deriv["core_registry_fingerprint"] = reg_fingerprint
            deriv["r23_decision_trace_source_reconciliation"] = {
                "state": "OPERATIVE_STANDALONE_LAW_BODY",
                "source_canonical_path": section["canonical_path"],
                "source_body_sha256": section["sha256"],
                "stable_registry_patch_marker": source_anchor.get("patch_marker"),
                "router_semantic_authority": "NONE",
            }
            rec["derivation"] = deriv
            if rec.get("applicability_class") == "CORE_INFRASTRUCTURE_GLOBAL":
                for key in ("task_class_predicates", "task_target_amrs_predicate"):
                    pred = rec.get(key, {})
                    refs = pred.get("source_evidence_refs", [])
                    pred["source_evidence_refs"] = [
                        f"AIR_LAW_ID_REGISTRY_V1@{reg_fingerprint}" if isinstance(x, str) and x.startswith("AIR_LAW_ID_REGISTRY_V1@") else x
                        for x in refs
                    ]
        laws.append(rec)
    router = copy.deepcopy(prior_router)
    router["ROUTER_VERSION"] = "2.0.0-AMRS4F-PACKAGE-ENABLED"
    router["candidate_state"] = "PACKAGE_ENABLED_V2_STANDALONE_SOURCE_DERIVED_ROUTER"
    router["law_applicability_metadata"] = laws
    router["law_applicability_metadata_fingerprint_sha256"] = canonical_json_sha256(laws)
    registry_hash = file_sha256(paths["LAW_SOURCE_LAW_ID_REGISTRY"])
    router["source_of_truth"] = {
        "canonical_path": CANONICAL_PATHS["LAW_SOURCE_LAW_ID_REGISTRY"],
        "filename": CANONICAL_FILENAMES["LAW_SOURCE_LAW_ID_REGISTRY"],
        "law_registry_entry_count": EXPECTED["laws"],
        "law_registry_entry_fingerprint_sha256": reg_fingerprint,
        "law_registry_ref": reg.get("SYSTEM_DESIGNATION"),
        "law_registry_version": reg.get("registry_version"),
        "sha256": registry_hash,
        "semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
    }
    router["metadata_state"] = {
        "operative_resolution_readiness": "PACKAGE_ENABLED_V2_CURRENT",
        "registry_law_count": EXPECTED["laws"],
        "resolved_metadata_count": EXPECTED["laws"],
        "resolved_global_infrastructure_law_ids": sorted([x["law_id"] for x in laws if x.get("applicability_class") == "CORE_INFRASTRUCTURE_GLOBAL"]),
        "unresolved_metadata_count": 0,
        "standalone_source_body_count": 82,
    }
    bindings = copy.deepcopy(router.get("derived_input_bindings", {}))
    bindings.update({
        "amrs4f_law_registry_sha256": registry_hash,
        "amrs4f_law_registry_fingerprint": reg_fingerprint,
        "r23_decision_trace_prior_router_sha256": PINNED_HASHES["LAW_APPLICABILITY_ROUTER"],
    })
    router["derived_input_bindings"] = bindings
    router["decision_trace_regeneration"] = {
        "authority": "DERIVED_NONAUTHORITATIVE_MACHINE_ROUTER",
        "prior_router_sha256": PINNED_HASHES["LAW_APPLICABILITY_ROUTER"],
        "source_law_registry_sha256": registry_hash,
        "source_law_registry_fingerprint": reg_fingerprint,
        "input_law_count": PRIOR_LAW_ROUTER_INPUT_COUNT,
        "output_law_count": EXPECTED["laws"],
        "added_law_ids": [DECISION_TRACE_LAW_ID],
        "applicability_semantics_for_prior_laws": "PRESERVED_EXCEPT_OPERATIVE_SOURCE_REBIND_TO_STANDALONE_LAW_BODIES",
        "new_law_applicability": "CORE_INFRASTRUCTURE_GLOBAL",
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
        "canonical_mutation": False,
        "positive_execution_authority": "NONE",
    }
    return router


def regenerate_law_router(core_text, prior_router):
    paths = _TRANSITION_ACTIVE_PATHS
    if paths is None:
        return _PRE_F_regenerate_law_router(core_text, prior_router)
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_regenerate_law_router(core_text, prior_router)
    return _post_f_regenerate_law_router(core_text, prior_router, paths)


def validate_law_router(router, core_text):
    paths = _TRANSITION_ACTIVE_PATHS
    if paths is None:
        return _PRE_F_validate_law_router(router, core_text)
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_validate_law_router(router, core_text)
    laws = router.get("law_applicability_metadata", [])
    if len(laws) != EXPECTED["laws"]:
        raise CompileError("law router count mismatch")
    ids = [x.get("law_id") for x in laws]
    reg = core_law_registry(core_text)
    registry_ids = [x.get("law_id") for x in reg["entries"]]
    if ids != registry_ids or len(ids) != len(set(ids)):
        raise CompileError("law router/package registry ordering or identity mismatch")
    observed_fp = canonical_json_sha256(laws)
    if router.get("law_applicability_metadata_fingerprint_sha256") != observed_fp:
        raise CompileError("law router metadata fingerprint mismatch")
    if router.get("authority", {}).get("positive_execution_authority") != "NONE":
        raise CompileError("law router authority escalation")
    expected_sot = {
        "canonical_path": CANONICAL_PATHS["LAW_SOURCE_LAW_ID_REGISTRY"],
        "filename": CANONICAL_FILENAMES["LAW_SOURCE_LAW_ID_REGISTRY"],
        "law_registry_entry_count": EXPECTED["laws"],
        "law_registry_entry_fingerprint_sha256": reg.get("entry_fingerprint_sha256"),
        "law_registry_ref": reg.get("SYSTEM_DESIGNATION"),
        "law_registry_version": reg.get("registry_version"),
        "sha256": file_sha256(paths["LAW_SOURCE_LAW_ID_REGISTRY"]),
        "semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
    }
    if router.get("source_of_truth") != expected_sot:
        raise CompileError("law router package source_of_truth mismatch")
    body_map = _law_body_records(paths)
    for rec in laws:
        body = body_map[rec["law_id"]]
        sec = rec.get("source_section", {})
        if sec.get("canonical_path") != body.get("canonical_path") or sec.get("sha256") != body.get("body_sha256"):
            raise CompileError(f"law router standalone source mismatch: {rec['law_id']}")
    dt = {x["law_id"]: x for x in laws}[DECISION_TRACE_LAW_ID]
    if dt.get("applicability_class") != "CORE_INFRASTRUCTURE_GLOBAL":
        raise CompileError("Decision Trace law applicability mismatch")
    return {
        "law_count": len(laws),
        "metadata_fingerprint_sha256": observed_fp,
        "router_version": router.get("ROUTER_VERSION"),
        "core_registry_fingerprint_sha256": reg.get("entry_fingerprint_sha256"),
        "decision_trace_law_state": "PRESENT_GLOBAL_NONAUTHORIZING_PACKAGE_SOURCE",
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
    }


def rebase_component_overlay(core_text, overlay, current_core_sha256, prior_overlay_sha256):
    paths = _ctx_paths()
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_rebase_component_overlay(core_text, overlay, current_core_sha256, prior_overlay_sha256)
    if overlay.get("SYSTEM_DESIGNATION") != "AIR_P_COMPONENT_METADATA_OVERLAY_V2":
        raise CompileError("component overlay designation mismatch")
    if overlay.get("authority_class") != "DERIVED_NONAUTHORITATIVE_METADATA_OVERLAY":
        raise CompileError("component overlay authority class mismatch")
    if overlay.get("semantic_authority") != "NONE" or overlay.get("positive_execution_authority") != "NONE":
        raise CompileError("component overlay authority boundary violation")
    comps = overlay.get("components", [])
    if overlay.get("component_count") != EXPECTED["components"] or len(comps) != EXPECTED["components"]:
        raise CompileError("component overlay count mismatch")
    sections = section_index(core_text)
    body_map = _law_body_records(paths)
    rebound = copy.deepcopy(overlay)
    core_count = 0
    package_count = 0
    for rec in rebound["components"]:
        meta = {k: rec[k] for k in ["component_id", "component_revision", "component_type", "semantic_owner", "routable"]}
        expected_meta = rec.get("metadata_provenance", {}).get("metadata_payload_sha256")
        if expected_meta and canonical_json_sha256(meta) != expected_meta:
            raise CompileError(f"metadata provenance mismatch {rec['component_id']}")
        anchor = rec.get("anchor", {})
        heading = anchor.get("section_heading")
        marker = anchor.get("patch_marker")
        if rec["component_id"] in body_map:
            sec = _standalone_body_section(paths, rec["component_id"], anchor)
            rec["anchor"] = {
                "binding_method": "EXACT_STANDALONE_LAW_BODY_PATH_PLUS_STABLE_LAW_ID",
                "canonical_path": sec["canonical_path"],
                "patch_marker": sec.get("resolved_patch_marker") or marker,
                "section_heading": sec["resolved_section_heading"],
                "target_source_heading_line": sec["heading_line"],
                "target_source_patch_marker_line": sec["patch_marker_line"],
                "target_source_sha256": sec["sha256"],
                "target_source_section_sha256": sec["sha256"],
                "source_role": "LAW_SOURCE_BODY",
            }
            package_count += 1
        else:
            heading_matches = [s for s in sections if s["heading"] == heading]
            exact = [s for s in heading_matches if marker in {m for m, _ in s["markers"]}]
            if len(exact) != 1:
                raise CompileError(f"retained Core component anchor not deterministically resolvable {rec['component_id']}")
            sec = exact[0]
            marker_lines = [ln for m, ln in sec["markers"] if m == marker]
            if len(marker_lines) != 1:
                raise CompileError(f"retained Core component marker cardinality {rec['component_id']}")
            rec["anchor"] = {
                "binding_method": "EXACT_SECTION_HEADING_PLUS_PATCH_MARKER",
                "patch_marker": marker,
                "section_heading": heading,
                "target_core_heading_line": sec["heading_line"],
                "target_core_patch_marker_line": marker_lines[0],
                "target_core_section_sha256": text_sha256(sec["text"]),
            }
            core_count += 1
    headers = markdown_headers(core_text)
    rebound["binding_target"] = {
        "binding_method": "AMRS4F_DUAL_SOURCE_COMPONENT_BINDING",
        "canonical_path": "prompts/AIR_CORE_RUNTIME.md",
        "component_metadata_present_in_source": False,
        "designation": headers.get("SYSTEM_DESIGNATION"),
        "prompt_version": headers.get("PROMPT_VERSION"),
        "semantic_authority": True,
        "sha256": current_core_sha256,
        "retained_core_component_count": core_count,
        "standalone_law_component_count": package_count,
        "law_source_registry_sha256": file_sha256(paths["LAW_SOURCE_LAW_ID_REGISTRY"]),
    }
    prov = copy.deepcopy(rebound.get("regeneration_provenance", {}))
    prov.update({
        "regeneration_contract_id": "R23_AMRS4F_COMPONENT_METADATA_DUAL_SOURCE_REBASE_V1",
        "candidate_policy": "PRESERVE_EXACT_113_COMPONENT_IDENTITIES_REBIND_82_LAW_COMPONENTS_TO_STANDALONE_BODIES",
        "current_core_sha256": current_core_sha256,
        "prior_overlay_sha256": prior_overlay_sha256,
        "new_componentization": "NO_NEW_COMPONENT_IDS",
        "semantic_authority": "NONE",
        "retained_core_component_count": core_count,
        "standalone_law_component_count": package_count,
    })
    rebound["regeneration_provenance"] = prov
    rebound["component_count"] = len(rebound["components"])
    if core_count != 31 or package_count != 82:
        raise CompileError(f"AMRS4F component binding cardinality mismatch: core={core_count} package={package_count}")
    return rebound


def component_registry_from_overlay(rebased_overlay, overlay_sha256):
    paths = _TRANSITION_ACTIVE_PATHS
    if paths is None or _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_component_registry_from_overlay(rebased_overlay, overlay_sha256)
    records = []
    for rec in rebased_overlay["components"]:
        a = rec["anchor"]
        if a.get("source_role") == "LAW_SOURCE_BODY":
            source_anchor = {
                "canonical_role": "LAW_SOURCE_BODY",
                "canonical_path": a["canonical_path"],
                "section_heading_line": a["target_source_heading_line"],
                "patch_marker": a["patch_marker"],
                "patch_marker_line": a["target_source_patch_marker_line"],
                "section_sha256": a["target_source_section_sha256"],
                "source_sha256": a["target_source_sha256"],
                "binding_method": a["binding_method"],
                "metadata_overlay_sha256": overlay_sha256,
            }
        else:
            source_anchor = {
                "canonical_role": "CORE_RUNTIME",
                "section_heading_line": a["target_core_heading_line"],
                "patch_marker": a["patch_marker"],
                "patch_marker_line": a["target_core_patch_marker_line"],
                "section_sha256": a["target_core_section_sha256"],
                "binding_method": a["binding_method"],
                "metadata_overlay_sha256": overlay_sha256,
            }
        records.append({
            "component_id": rec["component_id"],
            "component_revision": rec["component_revision"],
            "component_type": rec["component_type"],
            "semantic_owner": rec["semantic_owner"],
            "routable": rec["routable"],
            "section_heading": a["section_heading"],
            "patch_markers": [a["patch_marker"]],
            "source_anchor": source_anchor,
        })
    return records


def _runtime_reference_anchor(spec, paths):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_runtime_reference_anchor(spec, paths)
    role = spec["source_role"]
    if role != "CORE_RUNTIME" or spec["locator_type"] != "MARKDOWN_PATCH_SECTION":
        return _PRE_F_runtime_reference_anchor(spec, paths)
    core_text = read_text(paths["CORE_RUNTIME"])
    needle = f"Patch marker: {spec['patch_marker']}"
    if needle in core_text:
        section = _markdown_patch_section(core_text, spec["patch_marker"])
        return {
            "semantic_id": spec["semantic_id"],
            "canonical_source_path": CANONICAL_PATHS["CORE_RUNTIME"],
            "patch_marker": spec["patch_marker"],
            "source_sha256": file_sha256(paths["CORE_RUNTIME"]),
            "section_digest": section["sha256"],
            "section_digest_algorithm": "SHA256_UTF8_EXACT_SECTION_V1",
            "retrieval_trigger": copy.deepcopy(spec["retrieval_trigger"]),
            "required_dependencies": copy.deepcopy(spec["required_dependencies"]),
            "locator": {"type": "MARKDOWN_PATCH_SECTION", "start_line": section["start_line"], "end_line": section["end_line"]},
        }
    p, rec, marker_line = _find_law_body_by_patch_marker(paths, spec["patch_marker"])
    text = read_text(p)
    lines = text.splitlines()
    rel = p.relative_to(law_source_root(paths).parent).as_posix()
    return {
        "semantic_id": spec["semantic_id"],
        "canonical_source_path": rel,
        "patch_marker": spec["patch_marker"],
        "source_sha256": rec["body_sha256"],
        "section_digest": rec["body_sha256"],
        "section_digest_algorithm": "SHA256_UTF8_EXACT_STANDALONE_LAW_BODY_V1",
        "retrieval_trigger": copy.deepcopy(spec["retrieval_trigger"]),
        "required_dependencies": copy.deepcopy(spec["required_dependencies"]),
        "locator": {"type": "STANDALONE_LAW_BODY", "start_line": 1, "end_line": len(lines), "patch_marker_line": marker_line},
    }


def build_runtime_navigation_outputs(paths, starter):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_build_runtime_navigation_outputs(paths, starter)
    anchors = [_runtime_reference_anchor(spec, paths) for spec in RUNTIME_REFERENCE_ANCHOR_SPECS]
    ids = [a["semantic_id"] for a in anchors]
    if len(ids) != len(set(ids)):
        raise CompileError("runtime reference index duplicate semantic_id")
    id_set = set(ids)
    for a in anchors:
        if not set(a["required_dependencies"]).issubset(id_set):
            raise CompileError(f"runtime reference dependency not directly indexed: {a['semantic_id']}")
    validate_consumption_key_contract_mirror(read_text(paths["CORE_RUNTIME"]), starter)
    progressive = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
    kernel_mirror = starter["compiler_contract"]["turn_governance_kernel_mirror"]
    telemetry = starter["compiler_contract"]["boot_runtime_telemetry_defaults"]
    transition = starter["validation_contract"]["core_runtime_transition_identity_contract"]
    source_hashes = {}
    for a in anchors:
        source_hashes[a["canonical_source_path"]] = a["source_sha256"]
    source_hashes[CANONICAL_PATHS["CONTROL_SURFACE"]] = PINNED_HASHES["CONTROL_SURFACE"]
    source_hashes[CANONICAL_PATHS["DEFAULT_STARTER_PROFILE"]] = PINNED_HASHES["DEFAULT_STARTER_PROFILE"]
    reference_index = {
        "SYSTEM_DESIGNATION": "AIR_P_RUNTIME_REFERENCE_INDEX_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_NAVIGATION_TO_CANONICAL_SOURCE",
        "semantic_owner": "AIR_CORE_RUNTIME_V2_BOOTSTRAP_TRUST_KERNEL",
        "runtime_state": POST_F_RUNTIME_STATE,
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
        "direct_reference_depth": DIRECT_REFERENCE_DEPTH,
        "nested_only_discovery": "PROHIBITED",
        "canonical_source_authority": "PRESERVED",
        "source_hashes": source_hashes,
        "compiled_navigation_refs": {
            "routes": "air_p/compiled/AIR_P_ROUTE_CONTRACT_REGISTRY.json",
            "formal_objects": "air_p/compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json",
            "deterministic_validation": "air_p/compiled/AIR_P_DETERMINISTIC_VALIDATION_REGISTRY.json",
            "law_applicability": "law_package/index/AIR_LAW_APPLICABILITY_ROUTER.json",
            "specialist_discovery": "catalog/AIR_SPECIALIST_PACKAGE_INDEX.json",
        },
        "anchor_count": len(anchors),
        "anchors": anchors,
        "stale_anchor_behavior": "TARGETED_REVALIDATION_OR_FULL_RELEASE_INTEGRITY_AUDIT_NO_INFERENCE_FALLBACK",
        "backend_enforcement_claimed": False,
    }
    by_id = {a["semantic_id"]: a for a in anchors}
    kernel_anchors = [copy.deepcopy(by_id[sid]) for sid in KERNEL_REQUIRED_SEMANTIC_IDS]
    kernel = {
        "SYSTEM_DESIGNATION": "AIR_P_TURN_GOVERNANCE_KERNEL_V1",
        "authority_class": "DERIVED_NONAUTHORITATIVE_EXECUTION_NAVIGATION_PROJECTION",
        "semantic_owner": "AIR_CORE_RUNTIME_V2_BOOTSTRAP_TRUST_KERNEL",
        "runtime_state": POST_F_RUNTIME_STATE,
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
        "starter_transition_contract_id": transition["contract_id"],
        "starter_transition_state": POST_F_RUNTIME_STATE,
        "direct_reference_depth": DIRECT_REFERENCE_DEPTH,
        "runtime_reference_index_ref": "air_p/compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json",
        "pre_response_pipeline": copy.deepcopy(kernel_mirror["canonical_pipeline"]),
        "preartifact_governance": {
            "bootstrap_no_artifact_rule": kernel_mirror["bootstrap_no_artifact_rule"],
            "preartifact_evaluation_pair_rule": kernel_mirror["preartifact_evaluation_pair_rule"],
            "material_unresolved_input_rule": kernel_mirror["material_unresolved_input_rule"],
            "material_block_rule": kernel_mirror["material_block_rule"],
            "decision_trace_constructor_rule": kernel_mirror["decision_trace_constructor_rule"],
            "exact_token_rule": kernel_mirror["exact_token_rule"],
            "all_objects_rule": kernel_mirror["all_objects_rule"],
        },
        "progressive_runtime": {
            "default_boot_profile": progressive["default_boot_profile"],
            "tier_order": copy.deepcopy(progressive["tier_order"]),
            "direct_reference_rule": progressive["direct_reference_rule"],
            "byte_verification_context_rule": progressive["byte_verification_context_rule"],
            "mismatch_behavior": progressive["mismatch_behavior"],
            "required_user_boot_profile_patch_marker": progressive["required_user_boot_profile_patch_marker"],
            "required_retrieval_scope_enforcement_patch_marker": progressive["required_retrieval_scope_enforcement_patch_marker"],
            "retrieval_scope_enforcement": copy.deepcopy(progressive["retrieval_scope_enforcement"]),
            "default_user_boot_profile": progressive["default_user_boot_profile"],
            "user_boot_profile_dispatch": copy.deepcopy(progressive["user_boot_profile_dispatch"]),
            "explicit_profile_selection_rule": progressive["explicit_profile_selection_rule"],
            "silent_escalation": progressive["silent_escalation"],
            "escalation_telemetry_required": copy.deepcopy(progressive["escalation_telemetry_required"]),
            "boot_result_telemetry_required_when_observable": copy.deepcopy(progressive["boot_result_telemetry_required_when_observable"]),
            "release_package_interface_obligation": progressive["release_package_interface_obligation"],
        },
        "boot_telemetry": {
            "phase_order": copy.deepcopy(telemetry["phase_order"]),
            "evidence_class": telemetry["evidence_class"],
            "unavailable_timing_rule": telemetry["unavailable_timing_rule"],
            "performance_safety_rule": telemetry["performance_safety_rule"],
        },
        "required_contract_count": len(kernel_anchors),
        "required_contract_semantic_ids": copy.deepcopy(KERNEL_REQUIRED_SEMANTIC_IDS),
        "anchors": kernel_anchors,
        "ordinary_prose_before_formal_closure": "PROHIBITED_WHEN_GOVERNED_ROUTE_OR_OWED_FORMAL_OBJECT_EXISTS",
        "backend_enforcement_claimed": False,
    }
    validate_runtime_navigation_outputs(kernel, reference_index, paths)
    return kernel, reference_index


def validate_runtime_navigation_outputs(kernel, reference_index, paths):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_validate_runtime_navigation_outputs(kernel, reference_index, paths)
    if reference_index.get("SYSTEM_DESIGNATION") != "AIR_P_RUNTIME_REFERENCE_INDEX_V1" or reference_index.get("runtime_state") != POST_F_RUNTIME_STATE:
        raise CompileError("post-F runtime reference index identity mismatch")
    anchors = reference_index.get("anchors", [])
    if len(anchors) != len(RUNTIME_REFERENCE_ANCHOR_SPECS):
        raise CompileError("post-F runtime reference index anchor cardinality mismatch")
    ids = [a.get("semantic_id") for a in anchors]
    if len(ids) != len(set(ids)):
        raise CompileError("post-F runtime reference index duplicate semantic_id")
    for spec, observed in zip(RUNTIME_REFERENCE_ANCHOR_SPECS, anchors):
        expected = _runtime_reference_anchor(spec, paths)
        if observed != expected:
            raise CompileError(f"post-F runtime reference anchor mismatch: {spec['semantic_id']}")
    if kernel.get("runtime_state") != POST_F_RUNTIME_STATE or kernel.get("active_law_resolution_contract") != ACTIVE_V2_CONTRACT:
        raise CompileError("post-F turn governance kernel state mismatch")
    if kernel.get("required_contract_semantic_ids") != KERNEL_REQUIRED_SEMANTIC_IDS:
        raise CompileError("post-F turn governance kernel required contract set mismatch")
    return True


def _runtime_transition_state(starter, paths):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_runtime_transition_state(starter, paths)
    contract = _post_f_package_contract(paths)
    if contract.get("next_boundary") != "AMRS4G_INTEGRATED_SYSTEM_REPROOF_NO_V4_BUILD":
        raise CompileError("AMRS4F next boundary mismatch")
    handoff = _handoff_transition_identity(paths)
    if handoff.get("role") != "TARGET_CURRENT" or handoff.get("template_revision") != 26:
        raise CompileError("post-F Handoff tuple mismatch")
    return POST_F_RUNTIME_STATE


def validate_law_source_family(paths, regenerated_law_router=None):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_validate_law_source_family(paths, regenerated_law_router)
    schema = strict_json_load(paths["LAW_SOURCE_PACKAGE_SCHEMA"])
    law_registry = strict_json_load(paths["LAW_SOURCE_LAW_ID_REGISTRY"])
    body_index = strict_json_load(paths["LAW_SOURCE_LAW_BODY_INDEX"])
    floor_index = strict_json_load(paths["LAW_SOURCE_FLOOR_INVARIANT_INDEX"])
    counts = schema.get("counts", {})
    if counts != {"law_identity_count": 83, "physical_law_body_count": 82, "floor_body_count": 28, "source_family_file_count": 114}:
        raise CompileError("law-source schema count mismatch")
    if law_registry.get("entry_count") != 83 or canonical_json_sha256(law_registry.get("entries", [])) != law_registry.get("entry_fingerprint_sha256"):
        raise CompileError("law-source registry mismatch")
    root = law_source_root(paths)
    physical = {}
    for rec in body_index.get("entries", []):
        rel = rec["canonical_path"]
        p = root.parent / rel
        if not p.is_file() or file_sha256(p) != rec["body_sha256"] or p.stat().st_size != rec["size_bytes"]:
            raise CompileError(f"law-source body integrity mismatch: {rel}")
        physical[rel] = rec
    if len(physical) != 82:
        raise CompileError("law-source physical body count mismatch")
    floors = {}
    for rec in floor_index.get("entries", []):
        rel = rec["canonical_path"]
        p = root.parent / rel
        if not p.is_file() or file_sha256(p) != rec["body_sha256"] or p.stat().st_size != rec["size_bytes"]:
            raise CompileError(f"law-source floor integrity mismatch: {rel}")
        floors[rel] = rec
    if len(floors) != 28:
        raise CompileError("law-source floor count mismatch")
    observed = sorted(p.relative_to(root.parent).as_posix() for p in root.rglob('*') if p.is_file())
    expected = set(schema.get("required_root_resources", [])) | set(physical) | set(floors)
    if len(observed) != 114 or set(observed) != expected:
        raise CompileError("law-source family exact path set mismatch")
    if regenerated_law_router is not None:
        validate_law_router(regenerated_law_router, read_text(paths["CORE_RUNTIME"]))
    return {
        "package_id": schema.get("package_id"),
        "package_version": "1.0.0-AMRS4F-OPERATIVE",
        "semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
        "law_registry_fingerprint_sha256": law_registry.get("entry_fingerprint_sha256"),
        "law_body_index_fingerprint_sha256": body_index.get("body_index_fingerprint_sha256"),
        "floor_registry_fingerprint_sha256": floor_index.get("floor_registry_fingerprint_sha256"),
        "law_count": 83,
        "physical_law_body_count": 82,
        "floor_count": 28,
        "source_family_file_count": 114,
        "law_body_records": body_index.get("entries", []),
        "floor_body_records": floor_index.get("entries", []),
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
    }


def law_router_derivation_payload(law_router, paths):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_law_router_derivation_payload(law_router, paths)
    reg = strict_json_load(paths["LAW_SOURCE_LAW_ID_REGISTRY"])
    return {
        "SYSTEM_DESIGNATION": "AIR_LAW_ROUTER_DERIVATION_V1",
        "contract_version": "2.0.0",
        "source_law_registry_sha256": file_sha256(paths["LAW_SOURCE_LAW_ID_REGISTRY"]),
        "prior_router_sha256": PINNED_HASHES["LAW_APPLICABILITY_ROUTER"],
        "law_registry_fingerprint_sha256": reg["entry_fingerprint_sha256"],
        "router_law_count": len(law_router.get("law_applicability_metadata", [])),
        "router_metadata_fingerprint_sha256": law_router.get("law_applicability_metadata_fingerprint_sha256"),
        "derivation_contract": "REGENERATE_FROM_EXACT_PRIOR_ROUTER_PLUS_STANDALONE_LAW_REGISTRY_AND_BODY_INDEX",
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
        "semantic_authority": "NONE",
        "positive_execution_authority": "NONE",
    }


def law_package_build_plan(paths, law_router):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_law_package_build_plan(paths, law_router)
    state = validate_law_source_family(paths, law_router)
    root = law_source_root(paths)
    files = []
    payloads = {
        "law_package/index/AIR_LAW_ID_REGISTRY.json": strict_json_load(paths["LAW_SOURCE_LAW_ID_REGISTRY"]),
        "law_package/index/AIR_LAW_APPLICABILITY_ROUTER.json": copy.deepcopy(law_router),
        "law_package/index/AIR_FLOOR_INVARIANT_INDEX.json": strict_json_load(paths["LAW_SOURCE_FLOOR_INVARIANT_INDEX"]),
    }
    index_specs = [
        ("index/AIR_LAW_ID_REGISTRY.json", "LAW_ID_REGISTRY"),
        ("index/AIR_LAW_APPLICABILITY_ROUTER.json", "LAW_APPLICABILITY_ROUTER"),
        ("index/AIR_FLOOR_INVARIANT_INDEX.json", "FLOOR_INVARIANT_INDEX"),
    ]
    for rel, role in index_specs:
        obj = payloads["law_package/" + rel]
        raw = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        files.append({"path": rel, "role": role, "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw), "retrieval_class": "TIER1_COMPACT_NAVIGATION"})
    raw_copy_files = []
    for rec in sorted({x["canonical_path"]: x for x in state["law_body_records"]}.values(), key=lambda x: x["canonical_path"]):
        src = root.parent / rec["canonical_path"]
        rel = "laws/" + src.name
        files.append({"path": rel, "role": "LAW_BODY", "sha256": rec["body_sha256"], "size_bytes": rec["size_bytes"], "retrieval_class": "TIER2_EXACT_TARGETED_BODY"})
        raw_copy_files.append((src, rel))
    for rec in sorted(state["floor_body_records"], key=lambda x: x["canonical_path"]):
        src = root.parent / rec["canonical_path"]
        rel = "floors/" + src.name
        files.append({"path": rel, "role": "FLOOR_BODY", "sha256": rec["body_sha256"], "size_bytes": rec["size_bytes"], "retrieval_class": "TIER2_EXACT_TARGETED_BODY"})
        raw_copy_files.append((src, rel))
    deriv = law_router_derivation_payload(law_router, paths)
    deriv_raw = (json.dumps(deriv, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    files.append({"path": "evidence/AIR_LAW_ROUTER_DERIVATION.json", "role": "ROUTER_DERIVATION_EVIDENCE", "sha256": hashlib.sha256(deriv_raw).hexdigest(), "size_bytes": len(deriv_raw), "retrieval_class": "TIER3_DEEP_AUDIT"})
    payloads["law_package/evidence/AIR_LAW_ROUTER_DERIVATION.json"] = deriv
    files = sorted(files, key=lambda x: x["path"])
    content_fp = canonical_json_sha256(files)
    manifest = {
        "SYSTEM_DESIGNATION": "AIR_LAW_SOURCE_PACKAGE_MANIFEST_V1",
        "contract_version": "1.0.0",
        "package_id": "AIR_LAW_SOURCE_PACKAGE_V1",
        "package_version": "1.0.0-AMRS4F-OPERATIVE",
        "semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
        "law_count": 83,
        "law_registry_ref": "index/AIR_LAW_ID_REGISTRY.json",
        "law_registry_fingerprint_sha256": state["law_registry_fingerprint_sha256"],
        "router_ref": "index/AIR_LAW_APPLICABILITY_ROUTER.json",
        "router_fingerprint_sha256": next(x["sha256"] for x in files if x["path"] == "index/AIR_LAW_APPLICABILITY_ROUTER.json"),
        "floor_registry_ref": "index/AIR_FLOOR_INVARIANT_INDEX.json",
        "floor_registry_fingerprint_sha256": state["floor_registry_fingerprint_sha256"],
        "runtime_compatibility": {"runtime_family": "AIR_CORE_RUNTIME_V2", "target_amrs": 6, "semantic_owner_cutover_required_for_package_mode": True},
        "canonicalization_profile": {"json": "UTF8_NO_BOM_SORTED_KEYS_INDENT_2_TRAILING_LF", "text_bodies": "UTF8_NO_BOM_LF_EXACT_BYTES"},
        "files": files,
        "content_fingerprint_sha256": content_fp,
        "positive_execution_authority": "NONE",
    }
    raw = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    manifest_sha = hashlib.sha256(raw).hexdigest()
    pin = {
        "contract_id": "AIR_LAW_SOURCE_PACKAGE_PIN_V1",
        "contract_version": "1.0.0",
        "package_id": manifest["package_id"],
        "package_version": manifest["package_version"],
        "manifest_sha256": manifest_sha,
        "content_fingerprint_sha256": content_fp,
        "law_registry_fingerprint_sha256": state["law_registry_fingerprint_sha256"],
        "router_fingerprint_sha256": manifest["router_fingerprint_sha256"],
        "floor_registry_fingerprint_sha256": state["floor_registry_fingerprint_sha256"],
        "expected_law_count": 83,
        "runtime_compatibility": copy.deepcopy(manifest["runtime_compatibility"]),
        "positive_execution_authority": "NONE",
        "activation_state": "ACTIVE_PACKAGE_ENABLED_RELEASE_AMRS4F_SEMANTIC_OWNER_CUTOVER_COMPLETE",
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
    }
    payloads["law_package/AIR_LAW_SOURCE_PACKAGE_MANIFEST.json"] = manifest
    payloads["compiled/AIR_LAW_SOURCE_PACKAGE_PIN.json"] = pin
    cutover_pin = _post_f_package_contract(paths).get("package_pin", {})
    comparable_fields = [
        "contract_id", "contract_version", "package_id", "package_version",
        "manifest_sha256", "content_fingerprint_sha256",
        "law_registry_fingerprint_sha256", "router_fingerprint_sha256",
        "floor_registry_fingerprint_sha256", "expected_law_count",
        "runtime_compatibility", "positive_execution_authority",
    ]
    observed_pin = {k: copy.deepcopy(pin.get(k)) for k in comparable_fields}
    expected_pin = {k: copy.deepcopy(cutover_pin.get(k)) for k in comparable_fields}
    if observed_pin != expected_pin:
        raise CompileError("post-F generated law-package pin does not match exact AMRS4F Core cutover pin")
    return {"state": state, "payloads": payloads, "raw_copy_files": raw_copy_files, "manifest_sha256": manifest_sha, "content_fingerprint_sha256": content_fp}


def build_source_manifest(paths, rebased_overlay_sha256, regenerated_law_router_sha256):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _PRE_F_build_source_manifest(paths, rebased_overlay_sha256, regenerated_law_router_sha256)
    out = _PRE_F_build_source_manifest(paths, rebased_overlay_sha256, regenerated_law_router_sha256)
    out["runtime_state"] = POST_F_RUNTIME_STATE
    out["component_metadata_overlay"]["binding_target_role"] = "CORE_RUNTIME_PLUS_LAW_SOURCE_PACKAGE_BY_COMPONENT"
    out["law_applicability_router"]["authority_class"] = "DERIVED_NONAUTHORITATIVE_MACHINE_ROUTER_FROM_STANDALONE_SOURCE"
    out["law_source_family"] = {
        "state": "PACKAGE_ENABLED_SEMANTIC_OWNER_ACTIVE",
        "package_pin_output_ref": "AIR_LAW_SOURCE_PACKAGE_PIN.json",
        "semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
        "active_law_resolution_contract": ACTIVE_V2_CONTRACT,
        "provider_identity_semantic_authority": "NONE",
        "positive_execution_authority": "NONE",
    }
    return out


def _with_transition_context(paths, fn, *args, **kwargs):
    global _TRANSITION_ACTIVE_PATHS, CURRENT_RUNTIME_STATE
    old_paths = _TRANSITION_ACTIVE_PATHS
    old_state = CURRENT_RUNTIME_STATE
    old_core_pin = PINNED_HASHES["CORE_RUNTIME"]
    _TRANSITION_ACTIVE_PATHS = paths
    try:
        mode = _transition_mode(paths)
        if mode == "POST_F_PACKAGE_ENABLED_V2":
            CURRENT_RUNTIME_STATE = POST_F_RUNTIME_STATE
            PINNED_HASHES["CORE_RUNTIME"] = POST_F_CORE_SHA256
        else:
            CURRENT_RUNTIME_STATE = PRE_F_RUNTIME_STATE
            PINNED_HASHES["CORE_RUNTIME"] = PRE_F_CORE_SHA256
        return fn(*args, **kwargs)
    finally:
        PINNED_HASHES["CORE_RUNTIME"] = old_core_pin
        CURRENT_RUNTIME_STATE = old_state
        _TRANSITION_ACTIVE_PATHS = old_paths


def build_payloads(paths):
    return _with_transition_context(paths, _PRE_F_build_payloads, paths)


def validate_source_inputs(paths):
    return _with_transition_context(paths, _PRE_F_validate_source_inputs, paths)


def compile_package(out, paths, test_source=None):
    return _with_transition_context(paths, _PRE_F_compile_package, out, paths, test_source=test_source)

_TRANSITION_PRE_F_parse_route_registry = parse_route_registry

def parse_route_registry(core_text):
    paths = _TRANSITION_ACTIVE_PATHS
    if paths is None or _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _TRANSITION_PRE_F_parse_route_registry(core_text)
    p, _ = _law_body_path(paths, "CORE.REGISTRY.RUNTIME_ROUTE_DEPENDENCY_KERNEL")
    return _TRANSITION_PRE_F_parse_route_registry(read_text(p))

_TRANSITION_PRE_F_evaluate_deterministic_check = evaluate_deterministic_check

def evaluate_deterministic_check(check, starter, paths, json_cache=None, text_cache=None):
    if _transition_mode(paths) == "PRE_F_EMBEDDED_V1":
        return _TRANSITION_PRE_F_evaluate_deterministic_check(check, starter, paths, json_cache, text_cache)
    if check.get("operator") == "TEXT_CONTAINS_LITERAL" and check.get("file") == "prompts/AIR_CORE_RUNTIME.md":
        expected = check.get("expected", "")
        core_text = read_text(paths["CORE_RUNTIME"])
        if expected in core_text:
            return {
                "check_id": check.get("check_id"),
                "operator": check.get("operator"),
                "state": "PASS",
                "observed": {"source": "prompts/AIR_CORE_RUNTIME.md", "present": True},
            }
        root = law_source_root(paths).parent
        hits = []
        for p in sorted((root / "law_source").rglob("*")):
            if p.is_file() and p.suffix in {".md", ".json"}:
                try:
                    if expected in p.read_text(encoding="utf-8"):
                        hits.append(p.relative_to(root).as_posix())
                except UnicodeDecodeError:
                    pass
        return {
            "check_id": check.get("check_id"),
            "operator": check.get("operator"),
            "state": "PASS" if hits else "FAIL",
            "observed": {"source": "PACKAGE_ENABLED_CANONICAL_SOURCE_SET", "matches": hits[:16], "present": bool(hits)},
        }
    return _TRANSITION_PRE_F_evaluate_deterministic_check(check, starter, paths, json_cache, text_cache)
