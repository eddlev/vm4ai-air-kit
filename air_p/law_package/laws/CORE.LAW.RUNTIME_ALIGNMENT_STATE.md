==================================================
RUNTIME ALIGNMENT STATE LAW
==================================================

Patch marker: AIR_RUNTIME_ALIGNMENT_STATE_V1
Floor invariant: AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY

The legacy interval-based runtime watchdog behavior is retired. Runtime continuity is maintained by mandatory RT.ALIGN on every post-activation user turn and by additional state-transition/pre-effect/post-effect/recovery evaluation profiles when triggered.

AIR_SESSION.runtime_alignment_state minimum fields:
- state
- state_epoch
- current_evaluation_id
- current_evaluation_profile
- last_alignment_check_ref
- last_validation_report_ref
- last_evaluation_result
- post_activation_user_message_count
- recovery_state
- model_drift_evidence_state
- nonmodel_reconciliation_state

`runtime_alignment_state` never treats ordinary state evolution as model drift. Its current alignment projection follows the canonical ALIGNED / RECONCILIATION_REQUIRED / DRIFT_DETECTED truth table and keeps recovery/error classification independent.

On each post-activation user turn:
1. increment post_activation_user_message_count once
2. execute TURN_ENTRY alignment against canonical pre-transition state
3. construct AIR_ALIGNMENT_CHECK and coupled AIR_VALIDATION_REPORT
4. emit the pair before ordinary narrative or receiver-facing content, including handoff delivery responses
5. dispatch semantic instruction handler only after the required pair and dependency state are registered

No user or lower layer may configure an interval or waive a turn evaluation.

Missed evaluation/emission is a process defect. Recover visibly, preserve evidence of the miss when material, and do not treat late recovery as proof that the original response complied.


PATCH-025 BOOTSTRAP RECOVERY CONTRACT

Patch marker: AIR_PATCH025_BOOTSTRAP_RECOVERY_CONTRACT_V1

This contract is a narrow pre-activation recovery extension owned by AIR Core Runtime. It solves AIRP-PATCH-025 only. It does not resolve AIRP-PATCH-020, bind an Artifact, issue a lease, create Orbit-0 execution, enter RT.ACTION, or grant positive/material/canonical mutation authority.

