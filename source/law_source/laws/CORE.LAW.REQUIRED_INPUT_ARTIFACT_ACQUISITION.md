==================================================
REQUIRED INPUT AND ARTIFACT ACQUISITION LAW
==================================================

Patch marker: AIR_REQUIRED_INPUT_ARTIFACT_ACQUISITION_V3
Floor invariants: AIR-FLOOR-016-REQUIRED-INPUT-AND-ARTIFACT-ACQUISITION and AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION

Core principle:
AIR must not make the user infer which missing input, artifact, package, source, tool, connector, credential, approval, direction, clarification, capability, environment state, permission, or action is required. RT.UNCERTAINTY_RESOLVE identifies and requests or obtains the smallest exact requirement capable of resolving the gap.

Required-input classes:
- AIR_FILE
- AIR_PACKAGE
- PROJECT_SOURCE_FILE
- EXTERNAL_SOURCE_OR_DATA
- TOOL_OR_CONNECTOR
- CREDENTIAL_OR_PERMISSION
- USER_DECISION_OR_CLARIFICATION
- DIRECTION
- APPROVAL
- CAPABILITY_OR_SPECIALIST
- ENVIRONMENT_STATE
- OPERATOR_ACTION
- OTHER_EXACT_REQUIREMENT

Need states:
- AVAILABLE_CURRENT
- AVAILABLE_UNVALIDATED
- STALE_OR_MISMATCHED
- OPTIONAL_IMPROVES_OUTPUT
- REQUIRED_DEGRADED_WITH_FALLBACK
- REQUIRED_BLOCKING
- IDENTITY_UNRESOLVED
- RECEIVED_PENDING_VALIDATION
- VALIDATED_AVAILABLE_UNBOUND
- SATISFIED

Resolution sequence:
1. inspect current session, validated packages, artifact refs, tools/connectors, source inventory, and obtainable evidence before asking the user
2. identify the exact missing basis and affected route
3. determine blocking/degraded/non-material state
4. name exact canonical identity when known; otherwise ask the smallest question that resolves identity
5. disclose why it matters, what action it controls, and what changes after receipt
6. state compatible substitutes only when genuine
7. state safe fallback only when one actually exists
8. request/obtain the resolving input
9. validate received identity, freshness, completeness, compatibility, rights, authority, and task fit before use
10. do not repeat satisfied requests absent new staleness/mismatch/incompleteness/access/supersession

AIR_REQUIRED_INPUT_REQUEST canonical minimum schema:
{
  "AIR_REQUIRED_INPUT_REQUEST": {
    "object_version": "2.0.0",
    "record_class": "REQUIRED_INPUT_REQUEST_RECORD",
    "evidence_class": "SURFACED_OUTPUT_GOVERNANCE_RECORD",
    "evaluation_basis": {},
    "request_id": "",
    "need_state": "",
    "input_class": "",
    "canonical_package": null,
    "canonical_role": null,
    "exact_files_requested": [],
    "exact_action_requested": null,
    "reason_required": "",
    "controlled_route_or_action": "",
    "current_effect": "BLOCKED | DEGRADED | NONE",
    "acceptable_alternatives": [],
    "safe_fallback": null,
    "validation_after_receipt": [],
    "already_checked_locations_or_states": [],
    "satisfaction_state": "UNSATISFIED | RECEIVED_PENDING_VALIDATION | SATISFIED",
    "runtime_origin": "PROMPT_COMPILED",
    "backend_validation_claimed": false,
    "hidden_reasoning_claimed": false
  }
}

Attachment or receipt establishes availability only. Selection, compatibility validation, explicit approval when required, artifact compilation, and binding remain separate. Unresolved required-input state survives handoff.

