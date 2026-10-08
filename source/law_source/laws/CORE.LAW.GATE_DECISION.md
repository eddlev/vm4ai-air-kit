==================================================
AIR GATE LAW
==================================================

Patch marker: AIR_GATE_V3

Before material execution, transition, approval, closure, mutation, commit, push, deploy, export, destructive action, production-like action, or handoff, evaluate AIR_GATE.

AIR_GATE decision values:
- ALLOW
- REVIEW
- REJECT
- RESCOPE_REQUIRED
- EVIDENCE_REQUIRED

AIR_GATE is a decision record, not a copy of AIR_ARTIFACT or AIR_ACTIVE_CONTRACT. It references the state it evaluated and owns only the gate question, check results, missing evidence/blocking conditions, decision, reason, and safe next action.

Base mandatory schema (conditional top-level references are governed exclusively by AIR_FORMAL_OBJECT_SCHEMA_REGISTRY_V1 and are intentionally omitted from this base example):
{
  "AIR_GATE": {
    "object_version": "2.0.0",
    "record_class": "DECISION_RECORD",
    "evidence_class": "SURFACED_OUTPUT_GOVERNANCE_RECORD | SOURCE_SUPPORTED_GOVERNANCE_RECORD | TOOL_OBSERVED_GOVERNANCE_RECORD | BACKEND_ENFORCED_GOVERNANCE_RECORD",
    "evaluation_basis": {},
    "gate_id": "",
    "exact_gate_question": "",
    "requested_action": "",
    "gate_context": "ACTIVE_ARTIFACT_ACTION | CANDIDATE_BINDING_TRANSITION",
    "evaluation_checks": {
      "artifact_binding": "PASS | REVIEW | FAIL",
      "artifact_freshness": "PASS | REVIEW | FAIL",
      "scope": "PASS | REVIEW | FAIL",
      "out_of_scope": "PASS | REVIEW | FAIL",
      "allowed_action": "PASS | REVIEW | FAIL",
      "evidence": "PASS | REVIEW | FAIL",
      "stop_condition": "PASS | REVIEW | FAIL"
    },
    "required_evidence": [],
    "blocking_conditions": [],
    "decision": "ALLOW | REVIEW | REJECT | RESCOPE_REQUIRED | EVIDENCE_REQUIRED",
    "reason": [],
    "safe_next_action": "",
    "runtime_origin": "PROMPT_COMPILED | BACKEND_COMPILED",
    "backend_validation_claimed": false,
    "hidden_reasoning_claimed": false
  }
}

Gate context law:
- ACTIVE_ARTIFACT_ACTION requires current active_artifact_ref with artifact_id, artifact_revision, and artifact_lease_id; candidate_artifact_ref must be absent.
- CANDIDATE_BINDING_TRANSITION requires a schema-valid candidate_artifact_ref; active_artifact_ref must be absent. A candidate carries no positive execution authority.
- approval_scope_ref is mandatory when explicit approval materially controls the transition and otherwise follows the registry condition. Approval capture alone is non-authorizing input.
- active_contract_ref is mandatory only when active_contract_material is true.
- Conditional reference presence/absence is validated before Gate precheck; null placeholders do not satisfy required conditional references and do not bypass forbidden-field rules.
- RT.APPROVAL_RESOLVE is context-sensitive; it does not unconditionally manufacture an active-artifact Gate.
- Material action Authorization requires a bound Artifact, ACTIVE lease, exact scope pin, current ALLOW Gate, and matching approval basis.

The prior Gate fields mode, artifact_binding_state, authority_level, authorized_action_ids, excluded_action_ids, stop_conditions, and individual *_check top-level aliases are retired from the canonical Gate shape. Their authoritative source is the Artifact/Contract or the nested evaluation_checks projection.

ALLOW requires all applicable evaluation_checks to pass and required_evidence/blocking_conditions to permit the action. REVIEW is used for resolvable ambiguity. EVIDENCE_REQUIRED identifies missing proof. RESCOPE_REQUIRED identifies valid intent outside the active boundary. REJECT identifies a hard conflict or stop condition.

