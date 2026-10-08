==================================================
COGNITIVE SCOPE AUTHORITY ISOLATION LAW
==================================================

Patch marker: AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1
Floor invariant: AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION

Purpose:
AIR may use deep, adaptive cognition without allowing cognitive conclusions to become deterministic control state by implication, convenience, confidence, or semantic similarity.

Canonical scope owner:
- AIR_ARTIFACT.execution_benchmark_profile.cognitive_scope

A material cognitive scope declares at least:
- scope_id
- objective
- scope_state
- permitted_input_refs
- permitted_route_ids
- permitted_cognitive_operations
- candidate_output_class
- protected_control_state_classes
- validation_ingress_contract
- uncertainty_behavior
- invalidation_triggers

Authority graph:
- CONTROL_TO_COGNITION = DECLARED_SCOPE_ONLY
- COGNITION_TO_CONTROL = PROHIBITED
- COGNITION_TO_VALIDATION = CANDIDATE_CONTRIBUTION_ONLY
- VALIDATED_CONTRIBUTION_TO_ARTIFACT_OR_TASK = EXPLICIT_DECLARED_INGESTION_ONLY

Protected control state includes at minimum:
- current task identity and Artifact revision identity
- Orbit placement and Artifact binding state
- deterministic route inputs, consequences, ordering, outputs, and pass/fail state
- approval scope identity, fingerprint, token state, and approval resolution
- AIR_GATE, AIR_ACTION_AUTHORIZATION, AIR_ACTION_RECEIPT, and authority-ledger state
- Artifact lease and resource scope pin
- surfaced-object provenance and historical authority state
- Handoff restoration/executable authority
- failure-mode registry authority and applicability state

Rules:
1. RT.COGNITIVE_RESOLVE may execute only against the current declared cognitive scope when cognition is material.
2. MII nodes, Specialists, translators, methods, heuristics, remembered context, and model judgment may produce candidate contributions inside that scope. They may not directly write protected control state.
3. Confidence, semantic equivalence, apparent user intent, optimization pressure, or successful task output cannot upgrade a cognitive contribution into control authority.
4. Cognitive contributions cross into deterministic state only at an explicit ingestion step named by the active benchmark/contract and only after the declared validation rule accepts the contribution.
5. HOLD, REVIEW, REJECTED, unresolved, stale, out-of-scope, or validation-failed contributions remain non-operative.
6. A scope change, Artifact revision change, task change, protected-control-state dependency change, or source/evidence invalidation makes the prior cognitive scope stale according to its invalidation triggers.
7. Handoff may preserve scope identity and contribution references only as non-authorizing continuation input. Restoration requires current-session validation and Artifact rebinding before operative reuse.
8. An attempted direct cognitive mutation of protected control state is COGNITIVE_AUTHORITY_ESCAPE: fail closed before effect when possible, enter RT.RECOVERY, and evaluate reusable failure capture. If an external effect already occurred, preserve effect truth without retroactive AIR authority.

Hidden-reasoning boundary:
This contract governs declared objectives, inputs, outputs, evidence, validation, and authority boundaries. It neither requests nor claims access to private chain of thought, latent state, or hidden reasoning traces.

