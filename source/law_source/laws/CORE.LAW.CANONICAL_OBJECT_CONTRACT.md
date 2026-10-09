==================================================
CANONICAL AIR OBJECT CONTRACT LAW
==================================================

Patch marker: AIR_CANONICAL_OBJECT_CONTRACTS_V4
Patch marker: AIR_OBJECT_RESPONSIBILITY_CLOSURE_V1

Canonical formal object classes:
- AIR_RUNTIME_BRIDGE: STATE_TRANSITION_RECORD
- AIR_SESSION: SESSION_STATE_RECORD
- AIR_PROJECT_INITIALIZATION_BRIEF: PROJECT_STATE_RECORD
- AIR_PROJECT_EXECUTION_MAP: PROJECT_STATE_RECORD
- AIR_ARTIFACT: ACTIVE_EXECUTION_RECORD
- AIR_ACTIVE_CONTRACT: EXECUTION_CONTRACT
- AIR_GATE: DECISION_RECORD
- AIR_VALIDATION_REPORT: VALIDATION_RECORD
- AIR_ALIGNMENT_CHECK: ALIGNMENT_EVALUATION_RECORD
- AIR_ERROR: ERROR_RECORD
- AIR_ACTION_AUTHORIZATION: ACTION_AUTHORIZATION_RECORD
- AIR_ACTION_RECEIPT: ACTION_RECEIPT_RECORD
- AIR_SURFACED_OBJECT_LEDGER: SURFACED_OBJECT_LEDGER_RECORD
- AIR_FAILURE_MODE_RECORD: FAILURE_MODE_RECORD
- AIR_METHOD_EVIDENCE_WAIVER: METHOD_EVIDENCE_WAIVER_RECORD
- AIR_PRIOR_EFFECT_RECORD: RECOVERY_RECORD
- AIR_REQUIRED_INPUT_REQUEST: REQUIRED_INPUT_REQUEST_RECORD
- AIR_EVIDENCE_SOURCE_MANIFEST: EVIDENCE_SOURCE_MANIFEST_RECORD
- AIR_DEPENDENCY_RECORD: DEPENDENCY_RECORD
- AIR_HANDOFF_CARD: TRANSFER_RECORD

Object identity and record category:
- The top-level AIR object root name identifies semantic object identity.
- record_class identifies the semantic record category. It is not a unique object identifier and may be shared by multiple object types.
- evidence_class describes evidence strength only and never replaces object identity or record_class.

Common formal-object fields:
Every formal object must include, directly or through its defined root:
- object_version
- record_class
- runtime_origin
- backend_validation_claimed
- hidden_reasoning_claimed

Every formal object except AIR_ALIGNMENT_CHECK, its coupled alignment AIR_VALIDATION_REPORT, and an AIR_ERROR caused by alignment-evaluation failure must also include evaluation_basis under AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1.
evidence_class is allowed when material and must use the canonical evidence classes.

CLOSED-WORLD TOP-LEVEL FIELD LAW:
1. A formal object may contain only:
   - the common formal-object fields above;
   - the object-owned fields defined by its Core law;
   - fields explicitly registered as conditional for that same object by Core;
   - or a template-owned field for AIR_HANDOFF_CARD under the current Handoff schema.
2. A lower-precedence file may tighten conditions or populate an allowed field. It may not create a new top-level formal-object field, alias, parallel schema, or second owner without a Core amendment.
3. An unknown, aliased, foreign, or wrong-object top-level field makes the object INVALID_UNEMITTABLE and routes to AIR_ERROR with error_class OBJECT_SCHEMA_FIELD_OWNERSHIP_VIOLATION.
4. A reserved formal object label must never be embedded as if it were a field in another formal object. Cross-object linkage uses a *_ref field or the explicit AIR_HANDOFF_CARD transfer-snapshot exception.
5. Validators must reject extra top-level fields as well as missing mandatory fields.

SINGLE-OWNER STATE LAW:
Every mutable runtime fact has one canonical owning object. A non-owner may carry only one of:
- REFERENCE_ONLY: an explicit *_ref to the owning object/state;
- DERIVED_NONAUTHORITATIVE: a compact summary with its source ref and authoritative = false;
- IMMUTABLE_PROVENANCE_SNAPSHOT: a historical snapshot whose source object/ref and snapshot role are explicit;
- CONDITIONAL_OWNED: a field Core explicitly assigns to that object under a stated trigger.

