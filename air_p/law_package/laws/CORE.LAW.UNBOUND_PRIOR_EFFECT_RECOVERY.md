==================================================
UNBOUND PRIOR EFFECT RECOVERY LAW
==================================================

Patch marker: AIR_UNBOUND_PRIOR_EFFECT_RECOVERY_V3

When AIR detects that a material action occurred without a valid current AIR_ACTION_AUTHORIZATION, current artifact lease, or matching scope pin, it must create AIR_PRIOR_EFFECT_RECORD.

Retrospective authorization is prohibited. A later artifact or approval may govern future reconciliation but must not rewrite the earlier action as authorized.

AIR_PRIOR_EFFECT_RECORD exact schema:
{
  "AIR_PRIOR_EFFECT_RECORD": {
    "object_version": "2.0.0",
    "record_class": "RECOVERY_RECORD",
    "evidence_class": "SURFACED_OUTPUT_GOVERNANCE_RECORD | SOURCE_SUPPORTED_GOVERNANCE_RECORD | TOOL_OBSERVED_GOVERNANCE_RECORD | BACKEND_ENFORCED_GOVERNANCE_RECORD",
    "evaluation_basis": {},
    "prior_effect_id": "",
    "discovered_effect": {},
    "observed_target": {},
    "effect_evidence": [],
    "authorization_state_at_effect": "VALID | MISSING | STALE | INVALID | UNKNOWN",
    "scope_match_state_at_effect": "MATCH | MISMATCH | UNKNOWN",
    "lease_state_at_effect": "ACTIVE | SUSPENDED_REVIEW | EXPIRED_REBIND_REQUIRED | CLOSED | MISSING | UNKNOWN",
    "affected_artifact_ref": null,
    "risk_state": "LOW | MEDIUM | HIGH | UNKNOWN",
    "rollback_feasibility": "AVAILABLE | PARTIAL | UNAVAILABLE | UNKNOWN",
    "reconciliation_state": "RETAIN_PENDING_RECONCILIATION | REVERT_RECOMMENDED | REPLACE_RECOMMENDED | HUMAN_REVIEW_REQUIRED | OUT_OF_SCOPE_EFFECT | RESOLVED_WITH_EVIDENCE",
    "human_review_requirement": null,
    "safe_next_action": "",
    "retroactive_authorization_forbidden": true,
    "runtime_origin": "PROMPT_COMPILED | BACKEND_COMPILED",
    "backend_validation_claimed": false,
    "hidden_reasoning_claimed": false
  }
}

The record owns recovery facts for the observed prior effect. AIR_SESSION and AIR_ARTIFACT may carry only compact unresolved-effect refs/status, and AIR_HANDOFF_CARD may serialize the record/history for transfer. They must not create competing recovery truth.

Consequential effects remain blocking until reconciled or explicitly accepted by the authorized human decision owner.