AIR_PATCH025_BOOTSTRAP_RECOVERY_MACHINE_PAYLOAD_BEGIN
```json
{
  "CONTRACT_VERSION": "1.0.0",
  "SYSTEM_DESIGNATION": "AIR_PATCH025_BOOTSTRAP_RECOVERY_CONTRACT_V1",
  "action_semantics": {
    "AIR_ACTION_AUTHORIZATION": "PROHIBITED",
    "AIR_GATE_as_effect_authority": "PROHIBITED",
    "RT.ACTION": "PROHIBITED",
    "aliases_have_machine_authority": false,
    "artifact_binding": "PROHIBITED",
    "artifact_lease_creation": "PROHIBITED",
    "canonical_action_class_count": 5,
    "canonical_action_classes": [
      "RECOVERY_READ_ONLY_SOURCE_INSPECTION",
      "RECOVERY_EVIDENCE_ANALYSIS",
      "RECOVERY_PATCH_ARCHITECTURE_DESIGN",
      "RECOVERY_TEST_DESIGN",
      "RECOVERY_BOOTSTRAP_HOTFIX_SPECIFICATION_PREPARATION"
    ],
    "canonical_mutation_authority": "NONE",
    "class_authorized_external_effect": "NONE",
    "class_authorized_filesystem_write": "NONE",
    "class_specific_persistent_AIR_state_mutation": "NONE",
    "classes": {
      "RECOVERY_BOOTSTRAP_HOTFIX_SPECIFICATION_PREPARATION": {
        "completion": "EXTERNAL_EXECUTOR_COULD_GENERATE_AND_VALIDATE_WITHOUT_INVENTING_SEMANTICS",
        "fail_closed": [
          "MATERIAL_ARCHITECTURE_UNRESOLVED",
          "TEST_ORACLE_UNRESOLVED",
          "FILE_SCOPE_UNRESOLVED",
          "BASELINE_IDENTITY_UNRESOLVED",
          "WOULD_REQUIRE_PATCH020_INVENTION"
        ],
        "integrates_existing_classes": [
          "RECOVERY_PATCH_ARCHITECTURE_DESIGN",
          "RECOVERY_TEST_DESIGN"
        ],
        "permitted_computations": [
          "REQUIREMENT_INTEGRATION",
          "FILE_SET_CLOSURE",
          "PREHASH_LEDGER",
          "POSTHASH_REQUIREMENTS",
          "DIFF_REQUIREMENTS",
          "COMPILER_REQUIREMENTS",
          "DERIVED_REGENERATION_REQUIREMENTS",
          "TEST_INTEGRATION",
          "VALIDATION_SEQUENCE",
          "INSTALL_ROLLBACK_SPECIFICATION"
        ],
        "permitted_reads": "ALL_SETTLED_RECOVERY_DESIGN_AND_EXACT_BASELINE_EVIDENCE",
        "primary_deliverable": "NON_MATERIAL_RECOVERY_OUTPUT:BOOTSTRAP_HOTFIX_SPECIFICATION",
        "prohibited": [
          "GENERATE_CANDIDATE_BYTES",
          "WRITE_PACKAGE_FILES",
          "REGENERATE_DERIVED_FILES",
          "EDIT_COMPILER",
          "EDIT_TESTS",
          "EXECUTE_INSTALLATION",
          "OPEN_INSTALLATION_GATE",
          "CLAIM_UNKNOWN_POSTHASH"
        ],
        "purpose": "INTEGRATE_SETTLED_EVIDENCE_ARCHITECTURE_TESTS_AND_EXTERNAL_MAINTENANCE_PROCEDURES_INTO_IMPLEMENTATION_READY_SPECIFICATION_WITHOUT_GENERATING_IMPLEMENTATION",
        "qualifying_intent": [
          "PREPARE_HOTFIX_SPECIFICATION",
          "PREPARE_MAINTENANCE_PACKAGE_SPECIFICATION",
          "FREEZE_INTENDED_FILE_SET",
          "DEFINE_HASH_REQUIREMENTS",
          "DEFINE_VALIDATION_INSTALL_ROLLBACK"
        ],
        "required_basis": "BASELINE_DEFECT_SETTLED_ARCHITECTURE_FILE_SCOPE_TEST_REQUIREMENTS_NON_GOALS_AUTHORITY_BOUNDARY",
        "subordinate_classes": [
          "RECOVERY_READ_ONLY_SOURCE_INSPECTION",
          "RECOVERY_EVIDENCE_ANALYSIS"
        ]
      },
      "RECOVERY_EVIDENCE_ANALYSIS": {
        "completion": "ANALYTICAL_QUESTION_RESOLVED_TO_EVIDENCE_LIMIT_WITH_UNSUPPORTED_REMAINDER_EXPLICIT",
        "fail_closed": [
          "MATERIAL_EVIDENCE_CONFLICT_WITHOUT_RESOLUTION_BASIS",
          "REQUIRED_SOURCE_UNAVAILABLE",
          "CLAIM_EXCEEDS_EVIDENCE",
          "WOULD_CREATE_AUTHORITY"
        ],
        "permitted_computations": [
          "CORRELATION",
          "CONSISTENCY",
          "CAUSAL_MAPPING",
          "DEPENDENCY_REASONING",
          "COMPATIBILITY",
          "SUPPORT_REFUTATION",
          "EVIDENCE_STRENGTH"
        ],
        "permitted_reads": "SOURCE_INSPECTION_READS_PLUS_VALIDATED_RECOVERY_EVIDENCE_AND_APPROVED_DESIGN_BASIS_AS_DESIGN_EVIDENCE",
        "primary_deliverable": "NON_MATERIAL_RECOVERY_OUTPUT:EVIDENCE_ANALYSIS",
        "prohibited": [
          "PROMOTE_UNRESOLVED_FACT_TO_CANONICAL_TRUTH",
          "INVENT_EVIDENCE",
          "PATCH020_CONSTRUCTION",
          "SOURCE_MUTATION",
          "CANDIDATE_GENERATION",
          "AUTHORITY_CREATION"
        ],
        "purpose": "DERIVE_NONAUTHORIZING_EVIDENCE_GROUNDED_FINDINGS_WITH_UNRESOLVED_FACTS_PRESERVED",
        "qualifying_intent": [
          "ANALYZE",
          "EXPLAIN_EVIDENCE",
          "RECONCILE",
          "IDENTIFY_CONTRADICTION",
          "ASSESS_COMPATIBILITY",
          "TRACE_CAUSE"
        ],
        "required_basis": "EVIDENCE_SUFFICIENT_FOR_EXACT_ANALYTICAL_CLAIM",
        "subordinate_classes": [
          "RECOVERY_READ_ONLY_SOURCE_INSPECTION"
        ]
      },
      "RECOVERY_PATCH_ARCHITECTURE_DESIGN": {
        "completion": "REPAIR_BEHAVIOR_AFFECTED_SURFACE_NON_GOALS_AND_UNRESOLVED_DEPENDENCIES_EXPLICIT",
        "fail_closed": [
          "SEMANTIC_OWNER_UNRESOLVED",
          "REQUIRES_INVENTED_LAW_SEMANTICS",
          "AFFECTED_SOURCE_IDENTITY_UNAVAILABLE",
          "AUTHORITY_EXPANSION"
        ],
        "permitted_computations": [
          "SEMANTIC_DIFF_DESIGN",
          "ROUTE_STATE_DESIGN",
          "SOURCE_OWNERSHIP_MAPPING",
          "FILE_CLOSURE",
          "BLAST_RADIUS",
          "DERIVED_IMPACT",
          "COMPILER_TRANSITION_REQUIREMENTS",
          "NEGATIVE_BOUNDARIES"
        ],
        "permitted_reads": "SOURCE_EVIDENCE_CORE_CONTRACTS_DERIVED_PROJECTIONS_COMPILER_CONSTRAINTS_SETTLED_DESIGN",
        "primary_deliverable": "NON_MATERIAL_RECOVERY_OUTPUT:PATCH_ARCHITECTURE_CANDIDATE",
        "prohibited": [
          "CANDIDATE_SOURCE_BYTES",
          "CANONICAL_EDIT",
          "DERIVED_REGENERATION",
          "INSTALLATION",
          "PATCH020_SEMANTIC_INVENTION"
        ],
        "purpose": "DEFINE_PROSPECTIVE_REPAIR_SEMANTICS_AND_SOURCE_ARCHITECTURE_WITHOUT_IMPLEMENTATION_BYTES",
        "qualifying_intent": [
          "DESIGN_FIX",
          "DEFINE_PATCH_ARCHITECTURE",
          "DEFINE_SEMANTIC_DIFF",
          "IDENTIFY_AFFECTED_FILES",
          "DEFINE_ROUTE_OR_STATE_CHANGE",
          "RESOLVE_DESIGN_CONTRADICTION"
        ],
        "required_basis": "DEFECT_OWNER_PRE_POST_BEHAVIOR_AND_SOURCE_OWNERSHIP_SUFFICIENTLY_ESTABLISHED",
        "subordinate_classes": [
          "RECOVERY_READ_ONLY_SOURCE_INSPECTION",
          "RECOVERY_EVIDENCE_ANALYSIS"
        ]
      },
      "RECOVERY_READ_ONLY_SOURCE_INSPECTION": {
        "completion": "REQUESTED_OBSERVABLE_FACTS_REPORTED_WITH_BASIS_AND_UNKNOWNS",
        "fail_closed": [
          "SOURCE_MISSING",
          "SOURCE_IDENTITY_AMBIGUOUS",
          "READ_BASIS_STALE",
          "REQUEST_REQUIRES_INFERENCE_OR_MUTATION"
        ],
        "permitted_computations": [
          "SHA256",
          "BYTE_COMPARE",
          "READ_ONLY_DIFF",
          "PARSE",
          "ENUMERATE",
          "COUNT",
          "SORT_FOR_PRESENTATION",
          "SOURCE_LOCATION_EXTRACTION"
        ],
        "permitted_reads": "CURRENT_EXACT_SOURCE_AND_VALIDATED_EVIDENCE_AND_EXPLICIT_PROVENANCE",
        "primary_deliverable": "NON_MATERIAL_RECOVERY_OUTPUT:SOURCE_INSPECTION_REPORT",
        "prohibited": [
          "SOURCE_MUTATION",
          "CANDIDATE_GENERATION",
          "UNSUPPORTED_CAUSAL_CONCLUSION",
          "PATCH_ARCHITECTURE",
          "TEST_ARCHITECTURE",
          "HOTFIX_PACKAGE_PREPARATION"
        ],
        "purpose": "OBSERVE_MEASURE_PARSE_REPORT_EXACT_SOURCE_OR_EVIDENCE_FACTS",
        "qualifying_intent": [
          "INSPECT",
          "READ",
          "LOCATE",
          "ENUMERATE",
          "COMPARE_EXACT_BYTES",
          "CALCULATE_HASHES",
          "STRUCTURAL_DIFFERENCES",
          "VERIFY_LITERAL_OR_STRUCTURE"
        ],
        "required_basis": "EXACT_READABLE_SOURCE_OR_EVIDENCE_FOR_REQUESTED_OBSERVATION",
        "subordinate_classes": []
      },
      "RECOVERY_TEST_DESIGN": {
        "completion": "PROSPECTIVE_VERIFICATION_ENVELOPE_COVERS_POSITIVE_AND_RELEVANT_NEGATIVE_CASES",
        "fail_closed": [
          "EXPECTED_BEHAVIOR_UNRESOLVED",
          "TEST_ORACLE_UNDEFINED",
          "REQUIRES_PATCH020_CONSTRUCTION",
          "MATERIAL_SOURCE_TEST_BASIS_UNAVAILABLE"
        ],
        "permitted_computations": [
          "FIXTURE_DESIGN",
          "ASSERTION_DESIGN",
          "EXPECTED_STATE",
          "NEGATIVE_CASES",
          "MUTATION_DESIGN",
          "STATE_TRANSITION_TESTS",
          "COMPILER_VALIDATION",
          "REPRODUCIBILITY_TESTS"
        ],
        "permitted_reads": "SOURCE_TESTS_COMPILER_EVIDENCE_EXISTING_PATCH_ARCHITECTURE",
        "primary_deliverable": "NON_MATERIAL_RECOVERY_OUTPUT:RECOVERY_TEST_AND_ACCEPTANCE_DESIGN",
        "prohibited": [
          "INSTALLATION",
          "CANDIDATE_SOURCE_FILES",
          "CANONICAL_TEST_MUTATION",
          "FABRICATED_TEST_RESULTS",
          "SILENT_MATERIAL_PATCH_REDESIGN"
        ],
        "purpose": "DEFINE_PROSPECTIVE_VERIFICATION_REGRESSION_NEGATIVE_MUTATION_AND_REPRODUCIBILITY_TESTS",
        "qualifying_intent": [
          "DESIGN_TESTS",
          "DEFINE_FIXTURES",
          "DEFINE_ASSERTIONS",
          "DEFINE_REGRESSION_MATRIX",
          "DEFINE_NEGATIVE_TESTS",
          "DEFINE_VALIDATION_SEQUENCE",
          "DEFINE_HARNESS_CHANGES"
        ],
        "required_basis": "BEHAVIOR_EXPECTED_SEMANTICS_RELEVANT_SOURCE_TEST_STRUCTURE_AND_OBSERVABLE_PASS_FAIL_CRITERIA",
        "subordinate_classes": [
          "RECOVERY_READ_ONLY_SOURCE_INSPECTION",
          "RECOVERY_EVIDENCE_ANALYSIS"
        ]
      }
    },
    "core_owned_bookkeeping_exception": {
      "class_prohibitions_do_not_suppress": [
        "RT.RECOVERY_LIFECYCLE_BOOKKEEPING",
        "RUNTIME_ALIGNMENT_STATE_UPDATES",
        "RECOVERY_ERROR_RECORDS",
        "REUSABLE_FAILURE_MODE_CAPTURE_WHERE_CORE_REQUIRES",
        "SURFACED_OBJECT_LEDGER_ACCOUNTING_WHERE_CORE_REQUIRES",
        "PROVENANCE_PERSISTENCE_WHERE_CORE_REQUIRES"
      ],
      "positive_execution_authority": "NONE",
      "these_effects_are_action_class_body": "NO"
    },
    "dispatch": {
      "highest_class_wins": "PROHIBITED",
      "model_preference": "PROHIBITED",
      "multiple_independent_explicitly_ordered": "EXECUTE_FIRST_UNRESOLVED_BOUNDED_UNIT_ONLY",
      "multiple_independent_unordered": "AMBIGUOUS_RECOVERY_REQUEST_FAIL_CLOSED",
      "persistent_queue_authority": "NONE",
      "primary_selection_basis": "REQUESTED_RECEIVER_FACING_DELIVERABLE",
      "subordinate_operation_does_not_create_second_primary": true
    },
    "exactly_one_primary_class_per_bounded_unit": true,
    "material_effect_authority": "NONE",
    "one_bounded_recovery_unit_per_response": true,
    "orbit_0_execution": "PROHIBITED",
    "ordinary_project_execution": "PROHIBITED",
    "output_classification": "NON_MATERIAL_RECOVERY_OUTPUT",
    "output_does_not_close_project": true,
    "output_does_not_satisfy_receiver_delivery_state": true,
    "output_not_approved_output": true,
    "output_not_rt_deliver": true,
    "positive_execution_authority": "NONE"
  },
  "alignment_projection": {
    "authority": "EVALUATION_PROJECTION_ONLY",
    "contract_id": "PATCH025_RECOVERY_ALIGNMENT_PROJECTION_V1",
    "coupled_validation_report_authority": "EVALUATION_EVIDENCE_ONLY_NO_SECOND_RECOVERY_OWNER",
    "live_carrier_shape_allowed": "NO",
    "mapping": {
      "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC": "ACTIVE_BLOCKED",
      "COMPLETED_RETRY_REQUIRED": "COMPLETED_RETRY_REQUIRED",
      "INACTIVE": "RECOVERY_INACTIVE",
      "INACTIVE_USER_STOP": "INACTIVE_USER_STOP",
      "INVALIDATED_FAIL_CLOSED": "INVALIDATED_FAIL_CLOSED"
    },
    "mutation_authority": "NONE",
    "path": "AIR_ALIGNMENT_CHECK.recovery_state",
    "required_evaluation_bindings": [
      "evaluation_id",
      "evaluation_profile",
      "state_epoch",
      "evaluated_state_refs",
      "validation_report_ref"
    ],
    "stale_projection_authority": "NONE"
  },
  "design_authorization_stack": {
    "consolidated_spec": "AIR_PATCH025_BOOTSTRAP_RECOVERY_CONSOLIDATED_IMPLEMENTATION_SPECIFICATION_V1",
    "revision_1": "PATCH025_PERSISTENT_STATE_LIFECYCLE_REGISTRATION_CLOSURE",
    "revision_2": "CORRECTED_STATE_PLANE_NORMALIZATION",
    "revision_3": "RECOVERY_TRANSFER_PROJECTION_BOUNDARY",
    "revision_3_sha256": "5a52be81ebe329d2b453a4fab017daeac33f293f49d7e4cb0fa466dc1691ddbc"
  },
  "does_not_solve_patch_ids": [
    "AIRP-PATCH-020"
  ],
  "external_maintenance_boundary": {
    "AIR_ACTION_AUTHORIZATION_install_authority": "NONE",
    "AIR_GATE_install_authority": "NONE",
    "candidate_generation_validation": "SEPARATELY_AUTHORIZED_EXTERNAL_BOOTSTRAP_MAINTENANCE_PREPARATION",
    "installation": "NOT_RT.ACTION",
    "installation_requires_separate_human_authorization_bound_to_frozen_manifest_sha256": true
  },
  "handoff_projection": {
    "allowed_scalar_values": [
      "NONE_SOURCE_SESSION",
      "HANDOFF_REVALIDATION_REQUIRED"
    ],
    "authority": "NONE",
    "contract_id": "PATCH025_RECOVERY_STATE_HANDOFF_PROJECTION_V1",
    "destination_first_incident_id": "AIR_RECOVERY_INCIDENT::1",
    "destination_initialization_authority": "NONE",
    "destination_sequence_initial": 0,
    "handoff_path": "AIR_HANDOFF_CARD.runtime_alignment_state.recovery_state",
    "live_owner": "AIR_SESSION.runtime_alignment_state.recovery_state",
    "mapping": {
      "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC": "HANDOFF_REVALIDATION_REQUIRED",
      "COMPLETED_RETRY_REQUIRED": "HANDOFF_REVALIDATION_REQUIRED",
      "INACTIVE": "NONE_SOURCE_SESSION",
      "INACTIVE_USER_STOP": "HANDOFF_REVALIDATION_REQUIRED",
      "INVALIDATED_FAIL_CLOSED": "HANDOFF_REVALIDATION_REQUIRED"
    },
    "mutation_authority": "NONE",
    "nested_live_carrier_serialization": "PROHIBITED",
    "portable_state_historical_completeness_claim": "PROHIBITED",
    "source_failure_evidence_refs_as_fresh_destination_basis": "PROHIBITED",
    "source_incident_counter_restore": "PROHIBITED",
    "source_incident_id_restore": "PROHIBITED",
    "source_incident_sequence_restore": "PROHIBITED"
  },
  "incident_identity": {
    "constructor": "AIR_RECOVERY_INCIDENT::<decimal recovery_incident_sequence>",
    "decimal_contract": "ASCII_BASE10_UNSIGNED_NO_LEADING_ZEROES",
    "decrement": "PROHIBITED",
    "inactive_clears": [
      "recovery_incident_id",
      "bootstrap_recovery_user_message_count",
      "source_failure_evidence_refs"
    ],
    "inactive_retains": [
      "recovery_incident_sequence"
    ],
    "model_selected_unique_id": "PROHIBITED",
    "new_incident_counter_initial": 0,
    "randomness": "PROHIBITED",
    "reuse": "PROHIBITED",
    "scope": "CURRENT_AIR_SESSION_ONLY",
    "sequence_field": "recovery_incident_sequence",
    "sequence_increment_amount": 1,
    "sequence_increment_on": "EVERY_VALID_TRANSITION_INTO_ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC",
    "sequence_initial": 0,
    "terminal_preserves_sequence_and_id_and_counter": true,
    "timestamp_inference": "PROHIBITED",
    "uuid_generation": "PROHIBITED"
  },
  "lifecycle": {
    "allowed_transitions": [
      [
        "INACTIVE",
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC"
      ],
      [
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC",
        "INVALIDATED_FAIL_CLOSED"
      ],
      [
        "INVALIDATED_FAIL_CLOSED",
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC"
      ],
      [
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC",
        "INACTIVE_USER_STOP"
      ],
      [
        "INACTIVE_USER_STOP",
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC"
      ],
      [
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC",
        "COMPLETED_RETRY_REQUIRED"
      ],
      [
        "COMPLETED_RETRY_REQUIRED",
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC"
      ],
      [
        "COMPLETED_RETRY_REQUIRED",
        "INACTIVE"
      ]
    ],
    "initial_state": "INACTIVE",
    "initial_values": {
      "bootstrap_recovery_user_message_count": null,
      "recovery_incident_id": null,
      "recovery_incident_sequence": 0,
      "source_failure_evidence_refs": []
    },
    "prohibited_transitions": [
      [
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC",
        "INACTIVE"
      ]
    ],
    "repair_boundary": {
      "fresh_restore_new_incident_transition": [
        "COMPLETED_RETRY_REQUIRED",
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC"
      ],
      "fresh_restore_success_transition": [
        "COMPLETED_RETRY_REQUIRED",
        "INACTIVE"
      ],
      "interrupted_restoration_resume": "PROHIBITED",
      "required_fresh_restore_sequence": [
        "RT.BOOT",
        "RT.HANDOFF_RESTORE"
      ],
      "validated_repair_from_active": "COMPLETED_RETRY_REQUIRED"
    },
    "states": [
      "INACTIVE",
      "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC",
      "INVALIDATED_FAIL_CLOSED",
      "COMPLETED_RETRY_REQUIRED",
      "INACTIVE_USER_STOP"
    ],
    "terminal_reentry": {
      "INACTIVE_USER_STOP": {
        "explicit_user_restart_required": true,
        "prior_counter_resume": "PROHIBITED",
        "prior_route_resume": "PROHIBITED",
        "requires": [
          "EXPLICIT_USER_RESTART_REQUEST",
          "FRESH_QUALIFYING_CURRENT_SESSION_FAILURE_EVIDENCE",
          "NEW_RT.RECOVERY_INITIALIZATION"
        ],
        "stale_carrier_resume": "PROHIBITED"
      },
      "INVALIDATED_FAIL_CLOSED": {
        "explicit_user_restart_required": false,
        "prior_counter_resume": "PROHIBITED",
        "prior_route_resume": "PROHIBITED",
        "requires": [
          "INVALIDATOR_DEMONSTRABLY_RESOLVED",
          "FRESH_QUALIFYING_CURRENT_SESSION_FAILURE_EVIDENCE",
          "NEW_RT.RECOVERY_INITIALIZATION"
        ],
        "stale_carrier_resume": "PROHIBITED"
      }
    }
  },
  "patch020_invariant": {
    "applicability_evidence_ordering_construction": "PROHIBITED",
    "empty_closure_construction": "PROHIBITED",
    "fingerprint_construction": "PROHIBITED",
    "law_resolution_fingerprint_required_value": null,
    "selected_law_ordering_construction": "PROHIBITED",
    "serializer_semantics_construction": "PROHIBITED",
    "status": "ACTIVE_UNRESOLVED_HANDOFF_RESTORE_BLOCKING",
    "scope": "HISTORICAL_PATCH025_PRE_V1_GUARD"
  },
  "routing": {
    "RT.ALIGN": {
      "conditional_successors": {
        "ordinary_or_active_or_stop_probe": "RT.INPUT_TRANSLATE",
        "reestablishment_basis_gap": "RT.UNCERTAINTY_RESOLVE",
        "reestablishment_hard_invalid": "RT.RECOVERY_SURFACE_INVALIDATION_ONLY",
        "reestablishment_pass": "RT.RECOVERY"
      },
      "mode_profiles": {
        "POSTACTIVATION_NORMAL": "TURN_ENTRY",
        "PREACTIVATION_RECOVERY_DIAGNOSTIC_INGRESS": "RECOVERY",
        "PREACTIVATION_RECOVERY_REESTABLISHMENT_PROBE": "RECOVERY",
        "PREACTIVATION_RECOVERY_STOP_RESTART_PROBE": "RECOVERY"
      }
    },
    "RT.BOOT": {
      "completed_retry_required_use": "REQUIRED_FOR_FRESH_RESTORATION",
      "terminal_reentry_use": "PROHIBITED"
    },
    "RT.CLASSIFY": {
      "active_diagnostic_primary_class_count": 1,
      "definite_nonrestart_successor": "END_RESPONSE",
      "exact_restart_with_fresh_evidence_successor": "RT.RECOVERY",
      "exact_restart_without_fresh_evidence_successor": "RT.UNCERTAINTY_RESOLVE",
      "stop_restart_control_classes": [
        "RECOVERY_RESTART_REQUEST",
        "RECOVERY_RESTART_NOT_REQUESTED"
      ],
      "uncertain_restart_successor": "RT.UNCERTAINTY_RESOLVE_IF_BASIS_GAP"
    },
    "RT.INPUT_TRANSLATE": {
      "existing_failure_route": "RT.UNCERTAINTY_RESOLVE",
      "lifecycle_mutation_on_translation_uncertainty": "NONE_UNLESS_SEPARATE_INVALIDATOR"
    },
    "RT.RECOVERY": {
      "allowed_next": [
        "END_RESPONSE"
      ],
      "cases": [
        "RECOVERY_INITIALIZE_FROM_HANDOFF_FAILURE",
        "RECOVERY_EXECUTE_ACTIVE_DIAGNOSTIC_UNIT",
        "RECOVERY_REINITIALIZE_AFTER_USER_STOP",
        "RECOVERY_REINITIALIZE_AFTER_INVALIDATION",
        "RECOVERY_SURFACE_INVALIDATION_ONLY",
        "RECOVERY_CORE_LIFECYCLE_BOOKKEEPING"
      ]
    }
  },
  "rt_turn": {
    "mode_effects": {
      "POSTACTIVATION_NORMAL": {
        "bootstrap_recovery_user_message_count": "UNCHANGED",
        "post_activation_user_message_count": "INCREMENT_EXACTLY_ONCE",
        "turn_context": "NORMAL"
      },
      "PREACTIVATION_RECOVERY_DIAGNOSTIC_INGRESS": {
        "bootstrap_recovery_user_message_count": "INCREMENT_CURRENT_INCIDENT_EXACTLY_ONCE",
        "post_activation_user_message_count": "UNCHANGED",
        "turn_context": "RECOVERY"
      },
      "PREACTIVATION_RECOVERY_REESTABLISHMENT_PROBE": {
        "bootstrap_recovery_user_message_count": "UNCHANGED",
        "post_activation_user_message_count": "UNCHANGED",
        "turn_context": "PROBE"
      },
      "PREACTIVATION_RECOVERY_STOP_RESTART_PROBE": {
        "bootstrap_recovery_user_message_count": "UNCHANGED",
        "post_activation_user_message_count": "UNCHANGED",
        "turn_context": "PROBE"
      }
    },
    "modes": [
      "POSTACTIVATION_NORMAL",
      "PREACTIVATION_RECOVERY_DIAGNOSTIC_INGRESS",
      "PREACTIVATION_RECOVERY_STOP_RESTART_PROBE",
      "PREACTIVATION_RECOVERY_REESTABLISHMENT_PROBE"
    ],
    "preentry_failure": "NO_RT.TURN_ENTRY_NO_COUNTER_INCREMENT_FAIL_CLOSED",
    "preentry_mode_predicates": {
      "POSTACTIVATION_NORMAL": "ARTIFACT_BOUND_EXECUTION_AND_EXISTING_NORMAL_TURN_REQUIREMENTS",
      "PREACTIVATION_RECOVERY_DIAGNOSTIC_INGRESS": "STATE_ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC_AND_BOOTSTRAP_NO_ARTIFACT_AND_NO_POSITIVE_AUTHORITY_AND_CURRENT_ROUTE_NONE",
      "PREACTIVATION_RECOVERY_REESTABLISHMENT_PROBE": "STATE_INVALIDATED_FAIL_CLOSED_AND_VALID_TERMINAL_INCIDENT_AND_BOOTSTRAP_NO_ARTIFACT_AND_NO_POSITIVE_AUTHORITY_AND_CURRENT_ROUTE_NONE",
      "PREACTIVATION_RECOVERY_STOP_RESTART_PROBE": "STATE_INACTIVE_USER_STOP_AND_VALID_TERMINAL_INCIDENT_AND_BOOTSTRAP_NO_ARTIFACT_AND_NO_POSITIVE_AUTHORITY_AND_CURRENT_ROUTE_NONE"
    },
    "unconditional_produces": [
      "TURN_CONTEXT"
    ],
    "unknown_mode_behavior": "FAIL_CLOSED"
  },
  "semantic_owner": "AIR_CORE_RUNTIME_V2",
  "solves_patch_id": "AIRP-PATCH-025",
  "state_plane_normalization": {
    "canonical_current_state_field_count": 5,
    "canonical_current_state_fields": [
      "state",
      "recovery_incident_sequence",
      "recovery_incident_id",
      "bootstrap_recovery_user_message_count",
      "source_failure_evidence_refs"
    ],
    "canonical_mutable_owner": "AIR_SESSION.runtime_alignment_state.recovery_state",
    "durable_derived_rule_count": 10,
    "durable_derived_rule_refs": [
      "PATCH025_RULE_RECOVERY_CONTRACT_IDENTITY",
      "PATCH025_RULE_CANONICAL_RECOVERY_ACTION_CLASS_ENUM",
      "PATCH025_RULE_IMPLEMENTATION_AUTHORITY_NONE",
      "PATCH025_RULE_CANONICAL_MUTATION_AUTHORITY_NONE",
      "PATCH025_RULE_MATERIAL_EFFECT_AUTHORITY_NONE",
      "PATCH025_RULE_POSITIVE_EXECUTION_AUTHORITY_NONE_PREDICATE",
      "PATCH025_RULE_ORDINARY_EXECUTION_DISPATCH_PROHIBITED",
      "PATCH025_RULE_FORBIDDEN_TRANSITIONS",
      "PATCH025_RULE_COMPLETION_END_RESPONSE",
      "PATCH025_RULE_LAW_RESOLUTION_FINGERPRINT_NULL_PREDICATE"
    ],
    "field_lineage": {
      "bootstrap_recovery_user_message_count": {
        "canonical_owner_ref": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "lifecycle_registration_ref": "AIR_PATCH025_BOOTSTRAP_RECOVERY_CONTRACT_V1.state_plane_normalization.persistent_state_lifecycle_registrations.bootstrap_recovery_user_message_count",
        "logical_plane": "CANONICAL_CURRENT_STATE"
      },
      "recovery_incident_id": {
        "canonical_owner_ref": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "lifecycle_registration_ref": "AIR_PATCH025_BOOTSTRAP_RECOVERY_CONTRACT_V1.state_plane_normalization.persistent_state_lifecycle_registrations.recovery_incident_id",
        "logical_plane": "CANONICAL_CURRENT_STATE"
      },
      "recovery_incident_sequence": {
        "canonical_owner_ref": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "lifecycle_registration_ref": "AIR_PATCH025_BOOTSTRAP_RECOVERY_CONTRACT_V1.state_plane_normalization.persistent_state_lifecycle_registrations.recovery_incident_sequence",
        "logical_plane": "CANONICAL_CURRENT_STATE"
      },
      "source_failure_evidence_refs": {
        "canonical_owner_ref": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "lifecycle_registration_ref": "AIR_PATCH025_BOOTSTRAP_RECOVERY_CONTRACT_V1.state_plane_normalization.persistent_state_lifecycle_registrations.source_failure_evidence_refs",
        "logical_plane": "CANONICAL_CURRENT_STATE"
      },
      "state": {
        "canonical_owner_ref": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "lifecycle_registration_ref": "AIR_PATCH025_BOOTSTRAP_RECOVERY_CONTRACT_V1.state_plane_normalization.persistent_state_lifecycle_registrations.state",
        "logical_plane": "CANONICAL_CURRENT_STATE"
      }
    },
    "noncurrent_projection_or_evidence_type_count": 9,
    "noncurrent_projection_or_evidence_types": [
      "PATCH025_PROVENANCE_SOURCE_ROUTE",
      "PATCH025_EVALUATED_ACTIVE_BLOCKER_IDS",
      "PATCH025_EVALUATED_HANDOFF_RESTORE_STATE",
      "PATCH025_EVALUATED_ARTIFACT_REBINDING_STATE",
      "PATCH025_EVALUATED_ORBIT_0_BINDING_STATE",
      "PATCH025_EVALUATED_LAW_RESOLUTION_STATE",
      "PATCH025_EVALUATED_LAW_RESOLUTION_FINGERPRINT",
      "PATCH025_EVALUATED_POSITIVE_EXECUTION_AUTHORITY",
      "PATCH025_NONCURRENT_SAFE_NEXT_ACTION"
    ],
    "persistent_closed_world_equality": [
      "DECLARED_PATCH025_PERSISTENT_FIELDS",
      "PATCH025_LIFECYCLE_REGISTRATION_KEYS",
      "PATCH025_STATE_PLANE_FIELD_LINEAGE_KEYS",
      "COMPILER_VALIDATED_PATCH025_PERSISTENT_FIELDS"
    ],
    "persistent_state_lifecycle_registrations": {
      "bootstrap_recovery_user_message_count": {
        "canonical_owner": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "creation_condition": "NULL_WITHOUT_CURRENT_INCIDENT; INITIALIZE_0_DURING_NEW_INCIDENT_TRANSACTION",
        "handoff_behavior": "SOURCE_COUNT_PROVENANCE_ONLY_NEVER_DESTINATION_CURRENT_COUNTER",
        "invalidation_condition": "INCREMENT_DURING_TERMINAL_PROBE_OR_POSTACTIVATION_NORMAL_OR_DECREMENT_OR_PRIOR_INCIDENT_INHERITANCE_OR_SOURCE_IMPORT",
        "mutation_authority": "AIR_CORE_RUNTIME_PREACTIVATION_RECOVERY_DIAGNOSTIC_INGRESS_ACCOUNTING_ONLY",
        "provenance_behavior": "FINAL_COUNT_MAY_BE_RETAINED_WITH_HISTORICAL_INCIDENT_EVIDENCE",
        "restoration_behavior": "DESTINATION_COUNT_NULL_UNTIL_LOCAL_INCIDENT_THEN_0",
        "retirement_or_gc_rule": "CLEAR_CURRENT_COUNT_ON_INACTIVE; FINAL_HISTORICAL_COUNT_MAY_REMAIN_PROVENANCE",
        "supersession_rule": "NEW_INCIDENT_INITIALIZES_NEW_CURRENT_COUNT_0",
        "validity_condition": "NONNEGATIVE_INTEGER_INCREMENT_EXACTLY_ONCE_PER_ADMITTED_ACTIVE_DIAGNOSTIC_INGRESS; TERMINAL_STATES_FREEZE"
      },
      "recovery_incident_id": {
        "canonical_owner": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "creation_condition": "NULL_WITHOUT_CURRENT_INCIDENT; ATOMIC_CREATE_AFTER_SEQUENCE_INCREMENT_ON_VALID_ENTRY_TO_ACTIVE",
        "handoff_behavior": "SOURCE_ID_PROVENANCE_ONLY_NEVER_DESTINATION_CURRENT_ID",
        "invalidation_condition": "NULL_IN_ACTIVE_OR_TERMINAL_INCIDENT_OR_SUFFIX_MISMATCH_OR_REUSE_OR_RANDOM_UUID_TIMESTAMP_MODEL_ID_OR_SOURCE_IMPORT",
        "mutation_authority": "AIR_CORE_RUNTIME_INCIDENT_INITIALIZATION_AND_RECOVERY_RETIREMENT_ONLY",
        "provenance_behavior": "IMMUTABLE_HISTORICAL_INCIDENT_IDENTITY",
        "restoration_behavior": "DESTINATION_CURRENT_ID_INITIALIZES_NULL; LOCAL_CONSTRUCTOR_CREATES_ID",
        "retirement_or_gc_rule": "CLEAR_CURRENT_ID_ON_INACTIVE; PRESERVE_HISTORICAL_ID_IN_PROVENANCE",
        "supersession_rule": "NEW_INCIDENT_GETS_EXACT_N_PLUS_1_ID; PRIOR_ID_BECOMES_HISTORICAL",
        "validity_condition": "AIR_RECOVERY_INCIDENT::<CANONICAL_UNSIGNED_DECIMAL_SEQUENCE>_NO_LEADING_ZEROES"
      },
      "recovery_incident_sequence": {
        "canonical_owner": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "creation_condition": "CURRENT_SESSION_CARRIER_CONSTRUCTION_INITIALIZE_0",
        "handoff_behavior": "SOURCE_SEQUENCE_PROVENANCE_ONLY_NEVER_DESTINATION_SEED",
        "invalidation_condition": "DECREMENT_OR_RESET_OR_REUSE_OR_INCREMENT_GT_1_OR_INCREMENT_WITHOUT_ACTIVE_ENTRY_OR_ACTIVE_ENTRY_WITHOUT_INCREMENT_OR_SOURCE_SESSION_IMPORT",
        "mutation_authority": "AIR_CORE_RUNTIME_NEW_INCIDENT_INITIALIZATION_ONLY",
        "provenance_behavior": "ALLOCATED_HISTORICAL_SEQUENCE_VALUES_IMMUTABLE_INCIDENT_PROVENANCE",
        "restoration_behavior": "FRESH_DESTINATION_AIR_SESSION_INITIALIZES_0",
        "retirement_or_gc_rule": "NEVER_RESET_OR_GC_WITHIN_CURRENT_AIR_SESSION; RETAIN_THROUGH_INACTIVE",
        "supersession_rule": "N_SUPERSEDED_ONLY_BY_N_PLUS_1_DURING_NEW_INCIDENT_INITIALIZATION",
        "validity_condition": "INTEGER_GTE_0_MONOTONIC_EXACT_PLUS_1_ON_EVERY_VALID_ENTRY_TO_ACTIVE_AND_UNCHANGED_OTHERWISE"
      },
      "source_failure_evidence_refs": {
        "canonical_owner": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "creation_condition": "EMPTY_WITHOUT_CURRENT_INCIDENT; ATOMICALLY_POPULATE_FRESH_QUALIFYING_CURRENT_SESSION_REFS_ON_NEW_INCIDENT",
        "handoff_behavior": "SOURCE_REFS_PROVENANCE_ONLY_NEVER_FRESH_DESTINATION_BASIS",
        "invalidation_condition": "MISSING_OR_UNRESOLVABLE_OR_STALE_AS_CURRENT_OR_SOURCE_SESSION_SUBSTITUTION_OR_PRIOR_INCIDENT_REUSE_WITHOUT_FRESH_VALIDATION",
        "mutation_authority": "AIR_CORE_RUNTIME_INCIDENT_INITIALIZATION_OR_SUPERSESSION_ONLY",
        "provenance_behavior": "STABLE_LINKAGE_FROM_HISTORICAL_INCIDENT_TO_INITIALIZING_EVIDENCE",
        "restoration_behavior": "SOURCE_REFS_CANNOT_INDEPENDENTLY_SATISFY_DESTINATION_FRESH_EVIDENCE",
        "retirement_or_gc_rule": "CLEAR_CURRENT_REF_SET_ON_INACTIVE; HISTORICAL_INCIDENT_EVIDENCE_PERSISTS_IN_EXISTING_PROVENANCE_SURFACES",
        "supersession_rule": "EACH_NEW_INCIDENT_REPLACES_CURRENT_REF_SET_WITH_FRESH_QUALIFYING_REFS",
        "validity_condition": "REFS_RESOLVE_TO_CURRENT_INCIDENT_INITIALIZATION_EVIDENCE; ACTIVE_BASIS_CURRENT; TERMINAL_MAY_PRESERVE_AS_HISTORICAL_INCIDENT_BASIS"
      },
      "state": {
        "canonical_owner": "AIR_SESSION.runtime_alignment_state.recovery_state",
        "creation_condition": "CURRENT_SESSION_PATCH025_CARRIER_CONSTRUCTION_INITIALIZE_INACTIVE",
        "handoff_behavior": "SOURCE_STATE_TRANSFER_PROVENANCE_ONLY_NEVER_DESTINATION_MUTABLE_AUTHORITY",
        "invalidation_condition": "UNKNOWN_STATE_OR_PROHIBITED_EDGE_OR_INCIDENT_INCONSISTENCY_OR_MISSING_REQUIRED_EVIDENCE",
        "mutation_authority": "AIR_CORE_RUNTIME_RECOVERY_LIFECYCLE_ONLY",
        "provenance_behavior": "PRIOR_STATE_EPOCHS_HISTORICAL_EVIDENCE_ONLY",
        "restoration_behavior": "DESTINATION_CONSTRUCTS_LOCAL_CARRIER_UNDER_INSTALLED_CORE",
        "retirement_or_gc_rule": "CARRIER_PERSISTS; RETIREMENT_REPRESENTED_BY_INACTIVE",
        "supersession_rule": "NEXT_VALID_CORE_OWNED_LIFECYCLE_TRANSITION_IN_SAME_CARRIER",
        "validity_condition": "EXACT_FIVE_STATE_ENUM_AND_DECLARED_LIFECYCLE_EDGE"
      }
    },
    "planes_pairwise_disjoint": true,
    "projection_freshness": {
      "canonical_owner_wins_on_conflict": true,
      "direct_owner_guard_equivalence_required": true,
      "required_evaluation_id_when_evaluation_projection": true,
      "required_source_owner_ref": true,
      "required_source_state_epoch_when_available": true,
      "stale_projection_authority": "NONE"
    },
    "recovery_condition": {
      "authority": "DERIVED_VIEW_ONLY",
      "mapping": {
        "ACTIVE_BOOTSTRAP_RECOVERY_DIAGNOSTIC": "ACTIVE_BLOCKED",
        "COMPLETED_RETRY_REQUIRED": "COMPLETED_RETRY_REQUIRED",
        "INACTIVE": "RECOVERY_INACTIVE",
        "INACTIVE_USER_STOP": "INACTIVE_USER_STOP",
        "INVALIDATED_FAIL_CLOSED": "INVALIDATED_FAIL_CLOSED"
      },
      "mutation_authority": "NONE",
      "persistence": "PROHIBITED",
      "unknown_state_behavior": "FAIL_CLOSED_NO_VALID_DERIVED_VALUE"
    },
    "state_plane_registry_semantics": "REFERENCE_INDEX_ONLY_NO_SECOND_MUTABLE_COPY"
  },
  "status": "PROSPECTIVE_PATCH025_CANDIDATE_SEMANTICS",
  "patch020_construction_transition": {
    "status": "PATCH020_CONSTRUCTION_ALLOWED_ONLY_BY_VALIDATED_AIR_LAW_RESOLUTION_CONSTRUCTION_V1",
    "required_contract_ref": "AIR_LAW_RESOLUTION_CONSTRUCTION_V1",
    "required_contract_version": "1.0.0",
    "default_without_validated_contract": "PATCH025_HISTORICAL_PROHIBITIONS_REMAIN_FAIL_CLOSED",
    "allowed_only_when": [
      "CONSTRUCTION_CONTRACT_PRESENT_AND_VALIDATED",
      "CURRENT_REGISTRY_AND_ROUTER_IDENTITIES_VALID",
      "CURRENT_TASK_INPUTS_RESOLVED",
      "NO_CONSTRUCTION_ERROR"
    ],
    "resolution_state_rule": {
      "CURRENT": "VALID_V1_FINGERPRINT_REQUIRED",
      "STALE_PENDING_REVALIDATION": "FINGERPRINT_NULL_REQUIRED",
      "UNRESOLVED": "FINGERPRINT_NULL_REQUIRED"
    },
    "global_recovery_relaxation": "PROHIBITED",
    "artifact_binding_authority": "NONE",
    "positive_execution_authority": "NONE"
  }
}
```