A second full mutable copy is prohibited even when the values currently match. A non-owner copy cannot authorize execution, override its owner, repair staleness, or become current merely because it is newer in the conversation.

Governance-controlled source-rights records have one canonical owner: the Governance `governance_source_rights_state` record set keyed by source_rights_id. AIR_ARTIFACT.source_rights_state and AIR_HANDOFF_CARD.source_state.source_rights_state may carry only DERIVED_NONAUTHORITATIVE projections or references for those Governance-owned records. Every such projection must carry source_rights_id, governance_record_ref, authoritative = false, and projected_rights_state; it may not copy a second mutable permission record. Conflict, missing canonical reference, or disagreement between a projection and its Governance owner routes to REVIEW and cannot be resolved by last-writer-wins or consumer preference.

Canonical responsibility boundaries:
- AIR_RUNTIME_BRIDGE owns the onboarding-to-runtime transition record. Its onboarding/canonical-intent/context/source/specialist values are IMMUTABLE_PROVENANCE_SNAPSHOT after activation; current runtime authority moves to the emitted Session/Artifact state.
- AIR_SESSION owns session-global runtime/lifecycle/orbit/onboarding/visibility/alignment state. Task-level semantic, epistemic, and prior-effect carriers inside Session are DERIVED_NONAUTHORITATIVE summaries and must identify their Artifact or Recovery-record source refs when populated.
- AIR_PROJECT_INITIALIZATION_BRIEF owns first-activation orientation only. It does not own the roadmap, deep execution contract, task blockers, validation result, or test-run evidence.
- AIR_PROJECT_EXECUTION_MAP owns the project roadmap and project-level progression/readiness. It references the active Artifact and does not duplicate the Artifact execution contract or task-level evidence state.
- AIR_ARTIFACT owns current task execution state and is the sole active execution-binding object.
- AIR_ACTIVE_CONTRACT owns candidate contract-input terms only. It is never a parallel execution authority.
- AIR_GATE owns a decision about one proposed governed action/transition. It references Artifact/Contract state and must not copy their mutable contract or binding state wholesale.
- AIR_VALIDATION_REPORT owns validation target, basis, observations/checks, decision, limitations, and evidence references. It does not own plans, mutation scope, action authorization, task execution state, or roadmap state.
- AIR_ALIGNMENT_CHECK owns the compact projection of one Core alignment evaluation. Its coupled AIR_VALIDATION_REPORT owns the evaluation evidence/details.
- AIR_ERROR owns one surfaced error condition and safe recovery direction only.
- AIR_ACTION_AUTHORIZATION owns one single-use execution ticket after an ALLOW Gate. It references the Gate/Artifact/lease/scope/approval basis rather than re-evaluating them.
- AIR_ACTION_RECEIPT owns the post-attempt intended-versus-actual effect record and reconciliation evidence.
- AIR_SURFACED_OBJECT_LEDGER owns append-only evidence of canonical formal objects that were actually USER_VISIBLE_EMITTED; it cannot ledger merely constructed or inferred objects.
- AIR_FAILURE_MODE_RECORD owns one evidenced reusable failure mode, exact applicability signature/hash, corrective constraint, retest lifecycle, and recurrence state; it never supplies positive execution authority.
- AIR_METHOD_EVIDENCE_WAIVER owns one narrow exception to one Method step evidence_to_advance requirement. It never supplies action execution, Gate, approval, binding, or Orbit 0 authority. A waiver is permitted only when its typed scope/method/version/step/requirement/artifact match is exact, its permission basis resolves under the active Method Pack waiver contract, and validity_state is ACTIVE_CURRENT or APPLIED_RECORDED.
- AIR_PRIOR_EFFECT_RECORD owns recovery facts for an observed material effect that lacked valid current authorization/scope/lease at the time.
- AIR_REQUIRED_INPUT_REQUEST owns one exact unresolved input need and its acquisition/validation state.
- AIR_EVIDENCE_SOURCE_MANIFEST owns one durable typed manifest tying material evidence/claims to exact source identities, versions, hashes, collection/observation class, and validation references. Presentation mode never changes the underlying evidence set.
- AIR_DEPENDENCY_RECORD owns one durable first-class dependency/blocker relationship across task, project, source-contract, external capability, permission, or linked-bootstrap boundaries; it never grants positive execution authority.
- AIR_HANDOFF_CARD owns serialized transfer state. It may contain source-object snapshots only under the Handoff transfer-ownership contract; snapshots never restore as current execution authority.

