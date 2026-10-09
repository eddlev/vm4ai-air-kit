AMRS-AWARE LAW APPLICABILITY AND ARTIFACT BINDING
--------------------------------------------------

Patch marker: AIR_LAW_APPLICABILITY_ROUTER_V1
Requirements: LR02, LR03, LR04, LR05, LR06

`AIR_RUNTIME_ROUTE_MAP` remains runtime-route-only and has no law-selection or semantic-definition authority. `AIR_LAW_APPLICABILITY_ROUTER_V1` is a separately generated, derived, non-authoritative task+task-target-AMRS→law-reference router. Missing router metadata never defaults to all laws or no laws; resolution is UNRESOLVED and affected binding/execution fails closed.

Applicability polarity is semantic, not lexical. Negative wording such as `not`, `must not`, `does not`, or `cannot` is never sufficient by itself to exclude a law. Derived applicability metadata must distinguish NEGATES_APPLICABILITY from NEGATES_AUTHORITY, NEGATES_ALIAS, CONSTRAINS_BEHAVIOR, NEGATES_FALLBACK, and UNRESOLVED_NEGATION. Only explicit source-backed NEGATES_APPLICABILITY may support exclusion. Negative clauses that bound authority, aliases, fallback, or in-route behavior preserve applicability when the law otherwise governs the route/task. Mixed or unresolved polarity remains UNRESOLVED and fails closed rather than being guessed.

AIR_LAW_APPLICABILITY_ROUTER_V1_MACHINE_CONTRACT_BEGIN
```json
{
  "SYSTEM_DESIGNATION": "AIR_LAW_APPLICABILITY_ROUTER_V1",
  "contract_version": "1.0.0",
  "semantic_owner": "AIR_CORE_RUNTIME_V2",
  "runtime_file": "catalog/AIR_LAW_APPLICABILITY_ROUTER.json",
  "runtime_file_authority": "DERIVED_NONAUTHORITATIVE_MACHINE_ROUTER",
  "core_registry_ref": "AIR_LAW_ID_REGISTRY_V1",
  "applicability_polarity_semantics": {
    "classification_classes": [
      "NEGATES_APPLICABILITY",
      "NEGATES_AUTHORITY",
      "NEGATES_ALIAS",
      "CONSTRAINS_BEHAVIOR",
      "NEGATES_FALLBACK",
      "UNRESOLVED_NEGATION"
    ],
    "lexical_negation_is_exclusion_proof": false,
    "exclusion_requires": "EXPLICIT_SOURCE_BACKED_NEGATES_APPLICABILITY",
    "constraint_or_authority_negation_effect": "PRESERVE_OTHERWISE_SUPPORTED_APPLICABILITY",
    "mixed_or_unknown_behavior": "UNRESOLVED_FAIL_CLOSED"
  },
  "required_inputs": [
    "current_task_identity",
    "task_target_amrs",
    "current_task_class_ids",
    "current_task_facet_ids",
    "current_law_registry_identity_and_fingerprint",
    "current_router_identity_and_fingerprint"
  ],
  "resolution_algorithm": [
    "VALIDATE_REGISTRY_IDENTITY_AND_FINGERPRINT",
    "RESOLVE_CURRENT_TASK_IDENTITY_AND_TASK_TARGET_AMRS",
    "LOAD_DERIVED_APPLICABILITY_METADATA",
    "ADD_MANDATORY_FLOOR_CLOSURE",
    "EVALUATE_TASK_CLASS_AND_AMRS_PREDICATES",
    "EXPAND_LAW_DEPENDENCY_AND_RUNTIME_DEPENDENCY_CLOSURE",
    "REJECT_MISSING_IDS_CYCLES_AND_CONTRADICTIONS",
    "DETERMINISTICALLY_ORDER_SELECTED_LAW_IDS",
    "EMIT_INCLUDE_EXCLUDE_APPLICABILITY_EVIDENCE",
    "COMPUTE_LAW_RESOLUTION_FINGERPRINT",
    "BIND_RESULT_TO_AIR_ARTIFACT_LAW_RESOLUTION_STATE"
  ],
  "required_outputs": [
    "selected_law_ids",
    "mandatory_floor_closure",
    "law_dependency_closure",
    "runtime_dependency_closure",
    "applicability_evidence",
    "law_resolution_fingerprint",
    "resolution_state"
  ],
  "resolution_states": [
    "CURRENT",
    "STALE_PENDING_REVALIDATION",
    "UNRESOLVED"
  ],
  "staleness_invalidators": [
    "task_identity_change",
    "task_target_amrs_change",
    "law_registry_fingerprint_change",
    "router_fingerprint_change",
    "material_scope_change"
  ],
  "missing_router_or_metadata_behavior": "UNRESOLVED_FAIL_CLOSED_NO_SILENT_ALL_LAWS_OR_NO_LAWS_DEFAULT",
  "semantic_definition_authority": "NONE_ROUTER_REFERENCES_CORE_LAWS_ONLY",
  "law_resolution_construction_ref": "AIR_LAW_RESOLUTION_CONSTRUCTION_V1",
  "law_resolution_construction_version": "1.0.0",
  "construction_semantics": "ALL_SELECTED_LAW_ORDERING_EVIDENCE_ORDERING_EMPTY_CLOSURE_SERIALIZATION_AND_FINGERPRINT_RULES_OWNED_BY_AIR_LAW_RESOLUTION_CONSTRUCTION_V1"
}
```

AIR_LAW_APPLICABILITY_ROUTER_V1_MACHINE_CONTRACT_END
