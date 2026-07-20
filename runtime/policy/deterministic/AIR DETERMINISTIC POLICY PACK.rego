package air.deterministic_policy

import rego.v1

policy_pack_id := "AIR_DETERMINISTIC_POLICY_PACK_V1"
policy_pack_version := "1.1.0"

required_fields := [
  "policy_pack_id", "policy_pack_version", "policy_mode", "policy_posture",
  "active_contract_id", "active_step", "action_class", "effect_level", "environment",
  "resource_classes", "approval_required", "approval_present", "binding_requested",
  "validation_state", "repository_action", "release_action", "dependency_state",
  "taxonomy_binding_state", "human_status_transfer_state", "claim_state", "evidence_state",
  "unknown_fields", "input_provenance", "material_transition", "tool_configured",
  "tool_available", "tool_authorized", "tool_invoked", "tool_endpoint"
]

missing_required contains field if {
  some field in required_fields
  object.get(input, field, "__AIR_MISSING__") == "__AIR_MISSING__"
}

violations contains {"id":"AIR-POL-000","decision":"ERROR","reason":reason,"required_evidence":["complete canonical input"],"prohibited_effects":["operational ALLOW"]} if {
  count(missing_required) > 0
  reason := sprintf("Missing required fields: %v", [sort([x | some x in missing_required])])
}

violations contains {"id":"AIR-POL-000","decision":"ERROR","reason":"Malformed or contradictory canonical input","required_evidence":["corrected canonical input"],"prohibited_effects":["operational ALLOW"]} if {
  object.get(input, "malformed_input", false) == true
}
violations contains {"id":"AIR-POL-000","decision":"ERROR","reason":"Malformed or contradictory canonical input","required_evidence":["corrected canonical input"],"prohibited_effects":["operational ALLOW"]} if {
  object.get(input, "contradictory_input", false) == true
}
violations contains {"id":"AIR-POL-000","decision":"REVIEW","reason":"Unknown action or effect classification","required_evidence":["resolved action/effect classification"],"prohibited_effects":[]} if {
  input.action_class == "UNKNOWN"
}
violations contains {"id":"AIR-POL-000","decision":"REVIEW","reason":"Unknown action or effect classification","required_evidence":["resolved action/effect classification"],"prohibited_effects":[]} if {
  input.effect_level == "UNKNOWN"
}

material_actions := {"GENERATE","MUTATE","BIND","DEPLOY","REPOSITORY","RELEASE","DESTRUCTIVE"}
violations contains {"id":"AIR-POL-000","decision":"EVIDENCE_REQUIRED","reason":"Material unknown fields remain unresolved","required_evidence":["resolve unknown fields"],"prohibited_effects":[]} if {
  count(input.unknown_fields) > 0
  input.action_class in material_actions
}
violations contains {"id":"AIR-POL-000","decision":"REVIEW","reason":"Non-material unknown fields require review","required_evidence":["resolve unknown fields"],"prohibited_effects":[]} if {
  count(input.unknown_fields) > 0
  not input.action_class in material_actions
}

violations contains {"id":"AIR-POL-100","decision":"REJECT","reason":"Material action lacks scoped approval","required_evidence":["scoped user approval"],"prohibited_effects":["material action"]} if {
  input.action_class in material_actions
  input.approval_required == true
  input.approval_present == false
}

violations contains {"id":"AIR-POL-110","decision":"REJECT","reason":"Reusable binding requires current validation PASS","required_evidence":["current validation PASS"],"prohibited_effects":["binding"]} if {
  input.binding_requested == true
  input.validation_state != "PASS"
}
violations contains {"id":"AIR-POL-110","decision":"REJECT","reason":"Reusable binding lacks explicit binding approval","required_evidence":["explicit binding approval"],"prohibited_effects":["binding"]} if {
  input.binding_requested == true
  object.get(input, "binding_approval_present", input.approval_present) == false
}

violations contains {"id":"AIR-POL-120","decision":"REJECT","reason":"Repository action lacks separate repository approval","required_evidence":["repository approval"],"prohibited_effects":["repository mutation"]} if {
  input.repository_action == true
  object.get(input, "repository_approval_present", false) == false
}
violations contains {"id":"AIR-POL-120","decision":"REJECT","reason":"Release action lacks separate release approval","required_evidence":["release approval"],"prohibited_effects":["publication or release"]} if {
  input.release_action == true
  object.get(input, "release_approval_present", false) == false
}