AIR_RUNTIME_BRIDGE allowed object-owned top-level fields:
- bridge_version
- entry_path
- onboarding_answers
- answer_sources
- canonical_intent_state
- active_context_state
- base_continuity_mode
- neurodivergent_delivery_modifier
- user_alignment_state
- source_state
- specialist_selection_state
- blockers

AIR_SESSION allowed object-owned top-level fields:
- session_runtime_frame
- system_identity
- runtime_generation
- response_transaction_state when a bounded response transaction is active or resumable
- state_plane_registry
- persistent_state_lifecycle_registry
- contract_activation
- orbit_state
- task_binding
- compiler_contract
- artifact_presence
- object_visibility_mode
- object_visibility_authority_state
- profile_posture_acceptance_state
- load_integrity
- floor_invariant_registry
- onboarding_state
- governance_state
- specialist_binding_state
- runtime_alignment_state
- handoff_durability_state
- semantic_fidelity_state
- epistemic_sufficiency_state
- unbound_prior_effect_state
- creative_continuity_state when material
- q4d_delivery_state when material
- q6d_working_agreement when material

AIR_PROJECT_INITIALIZATION_BRIEF allowed object-owned top-level fields:
- brief_id
- project_started
- project_phase
- runtime_mode
- artifact_first_reason
- expected_artifact_classes
- next_active_step
- next_task_state
- evidence_posture

AIR_PROJECT_EXECUTION_MAP allowed object-owned top-level fields:
- map_id
- project_phase
- project_status
- artifact_presence
- current_active_step
- current_active_step_artifact_ref
- critical_path
- completed_steps
- upcoming_steps
- project_blockers
- next_task_state
- recommended_attachments
- evidence_milestones
- next_best_step
- completion_definition
- readiness when material
- milestone_readiness when material
- public_release_state when target readiness is AMRS-5 or AMRS-6
- validation_architecture_state when staged validation is material

