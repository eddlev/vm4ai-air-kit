--------------------------------------------------
DECISION TRACE JUSTIFICATION AND CLOSURE LAW
--------------------------------------------------

Patch marker: AIR_DECISION_TRACE_JUSTIFICATION_CLOSURE_V1
Floor invariants reinforced: AIR-FLOOR-007-REQUIRED-FORMAL-OBJECT-VISIBILITY, AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY, AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY, AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION, AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE, AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION

A receiver-facing or execution-affecting material decision that depends on interpretive/model judgment is not operative merely because AIR can state a conclusion. When AIR_DECISION_BASIS_CLOSURE_V1 requires a trace, AIR must construct and surface AIR_DECISION_TRACE, close its evidence/rule/authority/uncertainty basis, and independently forced-walk the surfaced basis before the dependent decision may pass.

AIR_DECISION_TRACE is a justification/audit record only. It never represents hidden chain-of-thought, private scratchpad, latent model state, or backend reasoning telemetry; it never grants approval, Gate authority, Authorization, Artifact binding, execution authority, release authority, or publication authority. Deterministically entailed results remain outside the trace requirement unless material interpretive/model judgment is also introduced.

AIR_DECISION_BASIS_CLOSURE_V1_MACHINE_PAYLOAD_BEGIN
```json
{
  "SYSTEM_DESIGNATION": "AIR_DECISION_BASIS_CLOSURE_V1",
  "contract_id": "AIR_DECISION_BASIS_CLOSURE_V1",
  "contract_version": "1.0.0",
  "law_id": "CORE.LAW.DECISION_TRACE_JUSTIFICATION_AND_CLOSURE",
  "law_display_name": "DECISION TRACE JUSTIFICATION AND CLOSURE LAW",
  "law_applicability_class": "CORE_INFRASTRUCTURE_GLOBAL",
  "trace_requirement": {
    "REQUIRED_WHEN": "A receiver-facing or execution-affecting material decision is not uniquely entailed by deterministic machine-contract evaluation and depends on interpretive/model judgment, qualitative comparison, synthetic judge output, recommendation/selection, or exception/resolution judgment.",
    "NOT_REQUIRED_WHEN": "The material result is fully determined by exact deterministic checks such as hash equality, schema/closed-world validation, exact token matching, arithmetic, set/list membership, or another machine contract with a unique result and no interpretive model judgment.",
    "UNRESOLVED_BEHAVIOR": "BLOCK_OPERATIVE_DECISION_AND_ROUTE_REVIEW; do not infer NOT_REQUIRED."
  },
  "hard_invariants": [
    "NO_HIDDEN_MODEL_STATE_CLAIM",
    "NO_CHAIN_OF_THOUGHT_DEPENDENCY",
    "TRACE_NEVER_CREATES_AUTHORITY",
    "MATERIAL_UNSUPPORTED_CLAIM_PREVENTS_PASS",
    "DIVERGENT_OR_UNRESOLVED_ROUTES_TO_REVIEW",
    "CLAIM_SOURCE_CONTRADICTION_FAILS_CLOSED",
    "ORIGINAL_DECISION_WITHHELD_DURING_BASIS_ONLY_RECONSTRUCTION"
  ],
  "closure_checks": [
    "MATERIAL_CLAIM_PROVENANCE_CLOSURE",
    "EVIDENCE_REFERENCE_EXISTENCE_IDENTITY_HASH_STATE",
    "RULE_REFERENCE_EXISTENCE_AND_CURRENT_APPLICABILITY",
    "LAW_RESOLUTION_FINGERPRINT_MATCH",
    "AUTHORITY_STATE_NON_GAIN",
    "UNCERTAINTY_DISCLOSURE",
    "CLAIM_SOURCE_CONSISTENCY",
    "SOURCE_INTENT_INVARIANT_COVERAGE_WHEN_MATERIAL",
    "FORCED_WALK_COMPARISON"
  ],
  "staleness_invalidators": [
    "material_claim_set_change",
    "evidence_identity_or_hash_change",
    "rule_set_or_law_resolution_fingerprint_change",
    "controlling_artifact_revision_or_lease_change",
    "authority_state_change",
    "material_uncertainty_change",
    "decision_subject_or_scope_change"
  ],
  "operative_pass": "trace_state=CURRENT_VERIFIED AND all four closure states PASS AND forced_walk comparison in {EXACT_MATCH,EQUIVALENT}",
  "positive_execution_authority": "NONE",
  "semantic_owner": "AIR_CORE_RUNTIME_V2"
}
```
AIR_DECISION_BASIS_CLOSURE_V1_MACHINE_PAYLOAD_END

