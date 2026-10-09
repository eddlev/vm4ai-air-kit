import hashlib
import importlib.util
import json
import os
import re
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("air_p_compiler", HERE / "compiler" / "compile_air_p.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class AirPPostCutoverCompilerTests(unittest.TestCase):
    def test_source_contract_discovery(self):
        result = MOD.validate_source_inputs()
        self.assertEqual(result["decision"], "PASS_SOURCE_CANDIDATE_CONTRACT_DISCOVERY")
        self.assertEqual(result["runtime_state"], MOD.ENGINE.POST_F_RUNTIME_STATE)
        self.assertEqual(result["component_count"], 113)
        self.assertEqual(result["route_count"], 22)
        self.assertEqual(result["control_event_count"], 22)
        self.assertEqual(result["deterministic_check_count"], 137)
        self.assertEqual(result["formal_object_count"], 21)
        self.assertEqual(result["law_router"]["law_count"], 83)
        self.assertEqual(result["unknown_deterministic_operators"], [])

    def test_payload_cardinalities_and_post_cutover_tuple(self):
        p = MOD.build_payloads()
        self.assertEqual(p["compiled/AIR_P_COMPONENT_REGISTRY.json"]["component_count"], 113)
        self.assertEqual(p["compiled/AIR_P_ROUTE_CONTRACT_REGISTRY.json"]["route_count"], 22)
        self.assertEqual(p["compiled/AIR_P_CONTROL_EVENT_REGISTRY.json"]["event_count"], 22)
        self.assertEqual(p["compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json"]["object_count"], 21)
        summary = p["compiled/AIR_P_DETERMINISTIC_VALIDATION_REGISTRY.json"]["current_execution_summary"]
        self.assertEqual(summary["declared_check_count"], 137)
        self.assertEqual(summary["implemented_check_count"], 137)
        self.assertEqual(summary["executed_check_count"], 137)
        self.assertEqual(summary["pass_count"], 137)
        self.assertEqual(summary["fail_count"], 0)
        hc = p["compiled/AIR_P_HANDOFF_CHECKPOINT_DELTA_CONTRACT.json"]
        self.assertEqual(hc["runtime_state"], MOD.ENGINE.POST_F_RUNTIME_STATE)
        self.assertEqual(hc["transition_tuple"]["role"], "TARGET_CURRENT")
        self.assertEqual(hc["transition_tuple"]["template_revision"], 26)

    def test_overlay_rebase_is_non_authoritative_and_current(self):
        p = MOD.build_payloads()
        overlay = p["source/AIR_P_COMPONENT_METADATA_OVERLAY.json"]
        self.assertEqual(overlay["binding_target"]["sha256"], MOD.ENGINE.POST_F_CORE_SHA256)
        self.assertEqual(overlay["component_count"], 113)
        self.assertEqual(overlay["semantic_authority"], "NONE")
        self.assertEqual(overlay["positive_execution_authority"], "NONE")
        ids = {x["component_id"] for x in overlay["components"]}
        self.assertIn("CORE.LAW.NEW_TASK_EXECUTION_BINDING_BARRIER", ids)
        self.assertEqual(overlay["regeneration_provenance"]["current_core_sha256"], MOD.ENGINE.POST_F_CORE_SHA256)

    def test_package_schema_and_formal_machine_registry(self):
        p = MOD.build_payloads()
        schema = p["schema/AIR_P_PACKAGE_SCHEMA.json"]
        bundle = p["compiled/AIR_P_RUNTIME_BUNDLE.json"]
        self.assertTrue(MOD.ENGINE.runtime_bundle_schema_validate(bundle, schema))
        formal = p["compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json"]
        self.assertEqual(formal["source_registry_version"], "2.9.0")
        self.assertTrue(formal["closed_world"])
        self.assertEqual(formal["object_count"], 21)

    def test_negative_mutation_suite(self):
        paths = MOD.default_source_paths()
        p = MOD.build_payloads(paths)
        result = MOD.mutation_suite(p, paths)
        self.assertEqual(result["suite_state"], "PASS")
        self.assertTrue(all(x["state"] == "PASS" for x in result["tests"]))

    def test_all_137_deterministic_checks_have_mutation_coverage(self):
        result = MOD.deterministic_check_mutation_coverage()
        self.assertEqual(result["overall_state"], "PASS")
        self.assertEqual(result["declared_check_count"], 137)
        self.assertEqual(result["covered_check_count"], 137)
        self.assertEqual(result["rejected_mutation_count"], 137)
        self.assertEqual(result["uncovered_or_unrejected_count"], 0)

    def test_three_in_memory_payload_runs_identical(self):
        args = MOD.default_source_paths()
        maps = [MOD.payload_hash_map(MOD.build_payloads(args)) for _ in range(3)]
        self.assertEqual(maps[0], maps[1])
        self.assertEqual(maps[1], maps[2])

    def test_exact_source_pins_are_post_cutover(self):
        result = MOD.validate_source_inputs()
        observed = {x["role"]: x["actual"] for x in result["source_pin_validation"]}
        expected = dict(MOD.ENGINE.PINNED_HASHES)
        expected["CORE_RUNTIME"] = MOD.ENGINE.POST_F_CORE_SHA256
        self.assertEqual(observed, expected)

    def test_isolated_compile_does_not_mutate_source_root(self):
        paths = MOD.default_source_paths()
        before = {role: MOD.ENGINE.file_sha256(path) for role, path in paths.items()}
        with tempfile.TemporaryDirectory() as td:
            test_source = str(Path(__file__).resolve())
            MOD.ENGINE.compile_package(td, paths, test_source=test_source)
            manifest = json.loads((Path(td) / "GENERATED_FILE_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertGreater(manifest["file_count_excluding_self"], 0)
        after = {role: MOD.ENGINE.file_sha256(path) for role, path in paths.items()}
        self.assertEqual(before, after)


    def test_runtime_navigation_outputs_are_direct_nonauthoritative_and_complete(self):
        paths = MOD.default_source_paths()
        p = MOD.build_payloads(paths)
        kernel = p["compiled/AIR_P_TURN_GOVERNANCE_KERNEL.json"]
        index = p["compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json"]
        self.assertTrue(MOD.ENGINE.validate_runtime_navigation_outputs(kernel, index, paths))
        self.assertEqual(index["SYSTEM_DESIGNATION"], "AIR_P_RUNTIME_REFERENCE_INDEX_V1")
        self.assertEqual(index["authority_class"], "DERIVED_NONAUTHORITATIVE_NAVIGATION_TO_CANONICAL_SOURCE")
        self.assertEqual(index["direct_reference_depth"], 1)
        self.assertEqual(index["anchor_count"], 17)
        self.assertEqual(kernel["SYSTEM_DESIGNATION"], "AIR_P_TURN_GOVERNANCE_KERNEL_V1")
        self.assertEqual(kernel["authority_class"], "DERIVED_NONAUTHORITATIVE_EXECUTION_NAVIGATION_PROJECTION")
        self.assertEqual(kernel["required_contract_count"], 11)
        self.assertEqual(kernel["runtime_state"], MOD.ENGINE.POST_F_RUNTIME_STATE)
        self.assertEqual(kernel["starter_transition_contract_id"], "AIR_STARTER_CORE_RUNTIME_TRANSITION_IDENTITY_V10")
        self.assertEqual(kernel["starter_transition_state"], MOD.ENGINE.POST_F_RUNTIME_STATE)
        self.assertEqual(kernel["ordinary_prose_before_formal_closure"], "PROHIBITED_WHEN_GOVERNED_ROUTE_OR_OWED_FORMAL_OBJECT_EXISTS")

    def test_runtime_navigation_dependencies_are_direct_and_source_pinned(self):
        paths = MOD.default_source_paths()
        p = MOD.build_payloads(paths)
        index = p["compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json"]
        ids = {a["semantic_id"] for a in index["anchors"]}
        required_fields = {"semantic_id", "canonical_source_path", "patch_marker", "source_sha256", "section_digest", "retrieval_trigger", "required_dependencies"}
        self.assertEqual(len(ids), 17)
        self.assertIn("AIR_CONTROL_UNRESOLVED_OPTION_SEMANTIC_QUALIFIER_V1", ids)
        self.assertIn("AIR_CONTROL_TURN_KERNEL_PROGRESSIVE_RUNTIME_RENDERER_V1", ids)
        self.assertIn("AIR_STARTER_CORE_RUNTIME_TRANSITION_IDENTITY_V10", ids)
        for anchor in index["anchors"]:
            self.assertTrue(required_fields.issubset(anchor))
            self.assertTrue(set(anchor["required_dependencies"]).issubset(ids))
            self.assertEqual(anchor["source_sha256"], index["source_hashes"][anchor["canonical_source_path"]])

    def test_runtime_navigation_negative_mutations_fail_closed(self):
        paths = MOD.default_source_paths()
        p = MOD.build_payloads(paths)
        kernel = json.loads(json.dumps(p["compiled/AIR_P_TURN_GOVERNANCE_KERNEL.json"]))
        index = json.loads(json.dumps(p["compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json"]))
        stale = json.loads(json.dumps(index))
        stale["anchors"][0]["source_sha256"] = "0" * 64
        with self.assertRaises(MOD.ENGINE.CompileError):
            MOD.ENGINE.validate_runtime_navigation_outputs(kernel, stale, paths)
        missing = json.loads(json.dumps(kernel))
        missing["required_contract_semantic_ids"] = missing["required_contract_semantic_ids"][:-1]
        with self.assertRaises(MOD.ENGINE.CompileError):
            MOD.ENGINE.validate_runtime_navigation_outputs(missing, index, paths)

    def test_amrs4f_transition_contract_is_v10_eleven_state_exact_current_tuple(self):
        paths = MOD.default_source_paths()
        starter = MOD.ENGINE.strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
        contract = starter["validation_contract"]["core_runtime_transition_identity_contract"]
        states = contract["current_cutover_states"]
        self.assertEqual(contract["contract_id"], "AIR_STARTER_CORE_RUNTIME_TRANSITION_IDENTITY_V10")
        self.assertEqual(len(states), 11)
        prior_ids = {
            "R23_DECISION_TRACE_PRE_CUTOVER",
            "R23_DECISION_TRACE_MIXED_CORE25_HANDOFF24",
            "R23_DECISION_TRACE_POST_CUTOVER",
            "R23_USER_BOOT_PROFILE_DISPATCH_POST_CUTOVER",
        }
        self.assertTrue(prior_ids.issubset({x["state_id"] for x in states}))
        pre_f = [x for x in states if x["state_id"] == MOD.ENGINE.PRE_F_RUNTIME_STATE]
        self.assertEqual(len(pre_f), 1)
        self.assertEqual(pre_f[0]["core_sha256"], MOD.ENGINE.PRE_F_CORE_SHA256)
        self.assertEqual(pre_f[0]["handoff_template_revision"], 26)
        post_f = [x for x in states if x["state_id"] == MOD.ENGINE.POST_F_RUNTIME_STATE]
        self.assertEqual(len(post_f), 1)
        current = post_f[0]
        self.assertEqual(current["core_sha256"], MOD.ENGINE.POST_F_CORE_SHA256)
        self.assertEqual(current["handoff_template_revision"], 26)
        self.assertEqual(current["handoff_template_sha256"], MOD.ENGINE.PINNED_HASHES["HANDOFF_CARD_TEMPLATE"])
        self.assertEqual(current["required_core_patch_marker"], MOD.ENGINE.AMRS4F_CUTOVER_MARKER)
        self.assertEqual(MOD.ENGINE._runtime_transition_state(starter, paths), MOD.ENGINE.POST_F_RUNTIME_STATE)

    def test_d001_unresolved_option_semantic_qualifier_contract_present(self):
        control = MOD.ENGINE.read_text(MOD.default_source_paths()["CONTROL_SURFACE"])
        self.assertIn("Patch marker: AIR_CONTROL_UNRESOLVED_OPTION_SEMANTIC_QUALIFIER_V1", control)
        self.assertIn("must not add project-specific relevance or selection", control)
        self.assertIn("do not describe it as any of the following unless current canonical state explicitly establishes that status", control)
        self.assertIn("Q4=C is the relevant continuity/delivery mode", control)
        self.assertIn("not evidence that the option is relevant, selected, or preferred", control)

    def test_d002_turn_kernel_formal_object_emission_closure_contract_present(self):
        paths = MOD.default_source_paths()
        core = MOD.ENGINE.read_text(paths["CORE_RUNTIME"])
        control = MOD.ENGINE.read_text(paths["CONTROL_SURFACE"])
        self.assertIn("Patch marker: AIR_TURN_GOVERNANCE_KERNEL_CONTRACT_V1", core)
        for step in [
            "CURRENT_ALIGNMENT_EVALUATION",
            "ROUTE_RESOLUTION",
            "REQUIRED_VISIBLE_OBJECT_SET",
            "CONSTRUCT_OWED_OBJECTS",
            "FORMAL_OBJECT_COMPLETENESS_VALIDATION",
            "RESPONSE_EMISSION_CLOSURE",
            "VISIBLE_OBJECT_EMISSION",
            "ORDINARY_PROSE",
        ]:
            self.assertIn(step, core)
        self.assertIn("BOOTSTRAP_NO_ARTIFACT is not a prose-only mode", core)
        self.assertIn("Material unresolved-input routing must therefore surface AIR_REQUIRED_INPUT_REQUEST", core)
        self.assertIn("AIR_DECISION_TRACE may be emitted only after its canonical constructor and current evaluation_basis pass", core)
        self.assertIn("Patch marker: AIR_CONTROL_TURN_KERNEL_PROGRESSIVE_RUNTIME_RENDERER_V1", control)
        self.assertIn("pre-artifact route owes a non-root formal object that requires `evaluation_basis`", control)
        self.assertIn("pre-artifact state creates no visibility exception", control)

    def test_consumption_key_contract_core_starter_exact_mirror(self):
        paths = MOD.default_source_paths()
        core = MOD.ENGINE.read_text(paths["CORE_RUNTIME"])
        starter = MOD.ENGINE.strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
        self.assertTrue(MOD.ENGINE.validate_consumption_key_contract_mirror(core, starter))

    def test_consumption_key_constructor_deterministic_and_mutation_sensitive(self):
        contract = MOD.ENGINE.core_consumption_key_contract(MOD.ENGINE.read_text(MOD.default_source_paths()["CORE_RUNTIME"]))
        a = {k: "x" for k in contract["preimage"]["authorization_projection_fields"]}
        a["single_use"] = True
        k1 = MOD.ENGINE.action_authorization_consumption_key(a, contract)
        k2 = MOD.ENGINE.action_authorization_consumption_key(a, contract)
        self.assertEqual(k1, k2)
        b = dict(a); b["target"] = "y"
        self.assertNotEqual(k1, MOD.ENGINE.action_authorization_consumption_key(b, contract))

    def test_consumption_key_constructor_excludes_lifecycle_and_provenance_fields(self):
        contract = MOD.ENGINE.core_consumption_key_contract(MOD.ENGINE.read_text(MOD.default_source_paths()["CORE_RUNTIME"]))
        a = {k: "x" for k in contract["preimage"]["authorization_projection_fields"]}
        a["single_use"] = True
        k1 = MOD.ENGINE.action_authorization_consumption_key(a, contract)
        a.update({"consumption_state":"CONSUMED","evaluation_basis":{"x":1},"runtime_origin":"PROMPT_COMPILED"})
        self.assertEqual(k1, MOD.ENGINE.action_authorization_consumption_key(a, contract))

    def test_consumption_key_constructor_fails_closed_on_missing_or_bad_stored_key(self):
        contract = MOD.ENGINE.core_consumption_key_contract(MOD.ENGINE.read_text(MOD.default_source_paths()["CORE_RUNTIME"]))
        a = {k: "x" for k in contract["preimage"]["authorization_projection_fields"]}
        a["single_use"] = True
        a.pop("target")
        with self.assertRaises(MOD.ENGINE.CompileError):
            MOD.ENGINE.action_authorization_consumption_key(a, contract)
        a["target"] = "x"; a["consumption_key_sha256"] = "bad"
        with self.assertRaises(MOD.ENGINE.CompileError):
            MOD.ENGINE.validate_stored_action_authorization_consumption_key(a, contract)

    def test_boot_profile_dispatch_contract_present_and_closed(self):
        paths = MOD.default_source_paths()
        core = MOD.ENGINE.read_text(paths["CORE_RUNTIME"])
        starter = MOD.ENGINE.strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
        self.assertIn("Patch marker: AIR_USER_BOOT_PROFILE_DISPATCH_V1", core)
        p = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        self.assertEqual(p["default_user_boot_profile"], "TIER_0_ROUTINE")
        self.assertEqual(p["silent_escalation"], "PROHIBITED")
        self.assertEqual(set(p["user_boot_profile_dispatch"]), {"TIER_0_ROUTINE","TIER_1_NAVIGATION","TIER_2_TARGETED_SOURCE","TIER_3_DEEP_AUDIT"})

    def test_tier0_negative_contract_blocks_broad_boot_work(self):
        starter = MOD.ENGINE.strict_json_load(MOD.default_source_paths()["DEFAULT_STARTER_PROFILE"])
        t0 = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]["user_boot_profile_dispatch"]["TIER_0_ROUTINE"]
        joined = " ".join(t0["negative_requirements"])
        self.assertIn("every release-file hash/size", joined)
        self.assertIn("compiled registry cardinalities", joined)
        self.assertIn("Router83", joined)

    def test_runtime_kernel_projects_user_boot_profile_dispatch(self):
        p = MOD.build_payloads(MOD.default_source_paths())
        pr = p["compiled/AIR_P_TURN_GOVERNANCE_KERNEL.json"]["progressive_runtime"]
        self.assertEqual(pr["required_user_boot_profile_patch_marker"], "AIR_USER_BOOT_PROFILE_DISPATCH_V1")
        self.assertEqual(pr["default_user_boot_profile"], "TIER_0_ROUTINE")
        self.assertEqual(pr["silent_escalation"], "PROHIBITED")
        self.assertEqual(len(pr["user_boot_profile_dispatch"]), 4)
        starter = MOD.ENGINE.strict_json_load(MOD.default_source_paths()["DEFAULT_STARTER_PROFILE"])
        expected = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        self.assertEqual(pr["required_retrieval_scope_enforcement_patch_marker"], "AIR_RETRIEVAL_SCOPE_ENFORCEMENT_V1")
        self.assertEqual(pr["retrieval_scope_enforcement"], expected["retrieval_scope_enforcement"])

    def test_tier1_navigation_closed_model_context_contract(self):
        paths = MOD.default_source_paths()
        core = MOD.ENGINE.read_text(paths["CORE_RUNTIME"])
        starter = MOD.ENGINE.strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
        pr = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        rse = pr["retrieval_scope_enforcement"]
        self.assertIn("Patch marker: AIR_RETRIEVAL_SCOPE_ENFORCEMENT_V1", core)
        self.assertEqual(rse["model_visible_scope_policy"], "CLOSED_WORLD_ALLOWLIST")
        self.assertTrue(rse["tool_only_checks_do_not_grant_model_visibility"])
        t1 = rse["tier1_navigation"]
        self.assertEqual(t1["handoff_body_or_fragment_without_dependency"], "PROHIBITED")
        self.assertEqual(t1["handoff_exact_field_tool_extraction_when_required"], "ALLOWED_TOOL_ONLY")
        self.assertEqual(t1["router83_law_applicability_metadata_before_typed_routing"], "PROHIBITED_MODEL_VISIBILITY")
        negatives = " ".join(pr["user_boot_profile_dispatch"]["TIER_1_NAVIGATION"]["negative_requirements"])
        self.assertIn("Handoff body or body fragments", negatives)
        self.assertIn("law_applicability_metadata", negatives)
        kernel = MOD.build_payloads(paths)["compiled/AIR_P_TURN_GOVERNANCE_KERNEL.json"]
        self.assertEqual(kernel["progressive_runtime"]["retrieval_scope_enforcement"], rse)

    def test_tier2_targeted_source_exact_anchor_closure_contract(self):
        paths = MOD.default_source_paths()
        starter = MOD.ENGINE.strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
        pr = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        t2 = pr["retrieval_scope_enforcement"]["tier2_targeted_source"]
        self.assertEqual(t2["target_resolution"], "EXPLICIT_TARGET_TO_DIRECT_RUNTIME_INDEX_ANCHOR_TO_DECLARED_DEPENDENCY_CLOSURE")
        self.assertTrue(t2["exact_section_or_json_subtree_only"])
        self.assertEqual(t2["ordinary_whole_archive_filename_size_enumeration"], "PROHIBITED")
        self.assertEqual(t2["broad_recursive_source_scan_when_direct_anchor_exists"], "PROHIBITED")
        self.assertEqual(t2["adjacent_context_outside_exact_section_boundaries"], "PROHIBITED")
        self.assertIn("SMALLEST_MISSING_TARGET_OR_INPUT", t2["unresolved_target_behavior"])
        negatives = " ".join(pr["user_boot_profile_dispatch"]["TIER_2_TARGETED_SOURCE"]["negative_requirements"])
        self.assertIn("whole-archive filename/size enumeration", negatives)
        self.assertIn("broad recursive source scans", negatives)
        self.assertIn("adjacent context", negatives)

    def test_boot_profile_patch_preserves_architecture_cardinalities(self):
        self.assertEqual(MOD.ENGINE.EXPECTED, {"components":113,"routes":22,"control_events":22,"deterministic_checks":137,"formal_objects":21,"laws":83})


DECISION_TRACE_LAW_ID = "CORE.LAW.DECISION_TRACE_JUSTIFICATION_AND_CLOSURE"
KNOWN_BROKEN_ENTRYPOINT_SHA256 = "e81ca4660c89f259bebd9ad236ec75358ab685c06f5811e9b43c2b79b268060e"
EXPECTED_DECISION_TRACE_REGISTRY_FINGERPRINT = "915f3f3f03b23106de450b5f5a6480d2122114a21d58c7da32ab769df0cf4686"


def _decision_trace_formal_spec(payloads):
    formal = payloads["compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json"]
    return next(x for x in formal["objects"] if x["object_id"] == "AIR_DECISION_TRACE")


def _decision_trace_contracts():
    paths = MOD.default_source_paths()
    core_text = MOD.ENGINE.read_text(paths["CORE_RUNTIME"])
    return MOD.ENGINE._with_transition_context(paths, MOD.ENGINE.core_decision_trace_contracts, core_text)


def _trace_fingerprint(trace, contract):
    preimage = {k: trace[k] for k in contract["included_fields"]}
    return MOD.ENGINE.canonical_json_sha256(preimage)


def _valid_trace_fixture(payloads):
    law_fp = payloads["source/AIR_LAW_APPLICABILITY_ROUTER.json"]["source_of_truth"]["law_registry_entry_fingerprint_sha256"]
    trace = {
        "object_version": "2.0.0",
        "record_class": "DECISION_JUSTIFICATION_RECORD",
        "runtime_origin": "PROMPT_COMPILED",
        "backend_validation_claimed": False,
        "hidden_reasoning_claimed": False,
        "evidence_class": "SOURCE_SUPPORTED_GOVERNANCE_RECORD",
        "evaluation_basis": {"evaluation_id": "EVAL-DT-FIXTURE", "dependency_state": "SATISFIED"},
        "trace_id": "AIR-DT-FIXTURE-001",
        "trace_contract_ref": "AIR_DECISION_BASIS_CLOSURE_V1",
        "trace_contract_version": "1.0.0",
        "controlling_artifact_ref": "AIR-ART-FIXTURE@R1",
        "task_identity_ref": "TASK-FIXTURE",
        "decision_subject_ref": "SUBJECT-FIXTURE",
        "decision_class": "MATERIAL_MODEL_EVALUATION",
        "trace_requirement_basis": "MATERIAL_MODEL_JUDGMENT_REQUIRED",
        "decision_statement": "Choose the admissible fixture outcome.",
        "decision_outcome": {"operative_code": "ALLOW", "label": "Allowed"},
        "decision_basis_summary": "Evidence E1 and rule CORE.LAW.DECISION_TRACE_JUSTIFICATION_AND_CLOSURE support the surfaced outcome.",
        "material_claim_refs": [{"claim_id": "C1", "evidence_ref_ids": ["E1"]}],
        "evidence_refs": [{"ref_id": "E1", "sha256": "1" * 64, "state": "CURRENT"}],
        "rule_refs": [DECISION_TRACE_LAW_ID],
        "law_resolution_fingerprint": law_fp,
        "authority_state_refs": [{"ref_id": "AUTH1", "state": "NONE"}],
        "uncertainty_state": "NONE_MATERIAL",
        "uncertainty_refs": [],
        "provenance_closure_state": "PASS",
        "rule_closure_state": "PASS",
        "authority_closure_state": "PASS",
        "claim_source_consistency_state": "PASS",
        "forced_walk_state": {"comparison_outcome": "EXACT_MATCH", "verification_mode": "DETERMINISTIC_RECONSTRUCTION"},
        "decision_trace_fingerprint": "",
        "trace_state": "CURRENT_VERIFIED",
        "positive_execution_authority": "NONE",
    }
    fp = _decision_trace_contracts()["AIR_DECISION_TRACE_FINGERPRINT_V1"]
    trace["decision_trace_fingerprint"] = _trace_fingerprint(trace, fp)
    return trace


def _validate_trace_fixture(trace, spec, contracts, payloads):
    violations = []
    allowed = set(spec["allowed_top_level_fields"])
    required = set(spec["required_top_level_fields"])
    fields = set(trace)
    if required - fields:
        violations.append("MISSING_REQUIRED_FIELD")
    if fields - allowed:
        violations.append("UNKNOWN_FIELD")
    if any(x in fields for x in spec.get("forbidden_top_level_fields", [])):
        violations.append("FORBIDDEN_HIDDEN_REASONING_FIELD")
    for key, value in spec.get("fixed_constraints", {}).items():
        if trace.get(key) != value:
            violations.append("FIXED_CONSTRAINT")
    for key, values in spec.get("enum_constraints", {}).items():
        if key in trace and trace[key] not in values:
            violations.append("ENUM_CONSTRAINT")

    evidence_by_id = {}
    for ref in trace.get("evidence_refs", []):
        if not isinstance(ref, dict) or not ref.get("ref_id") or not re.fullmatch(r"[0-9a-f]{64}", str(ref.get("sha256", ""))):
            violations.append("EVIDENCE_REF_INVALID")
            continue
        rid = ref["ref_id"]
        if rid in evidence_by_id and evidence_by_id[rid] != ref["sha256"]:
            violations.append("CLAIM_SOURCE_CONTRADICTION")
        evidence_by_id[rid] = ref["sha256"]
    for claim in trace.get("material_claim_refs", []):
        for rid in claim.get("evidence_ref_ids", []):
            if rid not in evidence_by_id:
                violations.append("MISSING_EVIDENCE")
    law_ids = {x["law_id"] for x in payloads["source/AIR_LAW_APPLICABILITY_ROUTER.json"]["law_applicability_metadata"]}
    if any(rule not in law_ids for rule in trace.get("rule_refs", [])):
        violations.append("FORGED_OR_UNKNOWN_RULE")
    current_law_fp = payloads["source/AIR_LAW_APPLICABILITY_ROUTER.json"]["source_of_truth"]["law_registry_entry_fingerprint_sha256"]
    if trace.get("law_resolution_fingerprint") != current_law_fp:
        violations.append("LAW_FINGERPRINT_STALE")
    if trace.get("uncertainty_state") == "UNRESOLVED_MATERIAL":
        violations.append("UNRESOLVED_UNCERTAINTY")
    if trace.get("positive_execution_authority") != "NONE":
        violations.append("ILLEGAL_AUTHORITY_GAIN")
    if any(trace.get(k) != "PASS" for k in ["provenance_closure_state", "rule_closure_state", "authority_closure_state", "claim_source_consistency_state"]):
        violations.append("CLOSURE_NOT_PASS")
    outcome = trace.get("forced_walk_state", {}).get("comparison_outcome")
    if outcome not in {"EXACT_MATCH", "EQUIVALENT"}:
        violations.append("FORCED_WALK_NOT_PASS")
    if trace.get("trace_state") != "CURRENT_VERIFIED":
        violations.append("TRACE_NOT_CURRENT")
    fp_contract = contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"]
    if all(k in trace for k in fp_contract["included_fields"]):
        if trace.get("decision_trace_fingerprint") != _trace_fingerprint(trace, fp_contract):
            violations.append("TRACE_FINGERPRINT_MISMATCH")
    return violations


def _forced_walk_compare(reconstructed, original):
    if reconstructed is None:
        return "UNRESOLVED"
    if reconstructed == original:
        return "EXACT_MATCH"
    if isinstance(reconstructed, dict) and isinstance(original, dict) and reconstructed.get("operative_code") == original.get("operative_code"):
        return "EQUIVALENT"
    return "DIVERGENT"


def _basis_diff(expected_claim_ids, reconstructed_claim_ids, contradictions=None):
    contradictions = contradictions or []
    return {
        "omissions": sorted(set(expected_claim_ids) - set(reconstructed_claim_ids)),
        "inventions": sorted(set(reconstructed_claim_ids) - set(expected_claim_ids)),
        "contradictions": sorted(contradictions),
    }



    def test_amrs4e_law_source_family_exact_and_shadow_only(self):
        paths = MOD.default_source_paths()
        result = MOD.validate_source_inputs(paths)
        state = result["law_source_family"]
        self.assertEqual(state["law_count"], 83)
        self.assertEqual(state["physical_law_body_count"], 82)
        self.assertEqual(state["floor_count"], 28)
        self.assertEqual(state["source_family_file_count"], 114)
        payloads = MOD.build_payloads(paths)
        pin = payloads["compiled/AIR_LAW_SOURCE_PACKAGE_PIN.json"]
        self.assertEqual(pin["positive_execution_authority"], "NONE")
        self.assertIn("PENDING_AMRS4F", pin["activation_state"])

    def test_amrs4e_law_package_manifest_exact_inventory_and_hashes(self):
        paths = MOD.default_source_paths()
        p = MOD.build_payloads(paths)
        manifest = p["law_package/AIR_LAW_SOURCE_PACKAGE_MANIFEST.json"]
        self.assertEqual(len(manifest["files"]), 114)
        self.assertEqual(len([x for x in manifest["files"] if x["role"] == "LAW_BODY"]), 82)
        self.assertEqual(len([x for x in manifest["files"] if x["role"] == "FLOOR_BODY"]), 28)
        self.assertEqual(len([x for x in manifest["files"] if x["retrieval_class"].startswith("TIER1")]), 3)
        self.assertEqual(MOD.ENGINE.canonical_json_sha256(manifest["files"]), manifest["content_fingerprint_sha256"])
        pin = p["compiled/AIR_LAW_SOURCE_PACKAGE_PIN.json"]
        raw = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\\n").encode("utf-8")
        self.assertEqual(hashlib.sha256(raw).hexdigest(), pin["manifest_sha256"])

    def test_amrs4e_runtime_bundle_exposes_package_pin_without_activation(self):
        p = MOD.build_payloads()
        bundle = p["compiled/AIR_P_RUNTIME_BUNDLE.json"]
        self.assertEqual(bundle["law_source_package_pin_ref"], "AIR_LAW_SOURCE_PACKAGE_PIN.json")
        self.assertTrue(MOD.ENGINE.runtime_bundle_schema_validate(bundle, p["schema/AIR_P_PACKAGE_SCHEMA.json"]))
        self.assertEqual(p["compiled/AIR_LAW_SOURCE_PACKAGE_PIN.json"]["positive_execution_authority"], "NONE")

    def test_amrs4e_formal_json_conformance_is_source_enforced(self):
        core = MOD.ENGINE.read_text(MOD.default_source_paths()["CORE_RUNTIME"])
        self.assertIn("AIR_FORMAL_JSON_CONFORMANCE_V1", core)
        p = MOD.build_payloads()
        formal = p["compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json"]
        self.assertTrue(formal["closed_world"])
        for obj in formal["objects"]:
            self.assertIn("record_class", obj)
        roundtrip = json.loads(json.dumps(formal, ensure_ascii=False, sort_keys=True))
        self.assertEqual(roundtrip, formal)


class AirPDecisionTraceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = MOD.default_source_paths()
        cls.payloads = MOD.build_payloads(cls.paths)
        cls.spec = _decision_trace_formal_spec(cls.payloads)
        cls.contracts = _decision_trace_contracts()

    def test_dt_t01_formal_object_schema_positive(self):
        trace = _valid_trace_fixture(self.payloads)
        self.assertEqual(_validate_trace_fixture(trace, self.spec, self.contracts, self.payloads), [])

    def test_dt_t02_formal_object_schema_negative_missing_field(self):
        trace = _valid_trace_fixture(self.payloads)
        trace.pop("trace_id")
        self.assertIn("MISSING_REQUIRED_FIELD", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t03_hidden_reasoning_fields_rejected(self):
        for field in ["chain_of_thought", "reasoning_steps", "internal_thoughts", "latent_state", "hidden_reasoning", "private_scratchpad"]:
            trace = _valid_trace_fixture(self.payloads)
            trace[field] = "forbidden"
            v = _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads)
            self.assertTrue("UNKNOWN_FIELD" in v or "FORBIDDEN_HIDDEN_REASONING_FIELD" in v)

    def test_dt_t04_evidence_ref_closure(self):
        trace = _valid_trace_fixture(self.payloads)
        self.assertNotIn("MISSING_EVIDENCE", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t05_missing_evidence_blocks_pass(self):
        trace = _valid_trace_fixture(self.payloads)
        trace["evidence_refs"] = []
        trace["decision_trace_fingerprint"] = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertIn("MISSING_EVIDENCE", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t06_forged_evidence_ref_fails_closed(self):
        trace = _valid_trace_fixture(self.payloads)
        trace["evidence_refs"][0]["sha256"] = "NOT_A_SHA256"
        trace["decision_trace_fingerprint"] = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertIn("EVIDENCE_REF_INVALID", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t07_rule_ref_closure(self):
        trace = _valid_trace_fixture(self.payloads)
        self.assertNotIn("FORGED_OR_UNKNOWN_RULE", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t08_forged_rule_ref_fails_closed(self):
        trace = _valid_trace_fixture(self.payloads)
        trace["rule_refs"] = ["CORE.LAW.NONEXISTENT"]
        trace["decision_trace_fingerprint"] = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertIn("FORGED_OR_UNKNOWN_RULE", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t09_law_fingerprint_change_stales_trace(self):
        trace = _valid_trace_fixture(self.payloads)
        trace["law_resolution_fingerprint"] = "0" * 64
        trace["decision_trace_fingerprint"] = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertIn("LAW_FINGERPRINT_STALE", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t10_claim_source_contradiction_fails_closed(self):
        trace = _valid_trace_fixture(self.payloads)
        trace["evidence_refs"].append({"ref_id": "E1", "sha256": "2" * 64, "state": "CURRENT"})
        trace["decision_trace_fingerprint"] = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertIn("CLAIM_SOURCE_CONTRADICTION", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t11_unresolved_uncertainty_cannot_pass(self):
        trace = _valid_trace_fixture(self.payloads)
        trace["uncertainty_state"] = "UNRESOLVED_MATERIAL"
        trace["decision_trace_fingerprint"] = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertIn("UNRESOLVED_UNCERTAINTY", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t12_trace_cannot_gain_authority(self):
        trace = _valid_trace_fixture(self.payloads)
        trace["positive_execution_authority"] = "GRANTED"
        self.assertIn("ILLEGAL_AUTHORITY_GAIN", _validate_trace_fixture(trace, self.spec, self.contracts, self.payloads))

    def test_dt_t13_forced_walk_exact_match(self):
        original = {"operative_code": "ALLOW", "label": "Allowed"}
        self.assertEqual(_forced_walk_compare(original, original), "EXACT_MATCH")

    def test_dt_t14_forced_walk_equivalent(self):
        self.assertEqual(_forced_walk_compare({"operative_code": "ALLOW", "label": "Proceed"}, {"operative_code": "ALLOW", "label": "Allowed"}), "EQUIVALENT")

    def test_dt_t15_forced_walk_divergent_routes_review(self):
        self.assertEqual(_forced_walk_compare({"operative_code": "REJECT"}, {"operative_code": "ALLOW"}), "DIVERGENT")

    def test_dt_t16_forced_walk_unresolved_routes_review(self):
        self.assertEqual(_forced_walk_compare(None, {"operative_code": "ALLOW"}), "UNRESOLVED")

    def test_dt_t17_original_outcome_withheld_until_comparison(self):
        forced = self.contracts["AIR_DECISION_TRACE_FORCED_WALK_V1"]
        phase2 = next(x for x in forced["phases"] if x["id"] == "FW2_BASIS_ONLY_RECONSTRUCTION")
        phase3 = next(x for x in forced["phases"] if x["id"] == "FW3_COMPARISON")
        self.assertIn("withhold original decision_outcome from verifier input", phase2["requirements"])
        self.assertIn("reveal original decision_outcome only after reconstruction", phase3["requirements"])

    def test_dt_t18_source_hash_change_stales_trace(self):
        trace = _valid_trace_fixture(self.payloads)
        before = trace["decision_trace_fingerprint"]
        trace["evidence_refs"][0]["sha256"] = "2" * 64
        after = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertNotEqual(before, after)

    def test_dt_t19_artifact_revision_change_stales_trace(self):
        trace = _valid_trace_fixture(self.payloads)
        before = trace["decision_trace_fingerprint"]
        trace["controlling_artifact_ref"] = "AIR-ART-FIXTURE@R2"
        after = _trace_fingerprint(trace, self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"])
        self.assertNotEqual(before, after)

    def test_dt_t20_omission_invention_contradiction_detection(self):
        diff = _basis_diff(["C1", "C2"], ["C2", "C3"], ["C4"])
        self.assertEqual(diff, {"omissions": ["C1"], "inventions": ["C3"], "contradictions": ["C4"]})

    def test_dt_t21_source_intent_invariant_coverage_required(self):
        closure = self.contracts["AIR_DECISION_BASIS_CLOSURE_V1"]
        self.assertIn("SOURCE_INTENT_INVARIANT_COVERAGE_WHEN_MATERIAL", closure["closure_checks"])

    def test_dt_t22_deterministic_checks_do_not_require_trace(self):
        closure = self.contracts["AIR_DECISION_BASIS_CLOSURE_V1"]
        text = closure["trace_requirement"]["NOT_REQUIRED_WHEN"]
        self.assertIn("exact deterministic checks", text)
        self.assertIn("hash equality", text)

    def test_dt_t23_ambiguous_requirement_routes_review(self):
        closure = self.contracts["AIR_DECISION_BASIS_CLOSURE_V1"]
        self.assertIn("BLOCK_OPERATIVE_DECISION_AND_ROUTE_REVIEW", closure["trace_requirement"]["UNRESOLVED_BEHAVIOR"])

    def test_dt_t24_handoff_rev25_to_rev26_migration_no_inference_or_authority(self):
        handoff = MOD.ENGINE.strict_json_load(self.paths["HANDOFF_CARD_TEMPLATE"])["AIR_HANDOFF_CARD"]
        rule = handoff["schema_manifest"]["revision_migration_contracts"]["REV25_TO_REV26"]
        self.assertEqual(handoff["template_revision"], 26)
        self.assertEqual(handoff["working_agreement"]["preferred_max_execution_granularity"], None)
        self.assertEqual(handoff["source_state"]["law_source_transfer_state"]["positive_execution_authority"], "NONE")
        self.assertIn("GENERIC PROCEED", rule["q6_migration_rule"])

    def test_dt_t25_handoff_current_trace_restores_stale_pending_revalidation(self):
        handoff = MOD.ENGINE.strict_json_load(self.paths["HANDOFF_CARD_TEMPLATE"])["AIR_HANDOFF_CARD"]
        self.assertIn("STALE_PENDING_CURRENT_SESSION_REVALIDATION", handoff["decision_trace_state"]["restoration_rule"])

    def test_dt_t26_handoff_next_step_trace_closure(self):
        handoff = MOD.ENGINE.strict_json_load(self.paths["HANDOFF_CARD_TEMPLATE"])["AIR_HANDOFF_CARD"]
        cond = next(x for x in handoff["schema_manifest"]["conditional_rules"] if x["id"] == "HC-COND-DECISION-TRACE-REV25")
        self.assertTrue(any("exact projection/fingerprint or a blocking required-input identity" in x for x in cond["requirements"]))

    def test_dt_t27_all_objects_visibility_requires_full_trace(self):
        control = MOD.ENGINE.read_text(self.paths["CONTROL_SURFACE"])
        self.assertIn("AIR DECISION TRACE PRESENTATION SURFACE LAW", control)
        self.assertIn("`ALL_OBJECTS` requires every generated `AIR_DECISION_TRACE` to be printed in full.", control)

    def test_dt_t28_presentation_invariance(self):
        control = MOD.ENGINE.read_text(self.paths["CONTROL_SURFACE"])
        self.assertIn("`air -t on` and `air -t off` never alter whether the formal object is owed.", control)
        self.assertIn("Preserve the same canonical `AIR_DECISION_TRACE` and the same evidence/closure obligations.", control)

    def test_dt_t29_trace_fingerprint_reproducibility(self):
        trace = _valid_trace_fixture(self.payloads)
        contract = self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"]
        vals = [_trace_fingerprint(trace, contract) for _ in range(3)]
        self.assertEqual(vals[0], vals[1])
        self.assertEqual(vals[1], vals[2])

    def test_dt_t30_independent_verifier_agrees_on_fingerprint_fixture(self):
        trace = _valid_trace_fixture(self.payloads)
        contract = self.contracts["AIR_DECISION_TRACE_FINGERPRINT_V1"]
        preimage = {k: trace[k] for k in contract["included_fields"]}
        first = _trace_fingerprint(trace, contract)
        second = hashlib.sha256(json.dumps(preimage, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        self.assertEqual(first, second)

    def test_dt_t31_model_dependent_forced_walk_disclosure(self):
        forced = self.contracts["AIR_DECISION_TRACE_FORCED_WALK_V1"]
        self.assertIn("INDEPENDENT_MODEL_EVALUATION", forced["verification_modes"])
        self.assertIn("non-deterministic", forced["verification_modes"]["INDEPENDENT_MODEL_EVALUATION"])

    def test_dt_t32_law_router_regeneration_adds_global_law_once(self):
        router = self.payloads["source/AIR_LAW_APPLICABILITY_ROUTER.json"]
        laws = [x["law_id"] for x in router["law_applicability_metadata"]]
        self.assertEqual(len(router["law_applicability_metadata"]), 83)
        self.assertEqual(laws.count(DECISION_TRACE_LAW_ID), 1)
        self.assertEqual(router["source_of_truth"]["law_registry_entry_fingerprint_sha256"], EXPECTED_DECISION_TRACE_REGISTRY_FINGERPRINT)

    def test_dt_t33_formal_registry_count_and_exact_transition_profiles(self):
        formal = self.payloads["compiled/AIR_P_FORMAL_OBJECT_CONTRACT_REGISTRY.json"]
        starter = MOD.ENGINE.strict_json_load(self.paths["DEFAULT_STARTER_PROFILE"])
        states = starter["validation_contract"]["core_runtime_transition_identity_contract"]["current_cutover_states"]
        post = next(x for x in states if x["state_id"] == MOD.ENGINE.POST_F_RUNTIME_STATE)
        self.assertEqual(formal["object_count"], 21)
        self.assertEqual(post["formal_object_profile"]["object_count"], 21)
        self.assertIn("AIR_DECISION_TRACE", post["formal_object_profile"]["required_additive_object_ids"])
        self.assertEqual(MOD.ENGINE.EXPECTED["formal_objects"], 21)

    def test_dt_t34_cutover_tuple_negatives_fail_exact_membership(self):
        starter = MOD.ENGINE.strict_json_load(self.paths["DEFAULT_STARTER_PROFILE"])
        states = starter["validation_contract"]["core_runtime_transition_identity_contract"]["current_cutover_states"]
        exact = {(x["core_sha256"], x["handoff_template_revision"], x["handoff_template_sha256"]) for x in states}
        current = next(x for x in states if x["state_id"] == MOD.ENGINE.POST_F_RUNTIME_STATE)
        self.assertNotIn(("0" * 64, current["handoff_template_revision"], current["handoff_template_sha256"]), exact)
        self.assertNotIn((current["core_sha256"], 999, current["handoff_template_sha256"]), exact)
        self.assertNotIn((current["core_sha256"], current["handoff_template_revision"], "0" * 64), exact)

    def test_dt_t35_compiler_bootstrap_boundary_remains_separate(self):
        entrypoint = HERE / "compiler" / "compile_air_p.py"
        observed = MOD.ENGINE.file_sha256(entrypoint)
        self.assertNotEqual(observed, KNOWN_BROKEN_ENTRYPOINT_SHA256, "Known compile_air_p.py bootstrap defect must be repaired under its separate scope before this suite may claim executable PASS")

    def test_dt_t36_law_router_source_of_truth_refreshes_from_current_core(self):
        core_text = MOD.ENGINE.read_text(self.paths["CORE_RUNTIME"])
        prior_router = MOD.ENGINE.strict_json_load(self.paths["LAW_APPLICABILITY_ROUTER"])
        router = MOD.ENGINE._with_transition_context(self.paths, MOD.ENGINE.regenerate_law_router, core_text, prior_router)
        registry = MOD.ENGINE.strict_json_load(self.paths["LAW_SOURCE_LAW_ID_REGISTRY"])
        expected = {
            "canonical_path": MOD.ENGINE.CANONICAL_PATHS["LAW_SOURCE_LAW_ID_REGISTRY"],
            "filename": MOD.ENGINE.CANONICAL_FILENAMES["LAW_SOURCE_LAW_ID_REGISTRY"],
            "law_registry_entry_count": MOD.ENGINE.EXPECTED["laws"],
            "law_registry_entry_fingerprint_sha256": registry["entry_fingerprint_sha256"],
            "law_registry_ref": registry["SYSTEM_DESIGNATION"],
            "law_registry_version": registry["registry_version"],
            "sha256": MOD.ENGINE.file_sha256(self.paths["LAW_SOURCE_LAW_ID_REGISTRY"]),
            "semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
        }
        self.assertEqual(router["source_of_truth"], expected)
        result = MOD.ENGINE._with_transition_context(self.paths, MOD.ENGINE.validate_law_router, router, core_text)
        self.assertEqual(result["law_count"], 83)
        self.assertEqual(result["active_law_resolution_contract"], "AIR_LAW_RESOLUTION_CONSTRUCTION_V2@2.0.0")

    def test_dt_t37_law_router_source_of_truth_mismatch_fails_closed(self):
        core_text = MOD.ENGINE.read_text(self.paths["CORE_RUNTIME"])
        prior_router = MOD.ENGINE.strict_json_load(self.paths["LAW_APPLICABILITY_ROUTER"])
        router = MOD.ENGINE._with_transition_context(self.paths, MOD.ENGINE.regenerate_law_router, core_text, prior_router)
        mutations = {
            "canonical_path": "law_source/BROKEN.json",
            "filename": "BROKEN_REGISTRY.json",
            "law_registry_entry_count": 82,
            "law_registry_entry_fingerprint_sha256": "0" * 64,
            "law_registry_ref": "BROKEN_REGISTRY",
            "law_registry_version": "0.0.0",
            "sha256": "0" * 64,
            "semantic_owner": "BROKEN_OWNER",
        }
        for field, bad_value in mutations.items():
            with self.subTest(field=field):
                mutated = json.loads(json.dumps(router))
                mutated["source_of_truth"][field] = bad_value
                with self.assertRaises(MOD.ENGINE.CompileError):
                    MOD.ENGINE._with_transition_context(self.paths, MOD.ENGINE.validate_law_router, mutated, core_text)


if __name__ == "__main__":
    unittest.main()

# ---------------------------------------------------------------------------
# AMRS4E transition-readiness remediation coverage
# ---------------------------------------------------------------------------
import shutil as _tr_shutil

_TRANSITION_PRE_F_PAYLOAD_MAP_SHA256 = "569aab74681b12e0ba3628e87fd4cd96bfb1f4d8c70c38d6b81d0f2171bd452f"
_TRANSITION_POST_F_PACKAGE_PIN = {
    "contract_id": "AIR_LAW_SOURCE_PACKAGE_PIN_V1",
    "contract_version": "1.0.0",
    "package_id": "AIR_LAW_SOURCE_PACKAGE_V1",
    "package_version": "1.0.0-AMRS4F-OPERATIVE",
    "manifest_sha256": "6618da3c251024eacfebb94ee1a17df70e1c98df9acd719cf003982770174763",
    "content_fingerprint_sha256": "a99fe6c9fc40f6d2aa99dc3221c599bcbd948ab007fee7790ff221512d1ae3c1",
    "law_registry_fingerprint_sha256": "915f3f3f03b23106de450b5f5a6480d2122114a21d58c7da32ab769df0cf4686",
    "router_fingerprint_sha256": "a7d45d8a1392107ad8ebcd2c989ada9b109cd508e2986d08e87f945fed3a1960",
    "floor_registry_fingerprint_sha256": "373451fb4952df32b49b24d902e4631c9c7a66b112fa87668ab5e1136ac88622",
    "expected_law_count": 83,
    "runtime_compatibility": {
        "runtime_family": "AIR_CORE_RUNTIME_V2",
        "semantic_owner_cutover_required_for_package_mode": True,
        "target_amrs": 6,
    },
    "positive_execution_authority": "NONE",
}
_TRANSITION_SOURCE_FAMILY_FP = "d7469d984c3b2d13f9797aa79ae673e30ac4ff0c787aace62522410c7309f74b"


def _transition_build_exact_post_f_core(source_root: Path) -> bytes:
    core = (source_root / "prompts" / "AIR_CORE_RUNTIME.md").read_bytes()
    law_bodies = sorted((source_root / "law_source" / "laws").glob("*.md"))
    if len(law_bodies) != 82:
        raise AssertionError(f"expected 82 law bodies, got {len(law_bodies)}")
    spans = []
    for p in law_bodies:
        body = p.read_bytes()
        if core.count(body) != 1:
            raise AssertionError(f"law body not unique in pre-F Core: {p.name}")
        start = core.find(body)
        spans.append((start, start + len(body)))
    spans.sort()
    for a, b in zip(spans, spans[1:]):
        if a[1] > b[0]:
            raise AssertionError("law body spans overlap")
    candidate = core
    for start, end in reversed(spans):
        candidate = candidate[:start] + candidate[end:]

    sf = []
    for p in sorted((source_root / "law_source").rglob("*")):
        if p.is_file():
            raw = p.read_bytes()
            sf.append({
                "path": p.relative_to(source_root).as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "size_bytes": len(raw),
            })
    if len(sf) != 114:
        raise AssertionError(f"expected 114 law-source files, got {len(sf)}")
    sf_fp = hashlib.sha256(json.dumps(sf, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    if sf_fp != _TRANSITION_SOURCE_FAMILY_FP:
        raise AssertionError("law-source family fingerprint drift")

    contract = {
        "SYSTEM_DESIGNATION": "AIR_AMRS4F_SEMANTIC_OWNER_CUTOVER_V1",
        "active_law_resolution_contract": "AIR_LAW_RESOLUTION_CONSTRUCTION_V2@2.0.0",
        "canonical_source_family": {
            "body_index_ref": "law_source/AIR_LAW_BODY_INDEX.json",
            "content_fingerprint_sha256": sf_fp,
            "file_count": 114,
            "floor_body_count": 28,
            "floor_index_ref": "law_source/AIR_FLOOR_INVARIANT_INDEX.json",
            "law_registry_ref": "law_source/AIR_LAW_ID_REGISTRY.json",
            "physical_law_body_count": 82,
            "root": "law_source/",
            "stable_law_id_count": 83,
        },
        "contract_version": "1.0.0",
        "core_deembedding": {
            "externalized_floor_body_count": 28,
            "externalized_stable_law_id_count": 83,
            "full_83_law_bodies_in_core": False,
            "full_floor_body_corpus_in_core": False,
            "removed_physical_law_body_count": 82,
            "retained_core_owned_capabilities": [
                "AIR_RUNTIME_IDENTITY_AND_FAIL_CLOSED_ACTIVATION",
                "TIER0_TIER3_BOOT_PROFILE_DISPATCH_AND_RETRIEVAL_SCOPE_ENFORCEMENT",
                "AIR_LAW_SOURCE_PROVIDER_ADAPTER_CONTRACTS",
                "LAW_SOURCE_PACKAGE_PIN_AND_MANIFEST_VALIDATION",
                "LAW_SOURCE_RESOLUTION_AND_FALLBACK_SEMANTICS",
                "AIR_LAW_RESOLUTION_CONSTRUCTION_V2",
                "MATERIAL_EXECUTION_INTERLOCK_UNTIL_REQUIRED_LAWS_RESOLVED",
                "BOOTSTRAP_FLOOR_INVARIANTS_NEEDED_TO_VALIDATE_EXTERNAL_LAW_PACKAGE",
                "PRE_REGISTRY_CORE_2_8_ACTIVATION_KERNEL",
                "NORMATIVE_LAW_RESOLUTION_CONSTRUCTION_KERNEL",
            ],
        },
        "cutover_state": "PACKAGE_ENABLED_RELEASE_SEMANTIC_OWNER_CUTOVER_COMPLETE",
        "legacy_v1_state": "LEGACY_EMBEDDED_RELEASE_ONLY_NOT_ACTIVE_FOR_THIS_PACKAGE_ENABLED_SOURCE",
        "next_boundary": "AMRS4G_INTEGRATED_SYSTEM_REPROOF_NO_V4_BUILD",
        "operative_floor_body_semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
        "operative_law_body_semantic_owner": "AIR_LAW_SOURCE_PACKAGE_V1",
        "package_pin": _TRANSITION_POST_F_PACKAGE_PIN,
        "positive_execution_authority": "NONE",
        "semantic_owner": "AIR_CORE_RUNTIME_V2_BOOTSTRAP_TRUST_KERNEL",
        "supersession": {
            "package_or_provider_state_positive_execution_authority": "NONE",
            "prior_semantic_owner_cutover_prohibition": "SATISFIED_BY_THIS_AMRS4F_CUTOVER",
            "prior_shadow_state": "SUPERSEDED_FOR_THIS_PACKAGE_ENABLED_SOURCE",
            "provider_identity_semantic_authority": "NONE",
        },
    }
    sentinel = b"AIR_LOAD_SENTINEL :: AIR_CORE_RUNTIME :: END_OF_FILE :: LOAD_INTEGRITY_V2"
    pos = candidate.rfind(sentinel)
    if pos < 0:
        raise AssertionError("Core terminal sentinel missing")
    prefix = candidate[:pos].rstrip(b"\n") + b"\n\n"
    block = (
        "==================================================\n"
        "AMRS-4F SEMANTIC OWNER CUTOVER AND CORE LAW-BODY DE-EMBEDDING\n"
        "==================================================\n\n"
        "Patch marker: AIR_AMRS4F_SEMANTIC_OWNER_CUTOVER_V1\n\n"
        "AMRS-4F makes the exact pinned law-source package the operative semantic owner for the 83 stable law identities and 28 floor bodies, while Core retains only the bootstrap trust kernel required to validate, retrieve, bind, and fail closed around that package. Provider identity remains provenance only and grants no semantic or execution authority.\n\n"
        "AIR_AMRS4F_SEMANTIC_OWNER_CUTOVER_V1_MACHINE_CONTRACT_BEGIN\n```json\n"
        + json.dumps(contract, indent=2, sort_keys=True, ensure_ascii=False)
        + "\n```\nAIR_AMRS4F_SEMANTIC_OWNER_CUTOVER_V1_MACHINE_CONTRACT_END\n\n"
        "AMRS-4F cutover rule: for this package-enabled source state, AIR_LAW_RESOLUTION_CONSTRUCTION_V2@2.0.0 is the active law-resolution contract. AIR_LAW_RESOLUTION_CONSTRUCTION_V1@1.0.0 remains valid only for exact legacy embedded-law releases and is not the active resolution contract for this source state.\n\n"
    ).encode("utf-8")
    result = prefix + block + sentinel + b"\n"
    observed = hashlib.sha256(result).hexdigest()
    if observed != MOD.ENGINE.POST_F_CORE_SHA256:
        raise AssertionError(f"exact post-F Core fixture hash mismatch: {observed}")
    return result


class AirPAMRS4ETransitionReadinessTests(unittest.TestCase):
    def test_transition_post_f_payload_map_is_current(self):
        payload_map = MOD.payload_hash_map(MOD.build_payloads())
        observed = hashlib.sha256(json.dumps(payload_map, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(observed, "40f6c52d63aa688b8d6d9563eee9077851686054f2ee87dd4bdf0d163b2ca0ad")

    def test_transition_declares_exact_two_core_states(self):
        self.assertEqual(MOD.ENGINE.PRE_F_CORE_SHA256, "e4fb9fc9ac5b50d7d2d043a9489a086b398f543c41eefdc2762e92fb5e06b835")
        self.assertEqual(MOD.ENGINE.POST_F_CORE_SHA256, "6007ab277ebcd0d59911fce6384a8ef417dbdd6f3eea38bfc71e39013b097588")
        self.assertNotIn("*", MOD.ENGINE.POST_F_CORE_SHA256)

    def test_transition_exact_post_f_state_compiles_from_standalone_sources(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "source"
            _tr_shutil.copytree(HERE.parent, target)
            paths = MOD.default_source_paths(target)
            self.assertEqual(MOD.ENGINE.file_sha256(paths["CORE_RUNTIME"]), MOD.ENGINE.POST_F_CORE_SHA256)
            result = MOD.ENGINE.validate_source_inputs(paths)
            self.assertEqual(result["runtime_state"], MOD.ENGINE.POST_F_RUNTIME_STATE)
            self.assertEqual(result["law_router"]["active_law_resolution_contract"], "AIR_LAW_RESOLUTION_CONSTRUCTION_V2@2.0.0")
            payloads = MOD.ENGINE.build_payloads(paths)
            pin = payloads["compiled/AIR_LAW_SOURCE_PACKAGE_PIN.json"]
            self.assertEqual(pin["manifest_sha256"], _TRANSITION_POST_F_PACKAGE_PIN["manifest_sha256"])
            self.assertEqual(pin["activation_state"], "ACTIVE_PACKAGE_ENABLED_RELEASE_AMRS4F_SEMANTIC_OWNER_CUTOVER_COMPLETE")
            source_manifest = payloads["compiled/AIR_P_SOURCE_MANIFEST.json"]
            self.assertEqual(source_manifest["law_source_family"]["state"], "PACKAGE_ENABLED_SEMANTIC_OWNER_ACTIVE")
            self.assertEqual(source_manifest["law_source_family"]["active_law_resolution_contract"], "AIR_LAW_RESOLUTION_CONSTRUCTION_V2@2.0.0")
            components = payloads["compiled/AIR_P_COMPONENT_REGISTRY.json"]["components"]
            self.assertEqual(sum(1 for x in components if x["source_anchor"]["canonical_role"] == "LAW_SOURCE_BODY"), 82)
            self.assertEqual(sum(1 for x in components if x["source_anchor"]["canonical_role"] == "CORE_RUNTIME"), 31)
            refs = payloads["compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json"]["anchors"]
            self.assertTrue(any(x["canonical_source_path"].startswith("law_source/laws/") for x in refs))
            projections = payloads["compiled/AIR_P_CONTROL_GOVERNANCE_PROJECTIONS.json"]["projections"]
            law_source_projection = next(x for x in projections if x["source_role"] == "LAW_SOURCE_PACKAGE_SCHEMA")
            self.assertEqual(law_source_projection["effect"], "PACKAGE_ENABLED_LAW_SOURCE_SEMANTIC_OWNER_AND_VALIDATION_INPUT")
            conformance = payloads["compiled/AIR_P_CONFORMANCE_PROFILE.json"]["required_checks"]
            self.assertIn("LAW_SOURCE_PACKAGE_ACTIVE_V2_SEMANTIC_OWNER", conformance)
            self.assertIn("LAW_ROUTER_83_OF_83_REGENERATED_FROM_STANDALONE_LAW_REGISTRY", conformance)
            self.assertNotIn("LAW_SOURCE_PACKAGE_SHADOW_ONLY_V1_REMAINS_OPERATIVE", conformance)
            out = Path(td) / "compiled-output"
            MOD.ENGINE.compile_package(out, paths, test_source=target / "air_p" / "tests" / "test_air_p_compiler.py")
            compilation_report = json.loads((out / "evidence" / "AIR_P_COMPILATION_REPORT.json").read_text())
            self.assertEqual(compilation_report["law_source_family"], "114/114 PACKAGE_ENABLED_SEMANTIC_OWNER_VALIDATED")
            self.assertEqual(compilation_report["law_router"], "83/83 REGENERATED_FROM_EXACT_PRIOR_ROUTER_PLUS_STANDALONE_LAW_REGISTRY")
            semantic_report = json.loads((out / "evidence" / "AIR_P_SEMANTIC_EQUIVALENCE_REPORT.json").read_text())
            self.assertEqual(semantic_report["law_source_package_mode"], "ACTIVE_PACKAGE_ENABLED_V2_SEMANTIC_OWNER")
            run_manifest = json.loads((out / "AIR_P_RUN_MANIFEST.json").read_text())
            self.assertEqual(run_manifest["validation"]["law_source_package_manifest_and_pin"], "PASS_DETERMINISTIC_ACTIVE_PACKAGE_ENABLED")
            self.assertEqual(run_manifest["validation"]["independent_process_reproducibility"], "EXTERNAL_RELEASE_GRADE_REPROOF_REQUIRED_SEPARATELY")
            self.assertEqual(run_manifest["decision"], "PASS_DETERMINISTIC_COMPILATION_EXTERNAL_RELEASE_GRADE_REPROOF_SEPARATE")

    def test_transition_unknown_core_hash_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "source"
            _tr_shutil.copytree(HERE.parent, target)
            core = target / "prompts" / "AIR_CORE_RUNTIME.md"
            core.write_bytes(core.read_bytes() + b"\nUNAPPROVED_DRIFT\n")
            with self.assertRaises(MOD.ENGINE.CompileError):
                MOD.ENGINE.validate_source_inputs(MOD.default_source_paths(target))

class AirPV081RepositoryBootSurfaceRegressionTests(unittest.TestCase):
    def _starter(self):
        return json.loads((HERE.parent / "prompts" / "AIR_DEFAULT_STARTER_PROFILE.json").read_text(encoding="utf-8"))

    def test_v081_current_handoff_metadata_reconciles_to_rev26(self):
        starter = self._starter()
        consumer = starter["compiler_contract"]["decision_trace_transition_consumer_contract"]
        revision = starter["handoff_contract"]["revision_identity_contract"]
        self.assertEqual(consumer["current_handoff_template_revision"], 26)
        self.assertEqual(consumer["current_handoff_sha256"], "8d1c87d3d4d2b191301eec9f27e83ac1e550b0ba99bede5a5d576e9d52e5f122")
        self.assertEqual(revision["current_template_revision"], 26)
        self.assertEqual(revision["current_template_state_id"], "R23_AMRS4F_PACKAGE_ENABLED_SEMANTIC_OWNER_CUTOVER")

    def test_v081_canonical_first_message_commands_are_exact(self):
        starter = self._starter()
        mirror = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        self.assertEqual(mirror["canonical_first_message_commands"], {
            "default_tier0": "Start a new AIR-P project.",
            "explicit_tier0": "Start a new AIR-P project. Tier0 boot.",
            "explicit_tier1": "Start a new AIR-P project. Tier1 boot.",
            "explicit_tier2": "Start a new AIR-P project. Tier2 boot.",
            "explicit_tier3": "Start a new AIR-P project. Tier3 boot.",
        })

    def test_v081_explicit_commands_are_bound_to_expected_profiles(self):
        starter = self._starter()
        mirror = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        dispatch = mirror["user_boot_profile_dispatch"]
        commands = mirror["canonical_first_message_commands"]
        self.assertIn(commands["explicit_tier0"], dispatch["TIER_0_ROUTINE"]["selection_aliases"])
        self.assertIn(commands["explicit_tier1"], dispatch["TIER_1_NAVIGATION"]["selection_aliases"])
        self.assertIn(commands["explicit_tier2"], dispatch["TIER_2_TARGETED_SOURCE"]["selection_aliases"])
        self.assertIn(commands["explicit_tier3"], dispatch["TIER_3_DEEP_AUDIT"]["selection_aliases"])

    def test_v081_exact_boundary_guard_covers_tier0_dependency_closure(self):
        starter = self._starter()
        mirror = starter["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        guard = mirror["exact_section_boundary_guard"]
        self.assertIn("Tier0 dependency-closure", guard)
        self.assertIn("discarded before model-visible ingestion", guard)
        self.assertTrue(any("adjacent context" in x for x in mirror["user_boot_profile_dispatch"]["TIER_0_ROUTINE"]["negative_requirements"]))

