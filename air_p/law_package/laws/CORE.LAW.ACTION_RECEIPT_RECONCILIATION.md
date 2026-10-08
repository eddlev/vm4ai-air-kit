==================================================
ACTION RECEIPT AND RECONCILIATION LAW
==================================================

Patch marker: AIR_ACTION_RECEIPT_RECONCILIATION_V4
Floor invariant: AIR-FLOOR-018-MATERIAL-ACTION-AUTHORIZATION-AND-RECEIPT

RT.RECEIPT uniquely owns post-material-effect reconciliation.

For every attempted material action:
1. capture tool/operator evidence and actual target/effect
2. compare expected versus actual
3. record unexpected side effects and effect identifiers
4. run required post-effect alignment/reconciliation
5. update artifact lease/scope/source/environment state when affected
6. construct AIR_ACTION_RECEIPT
7. block dependent action or closure until receipt validation is sufficient

AIR_ACTION_RECEIPT exact schema:
{
  "AIR_ACTION_RECEIPT": {
    "object_version": "2.0.0",
    "record_class": "ACTION_RECEIPT_RECORD",
    "evidence_class": "SURFACED_OUTPUT_GOVERNANCE_RECORD | SOURCE_SUPPORTED_GOVERNANCE_RECORD | TOOL_OBSERVED_GOVERNANCE_RECORD | BACKEND_ENFORCED_GOVERNANCE_RECORD",
    "evaluation_basis": {},
    "receipt_id": "",
    "authorization_ref": "",
    "action_id": "",
    "intended_target": {},
    "actual_target": {},
    "execution_evidence": [],
    "result": "SUCCESS | PARTIAL | FAILED | UNKNOWN",
    "effect_ids": [],
    "state_comparison": {},
    "unexpected_side_effects": [],
    "validation_result": "PASS | REVIEW | FAIL | UNVERIFIED",
    "artifact_lease_effect": "UNCHANGED | SUSPENDED_REVIEW | EXPIRED_REBIND_REQUIRED | CLOSED",
    "required_state_updates": [],
    "recovery_required": false,
    "runtime_origin": "PROMPT_COMPILED | BACKEND_COMPILED",
    "backend_validation_claimed": false,
    "hidden_reasoning_claimed": false
  }
}

A receipt records observed/received evidence; intended-versus-actual duplication is intrinsic to its comparison responsibility. It does not retroactively authorize an earlier effect and must not embed a full Gate, Artifact, or Authorization object.

