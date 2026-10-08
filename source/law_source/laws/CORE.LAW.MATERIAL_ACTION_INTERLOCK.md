==================================================
MATERIAL ACTION INTERLOCK LAW
==================================================

Patch marker: AIR_MATERIAL_ACTION_INTERLOCK_V3
Floor invariant: AIR-FLOOR-018-MATERIAL-ACTION-AUTHORIZATION-AND-RECEIPT

RT.ACTION is the unique positive material-action route.

Before constructing AIR_ACTION_AUTHORIZATION, require:
1. current RT.ALIGN evaluation basis
2. exactly one bound Orbit 0 AIR_ARTIFACT
3. ACTIVE artifact lease
4. exact resource_scope_pin match
5. current source/environment basis
6. DEP.INTENT_EXECUTION_ALIGNMENT_CURRENT = SATISFIED for the exact proposed action
7. current approval when required
8. AIR_GATE decision = ALLOW for the proposed action
9. action remains within artifact allowed actions and stop conditions are false

AIR_ACTION_AUTHORIZATION is a single-use execution ticket for exactly one declared effect. It is not an alternative to AIR_GATE and must not repeat the Gate evaluation as a second decision surface.

AIR_ACTION_AUTHORIZATION exact schema:
{
  "AIR_ACTION_AUTHORIZATION": {
    "object_version": "2.0.0",
    "record_class": "ACTION_AUTHORIZATION_RECORD",
    "evidence_class": "SURFACED_OUTPUT_GOVERNANCE_RECORD | SOURCE_SUPPORTED_GOVERNANCE_RECORD | TOOL_OBSERVED_GOVERNANCE_RECORD | BACKEND_ENFORCED_GOVERNANCE_RECORD",
    "evaluation_basis": {},
    "authorization_id": "",
    "action_id": "",
    "action_class": "",
    "requested_action": "",
    "controlling_artifact_ref": {
      "artifact_id": "",
      "artifact_revision": "",
      "artifact_lease_id": ""
    },
    "target": {},
    "gate_ref": "",
    "approval_basis_or_ref": null,
    "resource_scope_pin_ref": null,
    "expected_effect": "",
    "receipt_evidence_required": [],
    "authorization_invalidators": [],
    "single_use": true,
    "consumption_state": "UNCONSUMED | CONSUMED | INVALIDATED",
    "decision": "ALLOW",
    "runtime_origin": "PROMPT_COMPILED | BACKEND_COMPILED",
    "backend_validation_claimed": false,
    "hidden_reasoning_claimed": false
  }
}

The authorization references gate_ref, controlling_artifact_ref, resource_scope_pin_ref, and approval_basis_or_ref. It must not copy AIR_GATE.evaluation_checks, AIR_ARTIFACT.execution_contract, or the full approval/stop-condition state.

After the material effect is attempted:
- pre-effect evaluation basis becomes stale for post-effect state
- execute POST_MATERIAL_EFFECT alignment/reconciliation
- emit AIR_ACTION_RECEIPT before any dependent action, closure, or receiver-facing success claim

Bootstrap writes, scope broadening, action replay, and retrospective authorization are prohibited.

