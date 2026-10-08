==================================================
CLOSED-WORLD FORMAL OBJECT EMISSION CLOSURE LAW
==================================================

Patch marker: AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1
Floor invariants tightened: AIR-FLOOR-001, AIR-FLOOR-007, AIR-FLOOR-020, AIR-FLOOR-021

Purpose:
Convert distributed formal-object visibility law into one fail-closed per-response condition so a prompt runtime cannot satisfy a highly salient object pair while silently dropping other objects owed by the same route/state transition.

Core-owned response carrier:
RESPONSE_EMISSION_CLOSURE = {
  required_visible_objects,
  generated_formal_objects_for_response,
  schema_valid_generated_objects,
  emitted_visible_objects,
  object_visibility_mode,
  runtime_anchor_required,
  runtime_anchor_count,
  strict_handoff_one_root,
  closure_state
}

Required-visible-object set construction:
- Start with every object explicitly required by the selected Core route and current lifecycle/state transition.
- After ARTIFACT_BOUND_EXECUTION, add AIR_ALIGNMENT_CHECK and its coupled AIR_VALIDATION_REPORT for every substantive governed response including handoff delivery responses.
- FIRST_ACTIVATION under RT.ACTIVATE adds AIR_RUNTIME_BRIDGE, AIR_SESSION, AIR_PROJECT_INITIALIZATION_BRIEF, AIR_PROJECT_EXECUTION_MAP, and the current active-step AIR_ARTIFACT.
- MATERIAL_ARTIFACT_AMENDMENT adds the revised AIR_ARTIFACT and adds AIR_PROJECT_EXECUTION_MAP when roadmap, active step, blocker, or project progression state changed materially. EFFECTIVE_SCOPE_TRANSITION additionally and unconditionally adds AIR_SESSION so AIR_SESSION + AIR_PROJECT_EXECUTION_MAP + AIR_ARTIFACT are owed together.
- NEW_TASK_INCEPTION adds the distinct UNBOUND_DRAFT AIR_ARTIFACT before precheck/binding. TASK_OR_STEP_REPLACEMENT or material Orbit transition later adds AIR_SESSION, AIR_PROJECT_EXECUTION_MAP, and the bound AIR_ARTIFACT as the atomic binding bundle.
- A material AIR_GATE decision adds AIR_GATE; an allowed material action adds AIR_ACTION_AUTHORIZATION before the effect; every attempted material action adds AIR_ACTION_RECEIPT after POST_MATERIAL_EFFECT alignment/reconciliation.
- Material unresolved-input routing adds AIR_REQUIRED_INPUT_REQUEST when that branch is selected.
- Recovery runs AIR-error classification first. AIR_ERROR_CLASSIFIED requires AIR_ERROR; NON_ERROR_RECOVERY prohibits fabricated AIR_ERROR and adds only the applicable Core-defined recovery record.
- Explicit formal-object requests add the requested canonical object when lawful and constructible.
- RT.HANDOFF_CREATE never inlines AIR_HANDOFF_CARD. It writes the one-root card to AIR_HANDOFF_CARD.json, reopens and strictly validates the exact file bytes, then delivers only the downloadable file plus ordinary governed chat records and a file delivery receipt.

Closed-world pass condition:
1. required_visible_objects is a subset of schema_valid_generated_objects.
2. required_visible_objects is a subset of emitted_visible_objects in USER_VISIBLE_MESSAGE_BODY.
3. Under ALL_OBJECTS, every formal object generated for the visible response is emitted; optional repetition may be suppressed only under MINIMUM_REQUIRED_OBJECTS.
4. If runtime_anchor_required = true, runtime_anchor_count must equal 1.
5. No prose claim may substitute for an owed formal object.
6. AIR_ALIGNMENT_CHECK plus AIR_VALIDATION_REPORT satisfaction does not imply satisfaction of any other owed object.

Failure behavior:
- If any required object cannot be constructed, schema-validated, or visibly emitted, closure_state = FAIL.
- On FAIL, suppress ordinary/default-host continuation and receiver-facing narrative that depends on the missing state.
- Emit the narrow applicable AIR_ERROR/recovery surface or Strict Handoff failure path and preserve the unsatisfied obligation for the next lawful state transition.
- A later correction records the prior miss but does not retroactively make the earlier response compliant.

Ownership boundary:
Core computes RESPONSE_EMISSION_CLOSURE. Control renders it and may not remove, add, reinterpret, or reprioritize semantic obligations. Starter may mirror the requirement as a bootstrap default but may not redefine it.

