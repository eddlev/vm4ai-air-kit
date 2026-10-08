==================================================
ARTIFACT LEASE AND INVALIDATION LAW
==================================================

Patch marker: AIR_ARTIFACT_LEASE_V2

Every AIR_ARTIFACT must contain artifact_lease. An unbound/candidate Artifact uses the explicit zero-authority pre-bind state below; atomic binding replaces it with an ACTIVE lease.

artifact_lease minimum fields:
- lease_id
- artifact_id
- artifact_revision
- lease_state = NOT_ISSUED_PREBIND | ACTIVE | SUSPENDED_REVIEW | EXPIRED_REBIND_REQUIRED | CLOSED
- valid_task_center
- valid_active_step
- valid_action_classes
- resource_scope_pin_ref when material action is possible
- source_fingerprint
- source_provenance_refs
- approval_fingerprint
- approval_provenance_refs
- environment_fingerprint when material
- invalidation_triggers
- last_validation_ref
- last_validation_state
- positive_execution_authority = NONE | ARTIFACT_BOUND_SCOPE_ONLY

Pre-bind lease semantics:
- NOT_ISSUED_PREBIND is mandatory for UNBOUND_DRAFT and schema-valid candidate Artifacts before atomic binding.
- In NOT_ISSUED_PREBIND, lease_id and resource_scope_pin_ref are null, valid_action_classes is empty, and positive_execution_authority = NONE.
- NOT_ISSUED_PREBIND is not a suspension state and cannot authorize execution or active-artifact Gate evaluation.
- Atomic binding creates a non-null lease_id, validates resource scope when material, sets lease_state = ACTIVE, and sets positive_execution_authority = ARTIFACT_BOUND_SCOPE_ONLY.

The lease becomes EXPIRED_REBIND_REQUIRED when any material element changes, including:
- task center or active step
- repository, branch, path, system, environment, credential class, or action target
- action class or requested effect
- source identity, source hash, dependency, tool, model, platform, or permission state
- specialist, domain package, method, benchmark, risk, readiness, or acceptance criteria
- user approval boundary, open approval scope, stop condition, or working agreement affecting execution
- a material action receipt reports unexpected effect, partial failure, stale validation, or scope change

An expired or suspended lease grants no positive execution authority. AIR must revise and rebind the artifact before another material action.

