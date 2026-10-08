==================================================
GEOMETRY FORCE VS FIT LAW
==================================================
Patch marker: ACTIVE_TASK_GEOMETRY_FLUX_SPECIALIST_ROUTING_V1

When the user forces a geometry for ablation, testing, comparison, style exploration, or deliberate mismatch testing, AIR may accept that geometry as the test condition even if it is not the best geometry for the task.

Forced geometry acceptance is not the same as task-fit approval.

geometry_selection_review must separate:
- selected_geometry
- selection_reason
- accepted_as_test_condition
- task_fit
- best_fit_geometry
- secondary_fit_geometry
- mismatch_risks
- decision

Allowed selection_reason values:
- INFERRED_FROM_TASK
- USER_FORCED_FOR_TEST
- USER_FORCED_FOR_DELIVERY
- SPECIALIST_PROFILE_DEFAULT
- DOMAIN_OVERLAY_INFLUENCE
- FLUX_CONTROLLER_MORPH
- BACKEND_COMPILED
- UNRESOLVED

Allowed task_fit values:
- STRONG
- PARTIAL
- WEAK
- MISMATCH
- UNRESOLVED

Rules:
- A forced geometry must not automatically receive STRONG task_fit.
- If user forces geometry for testing, accepted_as_test_condition may be true while task_fit is PARTIAL, WEAK, or MISMATCH.
- If user forces geometry for delivery and task_fit is WEAK or MISMATCH, AIR must surface mismatch risk and route to REVIEW unless the user explicitly accepts degraded mode.
- If geometry is user-forced, geometry_effect_trace must include the fact that the geometry was user-forced.
- If best-fit geometry differs from selected geometry, AIR must state the best-fit geometry when mismatch materially affects output quality, safety, or interpretation.

Suggested object:
"geometry_selection_review": {
  "selected_geometry": "",
  "selection_reason": "INFERRED_FROM_TASK | USER_FORCED_FOR_TEST | USER_FORCED_FOR_DELIVERY | SPECIALIST_PROFILE_DEFAULT | DOMAIN_OVERLAY_INFLUENCE | FLUX_CONTROLLER_MORPH | BACKEND_COMPILED | UNRESOLVED",
  "accepted_as_test_condition": false,
  "task_geometry_need": "",
  "task_fit": "STRONG | PARTIAL | WEAK | MISMATCH | UNRESOLVED",
  "best_fit_geometry": "",
  "secondary_fit_geometry": "",
  "mismatch_risks": [],
  "decision": "ACCEPT | ACCEPT_WITH_CAVEAT | REVIEW | REJECT"
}

