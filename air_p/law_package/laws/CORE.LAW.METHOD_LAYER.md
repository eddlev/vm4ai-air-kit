==================================================
AIR METHOD LAYER LAW
==================================================

Patch marker: AIR_METHOD_LAYER_V2

A task-local method lives in AIR_ARTIFACT.method. Creating or promoting a new reusable method into an AIR_METHOD_PACK requires explicit promotion approval. Selecting an already-existing validated AIR_METHOD_PACK is a separate capability-selection decision and may be appropriate even for a one-off task when specification dependence, consequence, evidence pressure, verification difficulty, downstream dependency, or portability needs justify it.

Task-local method minimum fields:
- method_id
- purpose
- inputs
- outputs
- ordered_steps
- evidence_to_close
- failure_behavior
- handoff_fields

AIR_METHOD_PACK minimum fields:
- SYSTEM_DESIGNATION
- PROMPT_VERSION
- PROFILE_KIND = METHOD_PACK
- method_id
- purpose
- scope
- inputs
- outputs
- dependencies
- ordered_steps
- staleness_policy
- handoff_requirements
- binding_requirements

Each method step must include:
- step_id
- name
- action
- preconditions
- required_inputs
- expected_outputs
- evidence_to_advance
- failure_behavior
- next_step_rule

Method execution state values:
- NOT_STARTED
- IN_PROGRESS
- BLOCKED
- REVIEW
- COMPLETE
- FAILED
- INVALIDATED
- STALE_NEEDS_REGROUND

Method step state values:
- PENDING
- ACTIVE
- COMPLETE
- BLOCKED
- REVIEW
- SKIPPED_APPROVED
- FAILED
- INVALIDATED

EVIDENCE_REQUIRED and RESCOPE_REQUIRED are gate decisions, not method-step states.

method_step_gate decision values:
- ALLOW
- REVIEW
- EVIDENCE_REQUIRED
- REJECT
- RESCOPE_REQUIRED
- BLOCKED_BY_CONTRACT
- BLOCKED_BY_STALENESS

AIR_GATE controls material task action and is stricter when the two gates conflict.

Generic method continuation carrier:
When method state materially affects continuation, AIR_ARTIFACT and AIR_HANDOFF_CARD must preserve a `method_handoff_state` with:
- method_identity
- method_origin = INLINE | METHOD_PACK
- method_version when applicable
- active_method_state
- active_method_step
- method_step_gate
- method_evidence_state
- staleness_state
- unresolved_blockers
- next_allowed_action
- evidence_refs
- method_specific_state_schema_ref when method_origin = METHOD_PACK
- method_specific_state_schema_version when method_origin = METHOD_PACK
- method_specific_state

For METHOD_PACK origin, method_specific_state_schema_ref must exactly equal the active Method Pack's declared handoff_requirements.method_specific_state_schema.schema_id and the serialized state must validate against that typed schema. A prose-only requirement list is not sufficient for restoration. INLINE methods may leave the schema reference null when no separate typed method-specific contract exists.

`method_specific_state` contains only method-defined continuation state that is not already canonically owned elsewhere in AIR. It must not duplicate task center, execution-contract goal/scope, benchmark acceptance criteria, approval authority, or observed evidence as a second source of truth.
When a Method Pack declares handoff requirements, its `method_specific_state` must satisfy those requirements before restoration may continue. Missing material method state routes to REVIEW; AIR must not reconstruct it from guesswork.

A step cannot become COMPLETE without its evidence_to_advance unless an exact AIR_METHOD_EVIDENCE_WAIVER is canonically recorded and validates for that method/version/step/requirement/artifact scope under the active Method Pack waiver contract. Free text, generic approval, inferred permission, or reconstructed Handoff state cannot satisfy the exception. Written instructions alone do not prove execution. Promotion to a Method Pack requires explicit user approval and evidence of recurrence, low-variance need, portability need, reusable assets, or defect history.

