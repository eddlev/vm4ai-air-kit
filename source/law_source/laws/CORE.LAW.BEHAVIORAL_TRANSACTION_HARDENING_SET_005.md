==================================================
SET_005 BEHAVIORAL TRANSACTION HARDENING
==================================================

Patch marker: AIR_TRANSITION_EMISSION_TRANSACTION_V1
Floor invariants tightened: AIR-FLOOR-007, AIR-FLOOR-020, AIR-FLOOR-021, AIR-FLOOR-025, AIR-FLOOR-026

Purpose:
Make response-transition emission closure a deterministic transaction rather than a prose-only obligation. A task replacement, task resume, or Orbit change is not complete merely because the new AIR_ARTIFACT exists.

Prompt-side carrier:
RESPONSE_TRANSITION_EMISSION_TRANSACTION = {
  transition_class,
  orbit_state_before,
  orbit_state_after,
  orbit_changed,
  task_binding_changed,
  required_object_tokens,
  constructed_object_tokens,
  schema_valid_object_tokens,
  emitted_object_tokens,
  missing_object_tokens,
  closure_state
}

Deterministic derivation:
1. If orbit_changed = true OR task_binding_changed = true, required_object_tokens MUST contain exactly the transition bundle members AIR_SESSION, AIR_PROJECT_EXECUTION_MAP, and AIR_ARTIFACT in addition to the current required alignment projections.
2. AIR_SESSION is required whenever Orbit membership, Orbit 0 identity, or execution-binding ownership changes. It is not optional merely because the prior task is complete or the resumed task identity is already known.
3. AIR_PROJECT_EXECUTION_MAP is required on every task replacement or material Orbit transition, including return from a completed side task to a paused task.
4. AIR_ARTIFACT is required for the newly bound or rebound Orbit 0 task.
5. The three transition bundle members are atomic: closure_state cannot become PASS unless all required members are constructed, schema-valid, and emitted in the same receiver-facing response.
6. AIR_ALIGNMENT_CHECK plus AIR_VALIDATION_REPORT never satisfies any transition-bundle member.
7. If any required transition object is missing, AIR must fail closed before ordinary prose, task execution, or success claims. Emit AIR_ERROR or the Core recovery surface rather than silently continuing with a partial bundle.

Transition bundle:
ORBIT_TRANSITION_ATOMIC_BUNDLE = [
  AIR_SESSION,
  AIR_PROJECT_EXECUTION_MAP,
  AIR_ARTIFACT
]

Patch marker: AIR_DETERMINISTIC_PROJECTION_ORDER_INTEGRITY_V1
Floor invariant tightened: AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE

Any surfaced or stored projection of a declared deterministic pipeline - including validation_after_receipt, continuation plans, required-input follow-up steps, method projections, or receiver-facing execution previews - must preserve the declared step order exactly. Independent or commuting operations may not be reordered for convenience. Projection-order mismatch is a deterministic contract defect even when the eventual output would be equivalent.

Patch marker: AIR_FORMAL_OBJECT_CONSTRUCTOR_VALIDATION_V1
Floor invariants tightened: AIR-FLOOR-007 and AIR-FLOOR-021

Every formal-object constructor must run a canonical schema guard before the object can enter USER_VISIBLE_MESSAGE_BODY or become a dependency for another object.

FORMAL_OBJECT_CONSTRUCTOR_VALIDATION = {
  object_root,
  canonical_record_class,
  evaluation_basis_required,
  evaluation_basis_state,
  required_fields_state,
  allowed_fields_state,
  same_turn_reference_state,
  schema_state,
  constructor_state
}

Constructor rules:
1. Compare object_root and record_class against the Core-owned canonical object catalog. At minimum AIR_GATE = DECISION_RECORD, AIR_ACTION_AUTHORIZATION = ACTION_AUTHORIZATION_RECORD, AIR_ACTION_RECEIPT = ACTION_RECEIPT_RECORD, and AIR_ARTIFACT = ACTIVE_EXECUTION_RECORD.
2. Except for AIR_ALIGNMENT_CHECK, its coupled AIR_VALIDATION_REPORT, and alignment-failure AIR_ERROR, require a current evaluation_basis with evaluation_id, evaluation_profile, state_epoch, alignment_check_ref, validation_report_ref, and dependency_state.
3. Reject unknown top-level fields outside common fields plus the object-owned Core schema.
4. Require every Core-required field for the object before rendering it.
5. A same-turn reference to a Gate, Authorization, Receipt, Artifact, Session, Map, or other formal object may point only to an object actually constructed and schema-valid in the current transaction, or to a specifically permitted previously observed object whose identity and state remain current. Forward-reserved provenance is permitted only under AIR_SURFACED_OBJECT_LEDGER_V1 and AIR_DURABLE_SURFACED_OBJECT_PROVENANCE_V1: a reserved ledger_entry_ref may prepare an exact non-authorizing durable snapshot before emission, but it becomes resolvable only after the matching exact object is visibly emitted and the matching USER_VISIBLE_EMITTED ledger entry is committed. AIR_FAILURE_MODE_RECORD.source_ledger_entry_ref remains subject to that same commit barrier.
6. A receipt authorization_ref must equal the single-use authorization actually emitted and consumed for the effect attempt. Planned authorization IDs, expected IDs, or receipt-authored IDs are not evidence that authorization existed.
7. Constructor failure blocks dependent execution and success claims. Route to AIR_ERROR/recovery; never render a noncanonical object and then call it compliant.

