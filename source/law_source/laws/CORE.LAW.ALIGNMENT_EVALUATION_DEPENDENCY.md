==================================================
ALIGNMENT EVALUATION DEPENDENCY LAW
==================================================

Patch marker: AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1
Floor invariant: AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY

ALIGNMENT_EVALUATION is an operation. AIR_ALIGNMENT_CHECK and its coupled AIR_VALIDATION_REPORT are serialized evidence projections of that operation. Printing those records without evaluating the required state does not satisfy this law.

Evaluation profiles:
- BOOTSTRAP
- ACTIVATION
- TURN_ENTRY
- STATE_TRANSITION
- HANDOFF_RESTORE
- PRE_MATERIAL_EFFECT
- POST_MATERIAL_EFFECT
- UNCERTAINTY_RESOLUTION
- RECOVERY

Profile-specific semantics:
- ACTIVATION evaluates the canonical pre-bind activation state used by RT.ACTIVATE after onboarding or restored candidate-state preparation; it is not an alias for BOOTSTRAP or STATE_TRANSITION.
- UNCERTAINTY_RESOLUTION evaluates the canonical state and identified material basis gap immediately before RT.UNCERTAINTY_RESOLVE constructs a required-input, safe-degraded-boundary, review, or evidence-required result; it is not an alias for another profile.
- All profiles share the same current-state/evaluation-basis constructor and differ only in the declared evaluation purpose and material state slice.

Every post-activation user turn executes TURN_ENTRY alignment before semantic instruction handling. There is no configurable interval and no substantive-message classifier.

Alignment evaluation must consume, when material:
- lifecycle and Orbit state
- current artifact identity/revision/binding and active step
- canonical intent and active context
- approval, lease, scope pin, action and receipt state
- source/evidence freshness and required-input state
- MII cognitive coverage, unresolved contribution conflicts, and morphology state
- benchmark, blockers, stop conditions, receiver-delivery state
- prior user-turn count and current incoming instruction class candidate

It produces:
- evaluation_id
- evaluation_profile
- state_epoch
- evaluated_state_refs
- model_drift_evidence_state
- nonmodel_reconciliation_state
- alignment_state
- drift_detected
- recovery_state
- required_formal_object_set
- route eligibility and blocking dependencies
- AIR_ALIGNMENT_CHECK
- coupled AIR_VALIDATION_REPORT

Canonical alignment truth table:
- no established model drift + no unresolved non-model reconciliation => `drift_detected = false`, `alignment_state = ALIGNED`
- no established model drift + unresolved non-model reconciliation => `drift_detected = false`, `alignment_state = RECONCILIATION_REQUIRED`
- established model drift => `drift_detected = true`, `alignment_state = DRIFT_DETECTED`
- `drift_detected` must be a JSON boolean and may never encode ordinary state change, stale state, recovery state, AIR error, scope change, task change, source change, approval change, dependency change, environment change, or governance change.
- model-drift evidence must be current, evidence-bounded behavior showing model/host execution deviation from the active AIR behavioral/runtime contract; suspicion alone does not set the flag true.
- `recovery_state` and AIR-error classification are independent dimensions and do not alter the truth table.

If alignment cannot complete, affected downstream construction is invalid and AIR emits AIR_ERROR when an AIR error is classified, or RT.UNCERTAINTY_RESOLVE / non-error recovery as appropriate.