violations contains {"id":"AIR-POL-130","decision":"REJECT","reason":"Artifact or policy attempted self-approval/self-binding","required_evidence":["external approval"],"prohibited_effects":["self-approval","self-binding"]} if {
  object.get(input, "artifact_self_approval", false) == true
}
violations contains {"id":"AIR-POL-130","decision":"REJECT","reason":"Artifact or policy attempted self-approval/self-binding","required_evidence":["external approval"],"prohibited_effects":["self-approval","self-binding"]} if {
  object.get(input, "policy_self_approval", false) == true
}

mandatory_dependency if object.get(input.dependency_state, "mandatory_external_engine", false) == true
mandatory_dependency if object.get(input.dependency_state, "mandatory_hosted_service", false) == true
mandatory_dependency if object.get(input.dependency_state, "mandatory_package_manager", false) == true
mandatory_dependency if object.get(input.dependency_state, "mandatory_network", false) == true
mandatory_dependency if object.get(input.dependency_state, "mandatory_central_service", false) == true
violations contains {"id":"AIR-POL-200","decision":"REJECT","reason":"Optional external infrastructure was made mandatory","required_evidence":[],"prohibited_effects":["mandatory external dependency"]} if mandatory_dependency

violations contains {"id":"AIR-POL-300","decision":"REJECT","reason":"Raw human taxonomy attempted direct operative binding","required_evidence":["approved translator output"],"prohibited_effects":["raw taxonomy binding"]} if {
  input.taxonomy_binding_state in {"RAW_DIRECT_BINDING","UNTRANSLATED_BINDING_ATTEMPT"}
}
violations contains {"id":"AIR-POL-310","decision":"REJECT","reason":"Human status or authority transfer is prohibited","required_evidence":[],"prohibited_effects":["human status transfer"]} if {
  not input.human_status_transfer_state in {"NONE","NOT_APPLICABLE"}
}

claim_pairs := {
  "backend_enforced":"backend_enforced", "cryptographically_verified":"cryptographically_verified",
  "repository_aligned":"repository_observed", "release_ready":"release_evidence",
  "compliant":"compliance_evidence", "professional_equivalent":"professional_equivalence_evidence",
  "empirically_improved":"empirical_evidence"
}
violations contains {"id":"AIR-POL-400","decision":"REJECT","reason":reason,"required_evidence":[evidence_key],"prohibited_effects":[prohibited]} if {
  some claim_key, evidence_key in claim_pairs
  object.get(input.claim_state, claim_key, false) == true
  object.get(input.evidence_state, evidence_key, false) == false
  reason := sprintf("Claim %s lacks matching evidence", [claim_key])
  prohibited := sprintf("claim:%s", [claim_key])
}

violations contains {"id":"AIR-POL-500","decision":"REJECT","reason":"PROMPT_SIMULATED result cannot claim TOOL_EVALUATED evidence","required_evidence":["external tool evidence"],"prohibited_effects":["tool-evaluated claim"]} if {
  input.policy_mode == "PROMPT_SIMULATED"
  object.get(input.claim_state, "tool_evaluated", false) == true
}
violations contains {"id":"AIR-POL-500","decision":"REVIEW","reason":"TOOL_EVALUATED provenance is missing","required_evidence":["engine/version/policy/input/timestamp/adapter provenance"],"prohibited_effects":["tool-evaluated claim"]} if {
  input.policy_mode == "TOOL_EVALUATED"
  object.get(input, "tool_provenance_present", false) == false
}
violations contains {"id":"AIR-POL-500","decision":"REJECT","reason":"TOOL_EVALUATED mode selected without tool invocation","required_evidence":["tool invocation evidence"],"prohibited_effects":["tool-evaluated claim"]} if {
  input.policy_mode == "TOOL_EVALUATED"
  input.tool_invoked == false
}

violations contains {"id":"AIR-POL-600","decision":"ERROR","reason":reason,"required_evidence":[],"prohibited_effects":["operational ALLOW"]} if {
  err := object.get(input, "engine_error", "")
  err in {"PARSE_ERROR","COMPILE_ERROR","EVALUATION_ERROR","ENGINE_ERROR"}
  reason := sprintf("Policy engine failure: %s", [err])
}
violations contains {"id":"AIR-POL-600","decision":"EVIDENCE_REQUIRED","reason":"Policy result is undefined","required_evidence":["defined result"],"prohibited_effects":["operational ALLOW"]} if object.get(input, "undefined_result", false) == true
violations contains {"id":"AIR-POL-600","decision":"REVIEW","reason":"Policy or input schema version mismatch","required_evidence":["matching versions"],"prohibited_effects":["tool-evaluated claim"]} if object.get(input, "policy_version_mismatch", false) == true
violations contains {"id":"AIR-POL-600","decision":"REVIEW","reason":"Policy or input schema version mismatch","required_evidence":["matching versions"],"prohibited_effects":["tool-evaluated claim"]} if object.get(input, "schema_mismatch", false) == true

