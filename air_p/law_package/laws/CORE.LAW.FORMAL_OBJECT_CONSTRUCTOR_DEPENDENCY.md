==================================================
FORMAL OBJECT CONSTRUCTOR DEPENDENCY LAW
==================================================

Patch marker: AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1
Floor invariants: AIR-FLOOR-007 and AIR-FLOOR-021

Every formal AIR object except the root alignment projections and an AIR_ERROR caused by alignment-evaluation failure requires a current evaluation_basis:
- evaluation_id
- evaluation_profile
- state_epoch
- alignment_check_ref
- validation_report_ref
- dependency_state = SATISFIED

The evaluation basis must match the state from which the object is constructed. Multiple objects constructed from one unchanged canonical state may share one evaluation basis. A material state transition, external effect, artifact revision, approval/scope change, source-state change, or other dependency invalidation makes the prior basis stale for post-change state-dependent objects.

Strict AIR_HANDOFF_CARD output is a serialization exception only. Required dependencies still execute; the card carries the relevant evaluation provenance within its single root instead of emitting additional roots.

Constructor hardening requirements:
- `AIR_ALIGNMENT_CHECK.drift_detected` must be JSON boolean; string/number/null/enum substitutes are invalid.
- `AIR_ALIGNMENT_CHECK.alignment_state` is limited to ALIGNED | RECONCILIATION_REQUIRED | DRIFT_DETECTED and must satisfy the model-drift truth table.
- `drift_detected = true` without current model-drift evidence is INVALID_UNEMITTABLE.
- an effective scope transition is constructor-incomplete unless AIR_SESSION, AIR_PROJECT_EXECUTION_MAP, and AIR_ARTIFACT are all present in the same required visibility transaction.
- a genuinely new task is constructor/lifecycle-incomplete if it reuses the prior task Artifact identity or omits the inception AIR_ARTIFACT.
- an AIR-classified error is constructor/emission-incomplete unless AIR_ERROR is generated and owed by response closure.
- formal-object transaction state must progress CONSTRUCTED_CANDIDATE -> VALIDATED_EMITTABLE -> USER_VISIBLE_EMITTED -> LEDGER_COMMITTED; COMMITTED semantics before validation/emission are prohibited.