AIR_DECISION_TRACE_OBJECT_CONTRACT_V1_MACHINE_PAYLOAD_BEGIN
```json
{
  "SYSTEM_DESIGNATION": "AIR_DECISION_TRACE_OBJECT_CONTRACT_V1",
  "contract_version": "1.0.0",
  "semantic_owner": "AIR_CORE_RUNTIME_V2",
  "formal_object_ref": "AIR_DECISION_TRACE",
  "record_class": "DECISION_JUSTIFICATION_RECORD",
  "object_version": "2.0.0",
  "purpose": "Surface the receiver-visible justification basis for a material model judgment without claiming or exposing hidden chain-of-thought.",
  "required_top_level_fields": [
    "object_version",
    "record_class",
    "runtime_origin",
    "backend_validation_claimed",
    "hidden_reasoning_claimed",
    "evidence_class",
    "evaluation_basis",
    "trace_id",
    "trace_contract_ref",
    "trace_contract_version",
    "controlling_artifact_ref",
    "task_identity_ref",
    "decision_subject_ref",
    "decision_class",
    "trace_requirement_basis",
    "decision_statement",
    "decision_outcome",
    "decision_basis_summary",
    "material_claim_refs",
    "evidence_refs",
    "rule_refs",
    "law_resolution_fingerprint",
    "authority_state_refs",
    "uncertainty_state",
    "uncertainty_refs",
    "provenance_closure_state",
    "rule_closure_state",
    "authority_closure_state",
    "claim_source_consistency_state",
    "forced_walk_state",
    "decision_trace_fingerprint",
    "trace_state",
    "positive_execution_authority"
  ],
  "enum_constraints": {
    "decision_class": [
      "MATERIAL_INTERPRETIVE_JUDGMENT",
      "MATERIAL_MODEL_EVALUATION",
      "MATERIAL_SYNTHETIC_JUDGE_RESULT",
      "MATERIAL_RECOMMENDATION_OR_SELECTION",
      "MATERIAL_EXCEPTION_OR_RESOLUTION"
    ],
    "uncertainty_state": [
      "NONE_MATERIAL",
      "DISCLOSED",
      "UNRESOLVED_MATERIAL"
    ],
    "provenance_closure_state": [
      "PASS",
      "REVIEW",
      "REJECT",
      "UNRESOLVED"
    ],
    "rule_closure_state": [
      "PASS",
      "REVIEW",
      "REJECT",
      "UNRESOLVED"
    ],
    "authority_closure_state": [
      "PASS",
      "REVIEW",
      "REJECT",
      "UNRESOLVED"
    ],
    "claim_source_consistency_state": [
      "PASS",
      "REVIEW",
      "REJECT",
      "UNRESOLVED"
    ],
    "trace_state": [
      "CURRENT_VERIFIED",
      "REVIEW_REQUIRED",
      "REJECTED",
      "STALE_PENDING_REVALIDATION",
      "NONOPERATIVE_HISTORY"
    ],
    "positive_execution_authority": [
      "NONE"
    ]
  },
  "forbidden_fields": [
    "chain_of_thought",
    "reasoning_steps",
    "internal_thoughts",
    "latent_state",
    "hidden_reasoning",
    "private_scratchpad"
  ],
  "decision_basis_summary_semantics": "CONCISE_SURFACED_JUSTIFICATION_BASIS_ONLY_NOT_PRIVATE_REASONING_OR_STEP_BY_STEP_INTERNAL_THOUGHT",
  "trace_requirement_basis_semantics": "EXACT_SURFACED_REFERENCE_TO_WHY_THE_DECISION_TRACE_IS_REQUIRED_UNDER_AIR_DECISION_BASIS_CLOSURE_V1",
  "forced_walk_state_owner": "AIR_DECISION_TRACE_FORCED_WALK_V1",
  "fingerprint_owner": "AIR_DECISION_TRACE_FINGERPRINT_V1",
  "unknown_field_behavior": "INVALID_UNEMITTABLE",
  "positive_execution_authority": "NONE"
}
```
AIR_DECISION_TRACE_OBJECT_CONTRACT_V1_MACHINE_PAYLOAD_END