violations contains {"id":"AIR-POL-610","decision":"EVIDENCE_REQUIRED","reason":"Active contract requires tool evaluation but the local tool path is unavailable or unauthorized","required_evidence":["available and authorized local engine"],"prohibited_effects":["material transition"]} if {
  object.get(input, "tool_required_by_contract", false) == true
  not (input.tool_available == true and input.tool_authorized == true)
}
allowed_endpoints := {"LOCAL_CLI","127.0.0.1","127.0.0.1:8181","localhost","localhost:8181","::1","[::1]:8181"}
violations contains {"id":"AIR-POL-620","decision":"REJECT","reason":"OPA endpoint is not a permitted local CLI or loopback target","required_evidence":["separately approved remote-service architecture"],"prohibited_effects":["non-loopback policy endpoint"]} if {
  not input.tool_endpoint in allowed_endpoints
}
violations contains {"id":"AIR-POL-630","decision":"REJECT","reason":"A central AIR policy service was made a baseline dependency","required_evidence":[],"prohibited_effects":["central-service dependency"]} if object.get(input, "central_service_required", false) == true
violations contains {"id":"AIR-POL-700","decision":"REJECT","reason":"Policy result conflicts with stricter Runtime/AIR_GATE state","required_evidence":["resolved governing conflict"],"prohibited_effects":["policy override"]} if object.get(input, "runtime_conflict", false) == true

rank_map := {"ALLOW":0,"REVIEW":1,"EVIDENCE_REQUIRED":2,"REJECT":3,"ERROR":4}
ranks := [rank_map[v.decision] | some v in violations]
max_rank := max(ranks) if count(ranks) > 0
max_rank := 0 if count(ranks) == 0
final_decision := "ALLOW" if max_rank == 0
final_decision := "REVIEW" if max_rank == 1
final_decision := "EVIDENCE_REQUIRED" if max_rank == 2
final_decision := "REJECT" if max_rank == 3
final_decision := "ERROR" if max_rank == 4

matched_rule_ids := sort([v.id | some v in violations]) if count(violations) > 0
matched_rule_ids := ["AIR-POL-ALLOW-DEFAULT"] if count(violations) == 0
reasons := sort([v.reason | some v in violations]) if count(violations) > 0
reasons := ["No deterministic prohibition or evidence blocker matched"] if count(violations) == 0
required_evidence := sort([e | some v in violations; some e in v.required_evidence])
prohibited_effects := sort([e | some v in violations; some e in v.prohibited_effects])

policy_check_required if input.policy_posture == "HIGH" and input.material_transition == true
policy_check_required if input.policy_posture == "MEDIUM" and input.material_transition == true
policy_check_required if object.get(input, "hard_runtime_gate", false) == true
default policy_check_required := false

tool_preferred if {
  input.policy_posture == "HIGH"
  input.material_transition == true
  input.tool_configured == true
  input.tool_available == true
  input.tool_authorized == true
}
default tool_preferred := false

decision := {
  "decision": final_decision,
  "matched_rule_ids": matched_rule_ids,
  "reasons": reasons,
  "required_evidence": required_evidence,
  "prohibited_effects": prohibited_effects,
  "mode": input.policy_mode,
  "tool_evaluated": input.policy_mode == "TOOL_EVALUATED" and object.get(input, "tool_provenance_present", false) == true and object.get(input, "engine_error", "") == "",
  "policy_pack_id": policy_pack_id,
  "policy_pack_version": policy_pack_version,
  "policy_digest": object.get(input, "policy_digest", null),
  "input_digest": object.get(input, "input_digest", null),
  "evaluation_error": object.get(input, "engine_error", null),
  "fallback_state": object.get(input, "fallback_state", "NONE"),
  "policy_posture": input.policy_posture,
  "material_transition": input.material_transition,
  "policy_check_required": policy_check_required,
  "tool_preferred": tool_preferred,
  "claim_boundary": "Deterministic policy result only; Runtime, active contract, AIR_GATE and scoped approval remain authoritative."
}