AIR_ARTIFACT base allowed object-owned top-level fields:
- artifact_id
- artifact_revision
- artifact_binding_state
- artifact_lease
- action_governance_state
- supersedes_artifact_id when applicable
- orbit_level when queued or active
- queue_state when queued or paused
- task_key
- task_center
- active_step
- execution_contract
- execution_steering when the task is executable
- source_contract_refs
- governing_floor_invariants
- semantic_fidelity_contract
- epistemic_sufficiency_state
- mii_cognitive_lattice
- mii_fusion_state
- morphology_binding
- execution_benchmark_profile
- capability_clusters when vector compilation is material
- missing_vectors when vector compilation is material
- degraded_execution_mode when execution is materially degraded
- dependency_edges when execution dependencies are material
- vector_family_state_summary when vector-family state is material
- objective when coding/implementation formation is material
- selected_vectors
- obligations
- blockers
- assumptions_made
- uncertainty_or_degraded
- method
- method_execution_state when material
- method_handoff_state when material
- verification_specification when material
- specification_adequacy_state when material
- source_state
- active_contract_ref
- receiver_delivery_state
- resource_scope_pin when material action is possible
- implementation_notes_for_executor when coding is material
- architectural_invariants when coding is material
- security_checks when coding is material
- test_requirements when coding is material
- review_obligations when coding is material
- rejection_conditions when coding is material
- readiness_stage when coding/readiness is material
- target_readiness_stage when coding/readiness is material
- target_readiness_basis when coding/readiness is material
- readiness_gap when coding/readiness is material
- completion_readiness_state when coding/readiness is material
- readiness_reason when coding/readiness is material
- stage_constraints when coding/readiness is material
- promotion_requirements when coding/readiness is material
- blocked_capabilities when coding/readiness is material
- decision_state when coding/readiness review is material
- behavior_specification when behavior-bearing implementation is material
- active_task_geometry when morphology geometry is material
- geometry_effect_state when morphology geometry is material
- geometry_effect_trace when morphology geometry is material
- active_task_lambda_pressure when lambda pressure is material
- lambda_pressure_binding when lambda pressure is material
- profile_stack when Specialist/domain routing affects the task
- specialist_integrity_check when Specialist/domain routing affects the task
- specialist_recommendation when Specialist/domain routing affects the task
- domain_package_recommendation when Specialist/domain routing affects the task
- creative_continuity_state when creative continuity affects the task
- q4d_delivery_state when Q4D affects execution
- q6d_working_agreement when Q6D affects execution
- familiar_artifact_preservation when material
- small_step_surface when material
- voice_to_text_ambiguity_check when consequential VTT ambiguity exists
- task_source_references when source dependency is material
- source_evidence_boundary when source dependency is material
- claim_classification when source dependency is material
- patch_source_inventory when file mutation is material
- source_hashes when file mutation is material
- replacement_policy when file mutation is material
- mutation_scope when file mutation is material
- validation_plan when file mutation is material
- delivery_receipt_refs when file mutation is material
- governance_state when governance affects execution
- source_rights_state when governance affects execution
- framework_projection_state when governance affects execution
- test_evidence_requirements when testing/evidence affects execution
- prompt_layer_qualitative_trace when prompt-layer qualitative native checks materially affect the active step; mandatory when prompt AIR references backend-inspired native behavior
- evidence_source_manifest_ref when material evidence/source provenance governs the active step
- dependency_record_refs when durable dependencies govern the active step

AIR_ACTIVE_CONTRACT allowed object-owned top-level fields:
- contract_id
- contract_version
- authority_level
- task_center
- goal
- scope
- out_of_scope
- allowed_actions
- excluded_actions
- stop_conditions
- required_evidence_to_close
- rescope_protocol
- approval_scope
- decision_state
- receiver_delivery_state
- source_set
- compilation_state

AIR_GATE allowed object-owned top-level fields:
- gate_id
- exact_gate_question
- requested_action
- gate_context
- active_artifact_ref when gate_context = ACTIVE_ARTIFACT_ACTION
- candidate_artifact_ref when gate_context = CANDIDATE_BINDING_TRANSITION
- approval_scope_ref when approval is material
- decision_package_ref when approval is material
- decision_package_sha256 when approval is material
- active_contract_ref when material
- evaluation_checks
- required_evidence
- blocking_conditions
- decision
- reason
- safe_next_action

AIR_VALIDATION_REPORT allowed object-owned top-level fields:
- report_id
- validated_target
- validation_basis
- checks
- decision
- limitations
- source_or_tool_evidence
- observed_identity when validating file/package identity
- evaluation_id when coupled to RT.ALIGN
- evaluation_profile when coupled to RT.ALIGN
- state_epoch when coupled to RT.ALIGN
- evaluated_dimensions when coupled to RT.ALIGN
- test_evidence_observations when test/audit evidence is the validation target

AIR_ALIGNMENT_CHECK allowed object-owned top-level fields:
- check_id
- evaluation_id
- evaluation_profile
- state_epoch
- post_activation_user_message_count
- evaluated_state_refs
- drift_detected
- alignment_state
- recovery_state
- validation_report_ref

AIR_ERROR allowed object-owned top-level fields:
- error_id
- error_class
- affected_object_or_file
- blocking
- reason
- safe_next_action
- recoverable

AIR_ACTION_AUTHORIZATION allowed object-owned top-level fields:
- authorization_id
- action_id
- action_class
- requested_action
- controlling_artifact_ref
- target
- gate_ref
- approval_basis_or_ref
- approval_scope_ref when approval is material
- approval_scope_fingerprint when approval is material
- decision_package_sha256 when approval is material
- consumption_key_sha256 when approval is material
- resource_scope_pin_ref
- expected_effect
- receipt_evidence_required
- authorization_invalidators
- single_use
- consumption_state
- decision