AIR_DECISION_TRACE_FORCED_WALK_V1_MACHINE_PAYLOAD_BEGIN
```json
{
  "SYSTEM_DESIGNATION": "AIR_DECISION_TRACE_FORCED_WALK_V1",
  "contract_id": "AIR_DECISION_TRACE_FORCED_WALK_V1",
  "contract_version": "1.0.0",
  "purpose": "Reconstruct the admissible decision from surfaced evidence, material-claim provenance, rule closure, authority state and uncertainty without using the original conclusion as authority or exposing hidden chain-of-thought.",
  "phases": [
    {
      "id": "FW1_BASIS_LOCK",
      "requirements": [
        "freeze exact material_claim_refs",
        "freeze exact evidence_refs and source identities/hashes",
        "freeze exact rule_refs and current law_resolution_fingerprint",
        "freeze authority_state_refs",
        "freeze disclosed uncertainty state"
      ]
    },
    {
      "id": "FW2_BASIS_ONLY_RECONSTRUCTION",
      "requirements": [
        "withhold original decision_outcome from verifier input",
        "verify evidence existence/hash/state",
        "verify claim-to-evidence closure",
        "verify rule identity/applicability/currentness",
        "verify authority constraints",
        "derive reconstructed_outcome or UNRESOLVED using surfaced basis only"
      ]
    },
    {
      "id": "FW3_COMPARISON",
      "requirements": [
        "reveal original decision_outcome only after reconstruction",
        "compare operative meaning not wording",
        "classify EXACT_MATCH, EQUIVALENT, DIVERGENT or UNRESOLVED"
      ]
    },
    {
      "id": "FW4_ROUTING",
      "requirements": [
        "EXACT_MATCH or EQUIVALENT may satisfy trace verification only",
        "DIVERGENT or UNRESOLVED routes REVIEW",
        "trace verification never creates approval, Gate, Authorization, Artifact binding or execution authority"
      ]
    }
  ],
  "verification_modes": {
    "DETERMINISTIC_RECONSTRUCTION": "Use when outcome is uniquely determined by machine contracts and exact evidence.",
    "INDEPENDENT_MODEL_EVALUATION": "Use when material interpretation remains model-dependent; record non-deterministic evaluation evidence under the existing AMRS evidence/reproducibility policy."
  },
  "comparison_outcomes": [
    "EXACT_MATCH",
    "EQUIVALENT",
    "DIVERGENT",
    "UNRESOLVED"
  ],
  "hidden_model_state_claim": "PROHIBITED",
  "semantic_owner": "AIR_CORE_RUNTIME_V2",
  "positive_execution_authority": "NONE"
}
```
AIR_DECISION_TRACE_FORCED_WALK_V1_MACHINE_PAYLOAD_END

AIR_DECISION_TRACE_FINGERPRINT_V1_MACHINE_PAYLOAD_BEGIN
```json
{
  "SYSTEM_DESIGNATION": "AIR_DECISION_TRACE_FINGERPRINT_V1",
  "contract_id": "AIR_DECISION_TRACE_FINGERPRINT_V1",
  "algorithm": "SHA-256",
  "representation": "64_LOWERCASE_HEXADECIMAL",
  "canonical_json": {
    "encoding": "UTF-8",
    "duplicate_keys": "PROHIBITED",
    "bom": "PROHIBITED",
    "trailing_newline": "PROHIBITED",
    "insignificant_whitespace": "PROHIBITED",
    "object_key_order": "UNICODE_CODE_POINT_ASCENDING",
    "arrays": "CONTRACT_DEFINED_ORDER",
    "floats_nan_infinity": "PROHIBITED"
  },
  "included_fields": [
    "trace_contract_ref",
    "trace_contract_version",
    "trace_id",
    "controlling_artifact_ref",
    "task_identity_ref",
    "decision_subject_ref",
    "decision_class",
    "trace_requirement_basis",
    "decision_statement",
    "decision_outcome",
    "decision_basis_summary",
    "material_claim_refs",
    "evidence_refs",
    "rule_refs",
    "law_resolution_fingerprint",
    "authority_state_refs",
    "uncertainty_state",
    "uncertainty_refs",
    "provenance_closure_state",
    "rule_closure_state",
    "authority_closure_state",
    "claim_source_consistency_state",
    "forced_walk_state",
    "trace_state"
  ],
  "excluded_fields": [
    "decision_trace_fingerprint",
    "timestamps",
    "presentation_state",
    "positive_execution_authority",
    "backend_validation_claimed",
    "hidden_reasoning_claimed"
  ],
  "semantic_owner": "AIR_CORE_RUNTIME_V2",
  "positive_execution_authority": "NONE"
}
```
AIR_DECISION_TRACE_FINGERPRINT_V1_MACHINE_PAYLOAD_END

