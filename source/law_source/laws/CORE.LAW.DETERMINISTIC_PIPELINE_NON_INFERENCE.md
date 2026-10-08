==================================================
DETERMINISTIC PIPELINE NON-INFERENCE LAW
==================================================

Patch marker: AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1
Floor invariant: AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE

Core principle:
When a Core-owned route or pipeline is explicitly classified as DETERMINISTIC_PIPELINE, AIR must follow the declared pipeline exactly. Deterministic pipeline state is not a cognitive completion task.

Rules:
1. inference_policy = PROHIBITED for undeclared or unresolved deterministic slots.
2. AIR must not infer, interpolate, repair, substitute, reorder, skip, widen, narrow, optimize, or silently default a deterministic pipeline input, condition, transition, output, or pass/fail criterion.
3. Missing, ambiguous, conflicting, invalid, or unavailable required deterministic state routes to FAIL_CLOSED or the smallest exact AIR_REQUIRED_INPUT_REQUEST defined by the pipeline.
4. A router or classifier may resolve whether a declared condition is satisfied when the condition definition permits classification; it may not invent the consequence. Once a deterministic route is selected, the declared table/pipeline owns the consequence.
5. MII, Specialists, translators, methods, heuristics, remembered context, historical state, and contextual likelihood cannot fill deterministic pipeline slots unless the deterministic pipeline explicitly declares an invocation step, input/output schema, validation rule, and acceptance boundary for that contribution.
6. Cognitive output must not contaminate deterministic control state. A cognitive result becomes usable inside a deterministic pipeline only at an explicit declared ingestion step after validation.
7. step_order = STRICT unless the pipeline itself declares a different deterministic partial order.
8. unknown_condition_behavior, missing_input_behavior, and conflict_behavior default to FAIL_CLOSED for deterministic pipelines.
9. A deterministic pipeline may not downgrade itself to a cognitive/advisory path merely to continue execution.

Canonical deterministic runtime route set for this Foundation candidate:
- RT.BOOT
- RT.ONBOARD
- RT.HANDOFF_RESTORE
- RT.TURN
- RT.ALIGN
- RT.TASK_SWITCH
- RT.APPROVAL_RESOLVE
- RT.ACTION
- RT.RECEIPT
- RT.HANDOFF_CREATE

The route set is explicit and closed for this candidate. Routes not listed above are not made deterministic by analogy.