AIR_ACTION_RECEIPT allowed object-owned top-level fields:
- receipt_id
- authorization_ref
- action_id
- intended_target
- actual_target
- execution_evidence
- result
- effect_ids
- state_comparison
- unexpected_side_effects
- validation_result
- artifact_lease_effect
- required_state_updates
- recovery_required

AIR_SURFACED_OBJECT_LEDGER allowed object-owned top-level fields:
- ledger_id
- previous_ledger_hash
- response_message_count
- state_epoch
- entries
- ledger_hash

AIR_FAILURE_MODE_RECORD allowed object-owned top-level fields:
- failure_mode_id
- originating_task_ref
- originating_attempt_id
- failure_class
- failed_step_or_route
- expected_behavior
- observed_behavior
- trigger_conditions
- root_cause_state
- root_cause_basis
- invalidated_assumption_or_strategy
- prohibited_retry_pattern
- corrective_constraint
- applicability_signature
- applicability_signature_hash
- applicability_state
- affected_task_classes
- specialist_or_method_refs
- retest_requirement
- retest_state
- lifecycle_state
- recurrence_count
- superseded_by
- evidence_refs
- source_ledger_entry_ref

AIR_METHOD_EVIDENCE_WAIVER allowed object-owned top-level fields:
- waiver_id
- method_identity
- method_version
- step_id
- waived_requirement
- waiver_scope
- artifact_scope_ref
- permission_basis_type
- permission_basis_ref
- reason
- issued_state_epoch
- validity_state
- applied_state
- evidence_refs
- claim_boundary

AIR_METHOD_EVIDENCE_WAIVER validation law:
- waiver_scope must equal METHOD_STEP_EVIDENCE_TO_ADVANCE_ONLY.
- method_identity, method_version, step_id, waived_requirement, and artifact_scope_ref must exactly match the active Method execution and the one missing evidence_to_advance requirement.
- permission_basis_type must be explicitly allowed by the active Method Pack evidence_waiver_contract. EXPLICIT_USER_APPROVAL requires a resolvable user-visible permission_basis_ref; free text, generic approval state, model judgment, or inferred intent is insufficient.
- validity_state is ACTIVE_CURRENT, APPLIED_RECORDED, REVOKED, or EXPIRED. Only ACTIVE_CURRENT or APPLIED_RECORDED may support the exact completion whose basis they record.
- applied_state records whether the exact waiver has been consumed as completion basis; it does not grant execution authority and remains historical evidence after application.
- AIR_METHOD_EVIDENCE_WAIVER must be canonically emitted/ledgered before it may be referenced for completion or Handoff. Restored references remain non-authorizing bootstrap input until current validation.

AIR_PRIOR_EFFECT_RECORD allowed object-owned top-level fields:
- prior_effect_id
- discovered_effect
- observed_target
- effect_evidence
- authorization_state_at_effect
- scope_match_state_at_effect
- lease_state_at_effect
- affected_artifact_ref
- risk_state
- rollback_feasibility
- reconciliation_state
- human_review_requirement
- safe_next_action
- retroactive_authorization_forbidden

AIR_REQUIRED_INPUT_REQUEST allowed object-owned top-level fields are exactly the canonical minimum schema in Required Input and Artifact Acquisition Law.
AIR_HANDOFF_CARD allowed top-level fields are exactly those declared by its current template schema; current-card transfer duplication must satisfy the Handoff transfer_ownership_contract.

Canonical AIR_ACTIVE_CONTRACT vocabulary is identical to AIR_ARTIFACT.execution_contract vocabulary for overlapping terms. The deprecated aliases scope_in, scope_out, prohibited_actions, required_evidence, rescope_rule, and binding_state are not valid current AIR_ACTIVE_CONTRACT fields.

Formal-object root labels such as AIR_ACTION_AUTHORIZATION, AIR_ACTION_RECEIPT, AIR_PRIOR_EFFECT_RECORD, AIR_GATE, AIR_ARTIFACT, or AIR_VALIDATION_REPORT are objects, not fields. Another object may carry only their explicit *_ref or a Handoff transfer snapshot.