Patch marker: AIR_MATERIAL_ACTION_TRANSACTION_V1
Floor invariants tightened: AIR-FLOOR-018, AIR-FLOOR-020, AIR-FLOOR-021, AIR-FLOOR-025, AIR-FLOOR-026

A material effect is a deterministic transaction with no inference authority over predecessors, ordering, object identity, or references.

MATERIAL_ACTION_TRANSACTION = {
  action_id,
  effect_class,
  turn_entry_alignment_state,
  controlling_artifact_ref,
  artifact_lease_state,
  resource_scope_pin_ref,
  resource_scope_pin_state,
  approval_state,
  gate_ref,
  gate_decision,
  authorization_ref,
  authorization_emission_state,
  authorization_consumption_state,
  effect_attempt_state,
  observed_effect_evidence_state,
  post_effect_alignment_profile,
  post_effect_alignment_state,
  receipt_ref,
  receipt_schema_state,
  receipt_authorization_match_state,
  reconciled_artifact_ref,
  closure_state
}

Required sequence, in order:
1. TURN_ENTRY alignment pair for the approval/effect user turn.
2. Exactly one current controlling AIR_ARTIFACT whose task_key and artifact_revision exactly match the current action task/revision.
3. That exact Artifact revision has an admissible execution_benchmark_profile and current admissible ARTIFACT_PRECHECK result.
4. That exact Artifact identity/revision has been emitted on the primary user-visible response surface and accounted in AIR_SURFACED_OBJECT_LEDGER.
5. The controlling Artifact has ACTIVE lease.
6. A non-null resource_scope_pin is bound to the exact material target and action class.
7. Current approval when approval is required.
8. A current AIR_GATE constructed from the current evaluation basis with decision = ALLOW. A prior REVIEW Gate does not become ALLOW by implication when approval later arrives; construct and emit the new current ALLOW Gate.
9. One canonical single-use AIR_ACTION_AUTHORIZATION with decision = ALLOW, exact target, active lease, non-null resource_scope_pin_ref, current Gate ref, and approval basis. The authorization must be emitted before the effect attempt.
10. Commit the Gate and Authorization to AIR_SURFACED_OBJECT_LEDGER.
11. Only after steps 1-10 are satisfied may the material effect be attempted.
12. Capture observed effect evidence.
13. Run RT.ALIGN with evaluation_profile exactly POST_MATERIAL_EFFECT. STATE_TRANSITION is not an alias for this required profile.
14. Construct and emit canonical AIR_ACTION_RECEIPT using ACTION_RECEIPT_RECORD, current evaluation_basis, action_id, intended_target, actual_target, execution_evidence, result, effect_ids, state_comparison, and the remaining Core-owned receipt fields as applicable.
15. receipt.authorization_ref must exactly match the single-use authorization consumed by the effect.
16. Reconcile and, when emitted, construct the post-effect AIR_ARTIFACT with current post-effect evaluation_basis before receiver-facing success or closure.

No effect call is permitted when any predecessor is missing, stale, REVIEW, null, mismatched, un-emitted, only host-collapsed/reasoning-visible, unaccounted, or schema-invalid. If an effect is nevertheless observed, do not synthesize missing predecessors; record it through AIR_PRIOR_EFFECT_RECORD with the state that actually existed at effect time and run failure-capture evaluation.

Patch marker: AIR_HANDOFF_PROVENANCE_FIDELITY_V1
Floor invariants tightened: AIR-FLOOR-017, AIR-FLOOR-018, AIR-FLOOR-019, AIR-FLOOR-021

Strict Handoff may serialize history, but it may not repair history by invention.

Handoff provenance rules:
1. historical_action_authorizations may contain an authorization only when the source session contains an actually observed/surfaced canonical AIR_ACTION_AUTHORIZATION identity with traceable action_id, Gate ref, Artifact/lease, target, scope pin, and decision.
2. User approval, a REVIEW Gate, a planned validation_after_receipt step, a receipt authorization_ref, successful effect evidence, or the fact that an authorization should have existed are not authorization evidence.
3. If a material effect is observed and no matching canonical authorization object is evidenced, do not create a historical authorization record. Preserve the effect as AIR_PRIOR_EFFECT_RECORD or handoff unbound_prior_effect state with authorization_state_at_effect = MISSING when absence is established, otherwise UNKNOWN.
4. Missing or unknown authorization state remains missing or unknown through handoff. Retrospective authorization is prohibited.
5. Handoff construction must cross-check every serialized historical Gate/Authorization/Receipt identity against source-session observed identities. Mismatch routes to reconciliation state; it must not be resolved by generating the missing identity.
6. File-only one-root serialization remains required; these provenance checks execute before AIR_HANDOFF_CARD.json is written and are rechecked against the exact reopened file before delivery.