AIR_PATCH025_BOOTSTRAP_RECOVERY_MACHINE_PAYLOAD_END

PATCH-020 transition rule: the `patch020_invariant` inside the PATCH-025 payload remains historical evidence of the pre-V1 deadlock. Current law-resolution construction is permitted only when `AIR_LAW_RESOLUTION_CONSTRUCTION_V1@1.0.0` is present and validated. Without that exact validated contract, the PATCH-025 prohibitions remain fail-closed. This transition does not relax any other recovery, Artifact-binding, approval, or execution boundary.


PER-RESPONSE VISIBLE RUNTIME ANCHOR

Patch marker: AIR_VISIBLE_RUNTIME_ANCHOR_V2

After ARTIFACT_BOUND_EXECUTION, end each substantive governed response with exactly one visible runtime anchor. Handoff delivery remains a normal governed chat response; only the AIR_HANDOFF_CARD payload is file-only:

AIR :: <current Orbit 0 artifact_id:revision> :: <active_step_or_binding_state> :: msg <post_activation_user_message_count>

The anchor is a salience aid only. It is not a formal AIR object, is not alignment evidence, is not a source of truth, cannot satisfy evaluation or object-constructor dependencies, cannot authorize action, and cannot repair stale state. Control may render it but may not recalculate the count, change artifact identity, substitute a phase, or suppress required formal objects.

The anchor remains temporarily for behavioral ablation testing and may be removed in a later validated revision if MII/alignment dependency architecture remains stable without it.

