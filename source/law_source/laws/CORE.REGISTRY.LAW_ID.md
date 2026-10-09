STABLE LAW IDENTITY REGISTRY
--------------------------------------------------

Patch marker: AIR_LAW_ID_REGISTRY_V1
Requirements: LR01, LR03

Core owns stable law identity and semantic source reference. The derived applicability router may select/reject law references but may not rename, redefine, weaken, or synthesize Core law semantics. Existing patch markers remain source/migration anchors, not substitute law IDs. Unknown IDs and conflicting aliases fail closed.

AIR_LAW_ID_REGISTRY_V1_MACHINE_PAYLOAD_BEGIN
```json
{
  "SYSTEM_DESIGNATION": "AIR_LAW_ID_REGISTRY_V1",
  "registry_version": "1.0.0",
  "status": "CORE_2_8_OPERATIVE_STABLE_IDENTITY_REGISTRY",
  "semantic_owner": "AIR_CORE_RUNTIME_V2",
  "authority_class": "CORE_RUNTIME_OPERATIVE_STABLE_IDENTITY_REGISTRY",
  "entry_count": 83,
  "entry_fingerprint_sha256": "915f3f3f03b23106de450b5f5a6480d2122114a21d58c7da32ab769df0cf4686",
  "identity_source": "80 exact routable AIR_P_COMPONENT_METADATA_OVERLAY_V2 IDs + 3 Core identities including Decision Trace",
  "applicability_metadata_authority": "AIR_LAW_APPLICABILITY_ROUTER_V1 derived router; registry entries do not independently infer task applicability",
  "unknown_law_id_behavior": "FAIL_CLOSED",
  "entries": [
    {
      "law_id": "CORE.LAW.RUNTIME_LOAD_INTEGRITY",
      "display_name": "RUNTIME LOAD INTEGRITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.RUNTIME_LOAD_INTEGRITY",
      "source_anchor": {
        "section_heading": "RUNTIME LOAD INTEGRITY LAW",
        "patch_marker": "AIR_LOAD_INTEGRITY_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.BOOT_VALIDATION_PROPORTIONALITY",
      "display_name": "BOOT VALIDATION PROPORTIONALITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.BOOT_VALIDATION_PROPORTIONALITY",
      "source_anchor": {
        "section_heading": "BOOT VALIDATION PROPORTIONALITY LAW",
        "patch_marker": "AIR_BOOT_VALIDATION_PROPORTIONALITY_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.OPERATIVE_COMPATIBILITY_AUTHORITY",
      "display_name": "OPERATIVE COMPATIBILITY AUTHORITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.OPERATIVE_COMPATIBILITY_AUTHORITY",
      "source_anchor": {
        "section_heading": "OPERATIVE COMPATIBILITY AUTHORITY LAW",
        "patch_marker": "AIR_OPERATIVE_COMPATIBILITY_AUTHORITY_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.CANONICAL_FILE_IDENTITY_DELIVERY_INTEGRITY",
      "display_name": "CANONICAL FILE IDENTITY AND DELIVERY INTEGRITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.CANONICAL_FILE_IDENTITY_DELIVERY_INTEGRITY",
      "source_anchor": {
        "section_heading": "CANONICAL FILE IDENTITY AND DELIVERY INTEGRITY LAW",
        "patch_marker": "AIR_CANONICAL_FILE_IDENTITY_DELIVERY_INTEGRITY_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.REGISTRY.FLOOR_INVARIANT",
      "display_name": "FLOOR INVARIANT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.REGISTRY.FLOOR_INVARIANT",
      "source_anchor": {
        "section_heading": "FLOOR INVARIANT LAW",
        "patch_marker": "AIR_FLOOR_INVARIANT_REGISTRY_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.NON_INFERENCE_MATERIAL_AMBIGUITY",
      "display_name": "NON-INFERENCE UNDER UNRESOLVED MATERIAL AMBIGUITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.NON_INFERENCE_MATERIAL_AMBIGUITY",
      "source_anchor": {
        "section_heading": "NON-INFERENCE UNDER UNRESOLVED MATERIAL AMBIGUITY LAW",
        "patch_marker": "AIR_NON_INFERENCE_MATERIAL_AMBIGUITY_H1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.CONTROL_PLANE_SEMANTIC_NON_AUTHORITY",
      "display_name": "CONTROL-PLANE SEMANTIC NON-AUTHORITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.CONTROL_PLANE_SEMANTIC_NON_AUTHORITY",
      "source_anchor": {
        "section_heading": "CONTROL-PLANE SEMANTIC NON-AUTHORITY LAW",
        "patch_marker": "AIR_RUNTIME_CONTROL_EVENT_REGISTRY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.HANDOFF_MODE_SELECTION",
      "display_name": "HANDOFF MODE SELECTION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.HANDOFF_MODE_SELECTION",
      "source_anchor": {
        "section_heading": "HANDOFF MODE SELECTION LAW",
        "patch_marker": "AIR_HANDOFF_MODE_SELECTION_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.HANDOFF_RUNTIME_DURABILITY_GENERATION",
      "display_name": "HANDOFF RUNTIME DURABILITY AND GENERATION CONTRACT",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.HANDOFF_RUNTIME_DURABILITY_GENERATION",
      "source_anchor": {
        "section_heading": "HANDOFF RUNTIME DURABILITY AND GENERATION CONTRACT",
        "patch_marker": "AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.DURABLE_SURFACED_OBJECT_PROVENANCE",
      "display_name": "DURABLE SURFACED-OBJECT PROVENANCE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.DURABLE_SURFACED_OBJECT_PROVENANCE",
      "source_anchor": {
        "section_heading": "DURABLE SURFACED-OBJECT PROVENANCE LAW",
        "patch_marker": "AIR_DURABLE_SURFACED_OBJECT_PROVENANCE_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.HANDOFF_FILE_DELIVERY",
      "display_name": "HANDOFF JSON FILE OUTPUT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.HANDOFF_FILE_DELIVERY",
      "source_anchor": {
        "section_heading": "HANDOFF JSON FILE OUTPUT LAW",
        "patch_marker": "AIR_HANDOFF_FILE_DELIVERY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.COGNITIVE_SCOPE_AUTHORITY_ISOLATION",
      "display_name": "COGNITIVE SCOPE AUTHORITY ISOLATION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.COGNITIVE_SCOPE_AUTHORITY_ISOLATION",
      "source_anchor": {
        "section_heading": "COGNITIVE SCOPE AUTHORITY ISOLATION LAW",
        "patch_marker": "AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.DETERMINISTIC_PIPELINE_NON_INFERENCE",
      "display_name": "DETERMINISTIC PIPELINE NON-INFERENCE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.DETERMINISTIC_PIPELINE_NON_INFERENCE",
      "source_anchor": {
        "section_heading": "DETERMINISTIC PIPELINE NON-INFERENCE LAW",
        "patch_marker": "AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.DETERMINISTIC_CONTRACT_MACHINE_REPRESENTATION",
      "display_name": "DETERMINISTIC CONTRACT MACHINE REPRESENTATION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.DETERMINISTIC_CONTRACT_MACHINE_REPRESENTATION",
      "source_anchor": {
        "section_heading": "DETERMINISTIC CONTRACT MACHINE REPRESENTATION LAW",
        "patch_marker": "AIR_DETERMINISTIC_CONTRACT_MACHINE_REPRESENTATION_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ACTIVE_STATE_RECONCILIATION",
      "display_name": "ACTIVE-STATE RECONCILIATION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ACTIVE_STATE_RECONCILIATION",
      "source_anchor": {
        "section_heading": "ACTIVE-STATE RECONCILIATION LAW",
        "patch_marker": "AIR_ACTIVE_STATE_RECONCILIATION_H2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.REGISTRY.RUNTIME_ROUTE_DEPENDENCY_KERNEL",
      "display_name": "AIR ROUTE AND DEPENDENCY KERNEL",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.REGISTRY.RUNTIME_ROUTE_DEPENDENCY_KERNEL",
      "source_anchor": {
        "section_heading": "AIR ROUTE AND DEPENDENCY KERNEL",
        "patch_marker": "AIR_ROUTE_DEPENDENCY_KERNEL_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ALIGNMENT_EVALUATION_DEPENDENCY",
      "display_name": "ALIGNMENT EVALUATION DEPENDENCY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ALIGNMENT_EVALUATION_DEPENDENCY",
      "source_anchor": {
        "section_heading": "ALIGNMENT EVALUATION DEPENDENCY LAW",
        "patch_marker": "AIR_ALIGNMENT_EVALUATION_DEPENDENCY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY",
      "display_name": "FORMAL OBJECT CONSTRUCTOR DEPENDENCY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY",
      "source_anchor": {
        "section_heading": "FORMAL OBJECT CONSTRUCTOR DEPENDENCY LAW",
        "patch_marker": "AIR_FORMAL_OBJECT_CONSTRUCTOR_DEPENDENCY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.MII_COGNITIVE_ARCHITECTURE",
      "display_name": "AIR MII COGNITIVE ARCHITECTURE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.MII_COGNITIVE_ARCHITECTURE",
      "source_anchor": {
        "section_heading": "AIR MII COGNITIVE ARCHITECTURE LAW",
        "patch_marker": "AIR_MII_COGNITIVE_ARCHITECTURE_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.MII_SEMANTIC_TRANSLATION_AND_FIDELITY",
      "display_name": "MII SEMANTIC TRANSLATION AND FIDELITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.MII_SEMANTIC_TRANSLATION_AND_FIDELITY",
      "source_anchor": {
        "section_heading": "MII SEMANTIC TRANSLATION AND FIDELITY LAW",
        "patch_marker": "AIR_MII_SEMANTIC_TRANSLATION_KERNEL_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.MII_EPISTEMIC_SUFFICIENCY",
      "display_name": "MII EPISTEMIC SUFFICIENCY AND CLARIFICATION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.MII_EPISTEMIC_SUFFICIENCY",
      "source_anchor": {
        "section_heading": "MII EPISTEMIC SUFFICIENCY AND CLARIFICATION LAW",
        "patch_marker": "AIR_MII_EPISTEMIC_SUFFICIENCY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.MII_MORPHOLOGY_BINDING",
      "display_name": "MII MORPHOLOGY BINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.MII_MORPHOLOGY_BINDING",
      "source_anchor": {
        "section_heading": "MII MORPHOLOGY BINDING LAW",
        "patch_marker": "AIR_MII_MORPHOLOGY_BINDING_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.MII_RISK_PROPAGATION",
      "display_name": "MII RISK PROPAGATION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.MII_RISK_PROPAGATION",
      "source_anchor": {
        "section_heading": "MII RISK PROPAGATION LAW",
        "patch_marker": "AIR_MII_RISK_PROPAGATION_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.HANDOFF_INBOUND_VALIDATION",
      "display_name": "INBOUND CARD VALIDATION GATE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.HANDOFF_INBOUND_VALIDATION",
      "source_anchor": {
        "section_heading": "INBOUND CARD VALIDATION GATE LAW",
        "patch_marker": "AIR_HANDOFF_INBOUND_VALIDATION_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ENTRY_PATH_Q1_SEPARATION",
      "display_name": "ENTRY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ENTRY_PATH_Q1_SEPARATION",
      "source_anchor": {
        "section_heading": "ENTRY LAW",
        "patch_marker": "AIR_ENTRY_PATH_Q1_SEPARATION_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.DETERMINISTIC_ONBOARDING_NON_INFERENCE",
      "display_name": "DETERMINISTIC ONBOARDING NON-INFERENCE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.DETERMINISTIC_ONBOARDING_NON_INFERENCE",
      "source_anchor": {
        "section_heading": "DETERMINISTIC ONBOARDING NON-INFERENCE LAW",
        "patch_marker": "DETERMINISTIC_ONBOARDING_NON_INFERENCE_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.CANONICAL_INTENT_RESOLUTION_GATE",
      "display_name": "CANONICAL INTENT RESOLUTION GATE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.CANONICAL_INTENT_RESOLUTION_GATE",
      "source_anchor": {
        "section_heading": "CANONICAL INTENT RESOLUTION GATE LAW",
        "patch_marker": "AIR_INTENT_RESOLUTION_GATE_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ONBOARDING_GEOMETRY_ROUTING_MATRIX",
      "display_name": "ONBOARDING GEOMETRY ROUTING MATRIX LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ONBOARDING_GEOMETRY_ROUTING_MATRIX",
      "source_anchor": {
        "section_heading": "ONBOARDING GEOMETRY ROUTING MATRIX LAW",
        "patch_marker": "AIR_ONBOARDING_GEOMETRY_ROUTING_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ROUTER_COMPATIBILITY_SURFACE",
      "display_name": "ROUTER LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ROUTER_COMPATIBILITY_SURFACE",
      "source_anchor": {
        "section_heading": "ROUTER LAW",
        "patch_marker": "AIR_ROUTER_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.CREATIVE_CONTINUITY_EXTENSION",
      "display_name": "CREATIVE CONTINUITY EXTENSION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.CREATIVE_CONTINUITY_EXTENSION",
      "source_anchor": {
        "section_heading": "CREATIVE CONTINUITY EXTENSION LAW",
        "patch_marker": "AIR_CREATIVE_CONTINUITY_EXTENSION_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.CANONICAL_OBJECT_CONTRACT",
      "display_name": "CANONICAL AIR OBJECT CONTRACT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.CANONICAL_OBJECT_CONTRACT",
      "source_anchor": {
        "section_heading": "CANONICAL AIR OBJECT CONTRACT LAW",
        "patch_marker": "AIR_CANONICAL_OBJECT_CONTRACTS_V4"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.HANDOFF_CONTINUATION_BOOTSTRAP",
      "display_name": "HANDOFF CONTINUATION FLOW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.HANDOFF_CONTINUATION_BOOTSTRAP",
      "source_anchor": {
        "section_heading": "HANDOFF CONTINUATION FLOW",
        "patch_marker": "AIR_HANDOFF_CONTINUATION_BOOTSTRAP_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.HANDOFF_JSON_FILE_OUTPUT",
      "display_name": "HANDOFF JSON FILE OUTPUT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.HANDOFF_JSON_FILE_OUTPUT",
      "source_anchor": {
        "section_heading": "HANDOFF JSON FILE OUTPUT LAW",
        "patch_marker": "AIR_HANDOFF_STRICT_JSON_OUTPUT_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ORBIT0_PROMPT_SIDE_ANCHORING",
      "display_name": "ORBIT 0 PROMPT-SIDE ANCHORING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ORBIT0_PROMPT_SIDE_ANCHORING",
      "source_anchor": {
        "section_heading": "ORBIT 0 PROMPT-SIDE ANCHORING LAW",
        "patch_marker": "AIR_ORBIT0_PROMPT_SIDE_ANCHORING_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.BENCHMARK_SYNTHETIC_ROLE",
      "display_name": "BENCHMARK SYNTHETIC ROLE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.BENCHMARK_SYNTHETIC_ROLE",
      "source_anchor": {
        "section_heading": "BENCHMARK SYNTHETIC ROLE LAW",
        "patch_marker": "AIR_BENCHMARK_SYNTHETIC_ROLE_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.MACHINE_NATIVE_CAPABILITY_TRANSLATION_KERNEL",
      "display_name": "MACHINE-NATIVE CAPABILITY TRANSLATION KERNEL",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.MACHINE_NATIVE_CAPABILITY_TRANSLATION_KERNEL",
      "source_anchor": {
        "section_heading": "MACHINE-NATIVE CAPABILITY TRANSLATION KERNEL",
        "patch_marker": "AIR_MACHINE_NATIVE_CAPABILITY_TRANSLATION_KERNEL_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.KNOWLEDGE_TO_EXECUTION_TRANSFORMATION_PATH",
      "display_name": "KNOWLEDGE-TO-EXECUTION TRANSFORMATION PATH LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.KNOWLEDGE_TO_EXECUTION_TRANSFORMATION_PATH",
      "source_anchor": {
        "section_heading": "KNOWLEDGE-TO-EXECUTION TRANSFORMATION PATH LAW",
        "patch_marker": "AIR_KNOWLEDGE_TO_EXECUTION_PATH_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.PATCH_SOURCE_UPLOAD_GATE",
      "display_name": "PATCH SOURCE UPLOAD GATE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.PATCH_SOURCE_UPLOAD_GATE",
      "source_anchor": {
        "section_heading": "PATCH SOURCE UPLOAD GATE LAW",
        "patch_marker": "AIR_PATCH_SOURCE_UPLOAD_GATE_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.OBJECT_VISIBILITY_AND_BOOT_EVIDENCE",
      "display_name": "AIR OBJECT VISIBILITY AND BOOT EVIDENCE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.OBJECT_VISIBILITY_AND_BOOT_EVIDENCE",
      "source_anchor": {
        "section_heading": "AIR OBJECT VISIBILITY AND BOOT EVIDENCE LAW",
        "patch_marker": "AIR_OBJECT_VISIBILITY_BOOT_EVIDENCE_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.SYSTEM_MODIFIERS",
      "display_name": "AIR SYSTEM MODIFIER LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.SYSTEM_MODIFIERS",
      "source_anchor": {
        "section_heading": "AIR SYSTEM MODIFIER LAW",
        "patch_marker": "AIR_MINIMAL_SYSTEM_MODIFIERS_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.OBJECT_DEFAULT_PRECEDENCE_AND_ONBOARDING_LOCK",
      "display_name": "AIR OBJECT DEFAULT PRECEDENCE AND ONBOARDING LOCK LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.OBJECT_DEFAULT_PRECEDENCE_AND_ONBOARDING_LOCK",
      "source_anchor": {
        "section_heading": "AIR OBJECT DEFAULT PRECEDENCE AND ONBOARDING LOCK LAW",
        "patch_marker": "AIR_OBJECT_DEFAULT_PRECEDENCE_ONBOARDING_LOCK_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.SPECIALIST_PROFILE_ROUTING",
      "display_name": "SPECIALIST PROFILE ROUTING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.SPECIALIST_PROFILE_ROUTING",
      "source_anchor": {
        "section_heading": "SPECIALIST PROFILE ROUTING LAW",
        "patch_marker": "AIR_SPECIALIST_ROUTING_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.PROFILE_STACK_ROUTING",
      "display_name": "PROFILE STACK ROUTING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.PROFILE_STACK_ROUTING",
      "source_anchor": {
        "section_heading": "PROFILE STACK ROUTING LAW",
        "patch_marker": "ACTIVE_TASK_GEOMETRY_FLUX_SPECIALIST_ROUTING_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.CAPABILITY_LAYER_NEED_DETECTION",
      "display_name": "CAPABILITY LAYER NEED DETECTION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.CAPABILITY_LAYER_NEED_DETECTION",
      "source_anchor": {
        "section_heading": "CAPABILITY LAYER NEED DETECTION LAW",
        "patch_marker": "AIR_CAPABILITY_LAYER_NEED_DETECTION_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.SPECIALIST_CAPABILITY_RESOLUTION",
      "display_name": "SPECIALIST CAPABILITY RESOLUTION ROUTER",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.SPECIALIST_CAPABILITY_RESOLUTION",
      "source_anchor": {
        "section_heading": "SPECIALIST CAPABILITY RESOLUTION ROUTER",
        "patch_marker": "AIR_SPECIALIST_CAPABILITY_RESOLUTION_ROUTER_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.REGISTRY.SPECIALIST_PACKAGE_INDEX_DISCOVERY",
      "display_name": "AIR SPECIALIST PACKAGE INDEX DISCOVERY CONTRACT",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.REGISTRY.SPECIALIST_PACKAGE_INDEX_DISCOVERY",
      "source_anchor": {
        "section_heading": "AIR SPECIALIST PACKAGE INDEX DISCOVERY CONTRACT",
        "patch_marker": "AIR_SPECIALIST_PACKAGE_INDEX_DISCOVERY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.REQUIRED_INPUT_ARTIFACT_ACQUISITION",
      "display_name": "REQUIRED INPUT AND ARTIFACT ACQUISITION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.REQUIRED_INPUT_ARTIFACT_ACQUISITION",
      "source_anchor": {
        "section_heading": "REQUIRED INPUT AND ARTIFACT ACQUISITION LAW",
        "patch_marker": "AIR_REQUIRED_INPUT_ARTIFACT_ACQUISITION_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.RESPONSIVE_BINDING_APPROVAL",
      "display_name": "RESPONSIVE BINDING APPROVAL LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.RESPONSIVE_BINDING_APPROVAL",
      "source_anchor": {
        "section_heading": "RESPONSIVE BINDING APPROVAL LAW",
        "patch_marker": "AIR_RESPONSIVE_BINDING_APPROVAL_M1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.METHOD_LAYER",
      "display_name": "AIR METHOD LAYER LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.METHOD_LAYER",
      "source_anchor": {
        "section_heading": "AIR METHOD LAYER LAW",
        "patch_marker": "AIR_METHOD_LAYER_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.SPECIALIST_DOMAIN_PACKAGE_BINDING",
      "display_name": "SPECIALIST DOMAIN PACKAGE BINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.SPECIALIST_DOMAIN_PACKAGE_BINDING",
      "source_anchor": {
        "section_heading": "SPECIALIST DOMAIN PACKAGE BINDING LAW",
        "patch_marker": "AIR_SPECIALIST_PACKAGE_BINDING_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ORBIT_TASK_MANAGEMENT",
      "display_name": "ORBIT TASK MANAGEMENT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ORBIT_TASK_MANAGEMENT",
      "source_anchor": {
        "section_heading": "ORBIT TASK MANAGEMENT LAW",
        "patch_marker": "AIR_ORBIT_TASK_MANAGEMENT_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.PROMPT_RUNTIME_ACTIVATION_PERSISTENCE",
      "display_name": "PROMPT RUNTIME ACTIVATION PERSISTENCE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.PROMPT_RUNTIME_ACTIVATION_PERSISTENCE",
      "source_anchor": {
        "section_heading": "PROMPT RUNTIME ACTIVATION PERSISTENCE LAW",
        "patch_marker": "AIR_PROMPT_RUNTIME_PERSISTENCE_H1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ARTIFACT_SOLE_EXECUTION_BINDING",
      "display_name": "SOLE AIR_ARTIFACT EXECUTION BINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ARTIFACT_SOLE_EXECUTION_BINDING",
      "source_anchor": {
        "section_heading": "SOLE AIR_ARTIFACT EXECUTION BINDING LAW",
        "patch_marker": "AIR_ARTIFACT_SOLE_EXECUTION_BINDING_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.NEW_TASK_EXECUTION_BINDING_BARRIER",
      "display_name": "NEW TASK EXECUTION BINDING BARRIER LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.NEW_TASK_EXECUTION_BINDING_BARRIER",
      "source_anchor": {
        "section_heading": "NEW TASK EXECUTION BINDING BARRIER LAW",
        "patch_marker": "AIR_NEW_TASK_BINDING_BARRIER_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.GATE_DECISION",
      "display_name": "AIR GATE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.GATE_DECISION",
      "source_anchor": {
        "section_heading": "AIR GATE LAW",
        "patch_marker": "AIR_GATE_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.GEOMETRY_EFFECT_BINDING",
      "display_name": "GEOMETRY EFFECT BINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.GEOMETRY_EFFECT_BINDING",
      "source_anchor": {
        "section_heading": "GEOMETRY EFFECT BINDING LAW",
        "patch_marker": "AIR_GEOMETRY_EFFECT_BINDING_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.LAMBDA_PRESSURE_BINDING",
      "display_name": "LAMBDA PRESSURE BINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.LAMBDA_PRESSURE_BINDING",
      "source_anchor": {
        "section_heading": "LAMBDA PRESSURE BINDING LAW",
        "patch_marker": "AIR_LAMBDA_PRESSURE_BINDING_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.GEOMETRY_FORCE_VS_FIT",
      "display_name": "GEOMETRY FORCE VS FIT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.GEOMETRY_FORCE_VS_FIT",
      "source_anchor": {
        "section_heading": "GEOMETRY FORCE VS FIT LAW",
        "patch_marker": "ACTIVE_TASK_GEOMETRY_FLUX_SPECIALIST_ROUTING_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ACTIVE_TASK_GEOMETRY_REBINDING",
      "display_name": "ACTIVE TASK GEOMETRY REBINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ACTIVE_TASK_GEOMETRY_REBINDING",
      "source_anchor": {
        "section_heading": "ACTIVE TASK GEOMETRY REBINDING LAW",
        "patch_marker": "AIR_ACTIVE_TASK_GEOMETRY_REBINDING_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.DUAL_GEOMETRY_BINDING",
      "display_name": "DUAL GEOMETRY BINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.DUAL_GEOMETRY_BINDING",
      "source_anchor": {
        "section_heading": "DUAL GEOMETRY BINDING LAW",
        "patch_marker": "Q4D_DUAL_GEOMETRY_FAMILIAR_ARTIFACT_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.NATIVE_AXIS_SCAN",
      "display_name": "NATIVE AXIS SCAN LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.NATIVE_AXIS_SCAN",
      "source_anchor": {
        "section_heading": "NATIVE AXIS SCAN LAW",
        "patch_marker": "AIR_NATIVE_AXIS_SCAN_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.NATIVE_MEANING_ALIGNMENT_LITE",
      "display_name": "NATIVE MEANING ALIGNMENT LITE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.NATIVE_MEANING_ALIGNMENT_LITE",
      "source_anchor": {
        "section_heading": "NATIVE MEANING ALIGNMENT LITE LAW",
        "patch_marker": "AIR_NATIVE_MEANING_ALIGNMENT_LITE_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.BENCHMARK_JUDGE",
      "display_name": "BENCHMARK JUDGE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.BENCHMARK_JUDGE",
      "source_anchor": {
        "section_heading": "BENCHMARK JUDGE LAW",
        "patch_marker": "AIR_BENCHMARK_JUDGE_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.AMBIGUITY_TRIAGE_GATE",
      "display_name": "AMBIGUITY TRIAGE GATE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.AMBIGUITY_TRIAGE_GATE",
      "source_anchor": {
        "section_heading": "AMBIGUITY TRIAGE GATE LAW",
        "patch_marker": "AIR_AMBIGUITY_TRIAGE_GATE_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.AMRS_STAGE_COMPLETION_STEP_OPTIMALITY",
      "display_name": "AMRS STAGE COMPLETION AND STEP-OPTIMALITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.AMRS_STAGE_COMPLETION_STEP_OPTIMALITY",
      "source_anchor": {
        "section_heading": "AMRS STAGE COMPLETION AND STEP-OPTIMALITY LAW",
        "patch_marker": "AIR_AMRS_TARGET_READINESS_STEP_OPTIMALITY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.VISIBLE_ARTIFACT_BINDING",
      "display_name": "VISIBLE ARTIFACT BINDING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.VISIBLE_ARTIFACT_BINDING",
      "source_anchor": {
        "section_heading": "VISIBLE ARTIFACT BINDING LAW",
        "patch_marker": "AIR_VISIBLE_ARTIFACT_BINDING_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.MATERIAL_ACTION_INTERLOCK",
      "display_name": "MATERIAL ACTION INTERLOCK LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.MATERIAL_ACTION_INTERLOCK",
      "source_anchor": {
        "section_heading": "MATERIAL ACTION INTERLOCK LAW",
        "patch_marker": "AIR_MATERIAL_ACTION_INTERLOCK_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ARTIFACT_LEASE_INVALIDATION",
      "display_name": "ARTIFACT LEASE AND INVALIDATION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ARTIFACT_LEASE_INVALIDATION",
      "source_anchor": {
        "section_heading": "ARTIFACT LEASE AND INVALIDATION LAW",
        "patch_marker": "AIR_ARTIFACT_LEASE_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.RESOURCE_SCOPE_PIN",
      "display_name": "RESOURCE SCOPE PIN LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.RESOURCE_SCOPE_PIN",
      "source_anchor": {
        "section_heading": "RESOURCE SCOPE PIN LAW",
        "patch_marker": "AIR_RESOURCE_SCOPE_PIN_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.ACTION_RECEIPT_RECONCILIATION",
      "display_name": "ACTION RECEIPT AND RECONCILIATION LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.ACTION_RECEIPT_RECONCILIATION",
      "source_anchor": {
        "section_heading": "ACTION RECEIPT AND RECONCILIATION LAW",
        "patch_marker": "AIR_ACTION_RECEIPT_RECONCILIATION_V4"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.UNBOUND_PRIOR_EFFECT_RECOVERY",
      "display_name": "UNBOUND PRIOR EFFECT RECOVERY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.UNBOUND_PRIOR_EFFECT_RECOVERY",
      "source_anchor": {
        "section_heading": "UNBOUND PRIOR EFFECT RECOVERY LAW",
        "patch_marker": "AIR_UNBOUND_PRIOR_EFFECT_RECOVERY_V3"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.RUNTIME_ALIGNMENT_STATE",
      "display_name": "RUNTIME ALIGNMENT STATE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.RUNTIME_ALIGNMENT_STATE",
      "source_anchor": {
        "section_heading": "RUNTIME ALIGNMENT STATE LAW",
        "patch_marker": "AIR_RUNTIME_ALIGNMENT_STATE_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.TOOL_GATEWAY_ENFORCEMENT_BOUNDARY",
      "display_name": "TOOL GATEWAY ENFORCEMENT BOUNDARY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.TOOL_GATEWAY_ENFORCEMENT_BOUNDARY",
      "source_anchor": {
        "section_heading": "TOOL GATEWAY ENFORCEMENT BOUNDARY LAW",
        "patch_marker": "AIR_TOOL_GATEWAY_ENFORCEMENT_BOUNDARY_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.REQUIRED_FORMAL_OBJECT_EMISSION_PREFLIGHT",
      "display_name": "REQUIRED FORMAL OBJECT EMISSION PREFLIGHT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.REQUIRED_FORMAL_OBJECT_EMISSION_PREFLIGHT",
      "source_anchor": {
        "section_heading": "REQUIRED FORMAL OBJECT EMISSION PREFLIGHT LAW",
        "patch_marker": "AIR_REQUIRED_EMISSION_PREFLIGHT_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.CLOSED_WORLD_FORMAL_OBJECT_EMISSION_CLOSURE",
      "display_name": "CLOSED-WORLD FORMAL OBJECT EMISSION CLOSURE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.CLOSED_WORLD_FORMAL_OBJECT_EMISSION_CLOSURE",
      "source_anchor": {
        "section_heading": "CLOSED-WORLD FORMAL OBJECT EMISSION CLOSURE LAW",
        "patch_marker": "AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.FORMAL_OBJECT_COMPLETENESS_PREFLIGHT",
      "display_name": "FORMAL OBJECT COMPLETENESS PREFLIGHT LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.FORMAL_OBJECT_COMPLETENESS_PREFLIGHT",
      "source_anchor": {
        "section_heading": "FORMAL OBJECT COMPLETENESS PREFLIGHT LAW",
        "patch_marker": "AIR_FORMAL_OBJECT_COMPLETENESS_PREFLIGHT_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.VISIBLE_CHANNEL_EMISSION_INTEGRITY",
      "display_name": "VISIBLE CHANNEL EMISSION INTEGRITY LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.VISIBLE_CHANNEL_EMISSION_INTEGRITY",
      "source_anchor": {
        "section_heading": "VISIBLE CHANNEL EMISSION INTEGRITY LAW",
        "patch_marker": "AIR_VISIBLE_CHANNEL_EMISSION_INTEGRITY_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.GROUNDING_Q5_SPECIALIST_NEED_CHECK",
      "display_name": "AIR GROUNDING DOCTRINE AND Q5 SPECIALIST NEED CHECK LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.GROUNDING_Q5_SPECIALIST_NEED_CHECK",
      "source_anchor": {
        "section_heading": "AIR GROUNDING DOCTRINE AND Q5 SPECIALIST NEED CHECK LAW",
        "patch_marker": "AIR_GROUNDING_Q5_SPECIALIST_NEED_CHECK_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.AI_GOVERNANCE_SPECIALIST_PACKAGE_REGULATORY_EVIDENCE_ROUTING",
      "display_name": "AIR AI GOVERNANCE SPECIALIST PACKAGE AND REGULATORY EVIDENCE ROUTING LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.AI_GOVERNANCE_SPECIALIST_PACKAGE_REGULATORY_EVIDENCE_ROUTING",
      "source_anchor": {
        "section_heading": "AIR AI GOVERNANCE SPECIALIST PACKAGE AND REGULATORY EVIDENCE ROUTING LAW",
        "patch_marker": "AIR_AI_GOVERNANCE_PACKAGE_ROUTING_V2"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.BEHAVIORAL_TRANSACTION_HARDENING_SET_005",
      "display_name": "SET_005 BEHAVIORAL TRANSACTION HARDENING",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.BEHAVIORAL_TRANSACTION_HARDENING_SET_005",
      "source_anchor": {
        "section_heading": "SET_005 BEHAVIORAL TRANSACTION HARDENING",
        "patch_marker": "AIR_TRANSITION_EMISSION_TRANSACTION_V1"
      },
      "applicability_class": "ROUTABLE_IDENTITY_DERIVED_ROUTER_METADATA_REQUIRED",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "DERIVED_ROUTER_OWNED_NOT_CORE_REGISTRY"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.REGISTRY.LAW_ID",
      "display_name": "Core Stable Law Identity Registry",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.REGISTRY.LAW_ID",
      "source_anchor": {
        "section_heading": "AMRS-6 CORE 2.8 SEMANTIC ACTIVATION LAW",
        "patch_marker": "AIR_LAW_ID_REGISTRY_V1"
      },
      "applicability_class": "CORE_INFRASTRUCTURE_GLOBAL",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "GLOBAL_INFRASTRUCTURE"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.AMRS_AWARE_LAW_APPLICABILITY",
      "display_name": "AMRS-Aware Law Applicability Router Law",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.AMRS_AWARE_LAW_APPLICABILITY",
      "source_anchor": {
        "section_heading": "AMRS-6 CORE 2.8 SEMANTIC ACTIVATION LAW",
        "patch_marker": "AIR_LAW_APPLICABILITY_ROUTER_V1"
      },
      "applicability_class": "CORE_INFRASTRUCTURE_GLOBAL",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "GLOBAL_INFRASTRUCTURE"
      },
      "mandatory_floor_refs": [],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    },
    {
      "law_id": "CORE.LAW.DECISION_TRACE_JUSTIFICATION_AND_CLOSURE",
      "display_name": "DECISION TRACE JUSTIFICATION AND CLOSURE LAW",
      "semantic_owner": "AIR_CORE_RUNTIME_V2",
      "source_component_ref": "CORE.LAW.DECISION_TRACE_JUSTIFICATION_AND_CLOSURE",
      "source_anchor": {
        "section_heading": "DECISION TRACE JUSTIFICATION AND CLOSURE LAW",
        "patch_marker": "AIR_DECISION_TRACE_JUSTIFICATION_CLOSURE_V1"
      },
      "applicability_class": "CORE_INFRASTRUCTURE_GLOBAL",
      "task_class_predicates": [],
      "task_target_amrs_predicate": {
        "state": "GLOBAL_INFRASTRUCTURE"
      },
      "mandatory_floor_refs": [
        "AIR-FLOOR-007-REQUIRED-FORMAL-OBJECT-VISIBILITY",
        "AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY",
        "AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY",
        "AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION",
        "AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE",
        "AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION"
      ],
      "dependency_law_refs": [],
      "runtime_route_refs": [],
      "runtime_dependency_refs": [],
      "control_event_refs": [],
      "legacy_aliases": [],
      "supersedes": null,
      "lifecycle_state": "ACTIVE"
    }
  ]
}
```
AIR_LAW_ID_REGISTRY_V1_MACHINE_PAYLOAD_END
