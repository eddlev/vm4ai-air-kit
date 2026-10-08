==================================================
MII SEMANTIC TRANSLATION AND FIDELITY LAW
==================================================

Patch marker: AIR_MII_SEMANTIC_TRANSLATION_KERNEL_V1
Patch marker: AIR_MII_SEMANTIC_FIDELITY_V1
Floor invariant: AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY

RT.INPUT_TRANSLATE preserves the raw user input as the evidence of what was said and derives a machine-useful semantic representation without silently replacing meaning.

Protected semantic states:
- RAW_INPUT
- CANONICAL_INTENT
- ACTIVE_CONTEXT
- TASK_BENCHMARK_REPRESENTATION
- PROPOSED_PLAN_OR_ACTION
- OUTPUT_INTERPRETATION

For material work, CANONICAL_INTENT is a typed representation proportional to materiality. It preserves objective, requested_effect, scope, constraints, exclusions, preserved_user_facts, explicit_decisions, contextual_dependencies, authority_permission_assumptions, unresolved_ambiguities, material_semantic_commitments, and source_refs. Missing or unresolved material intent is preserved as missing/unresolved rather than reconstructed from narrative proximity or model preference.

Input translation may identify and classify literal meaning, intended meaning, contextual meaning, idiom/metaphor, constraints, requested effect, ambiguity, and semantic-loss risk. It may clarify, decompose, structure, or enrich meaning. It must not silently narrow, broaden, contradict, substitute, or materially reinterpret intent. Equivalent wording or harmless representation changes are not semantic drift when operative meaning is preserved.

Material semantic deltas use the canonical classes OMISSION, NARROWING, BROADENING, CONTRADICTION, CONSTRAINT_LOSS, EXCLUSION_LOSS, CONTEXT_LOSS, AUTHORITY_CHANGE, REQUESTED_EFFECT_CHANGE, SEMANTIC_SUBSTITUTION, and UNRESOLVED_AMBIGUITY. Equivalence is represented separately and never manufactured to erase a material delta.

Applicable context may include:
- current Orbit 0 task and scope
- Q5/Q6/Q6D state
- user-provided facts and explicit decisions
- current sources/evidence
- approvals, authority boundaries, and known constraints
- unresolved ambiguity
- prior accepted task decisions
- valid handoff-restored state

semantic_fidelity_state is the canonical owner of semantic-fidelity evaluation. Its nested intent_execution_alignment_state is machine-evaluable PASS | REVIEW | REJECT state across INPUT_TO_INTENT, INTENT_TO_TASK, TASK_TO_PLAN, PLAN_TO_ACTION, and ACTION_TO_OUTPUT boundaries. PASS means no detected material semantic transformation changes operative meaning at the evaluated boundary. REVIEW/REJECT routes through existing RT.UNCERTAINTY_RESOLVE, RT.AMEND, or RT.RECOVERY mechanisms as applicable and never grants positive execution authority.

Before any material RT.ACTION, AIR evaluates the proposed action against current CANONICAL_INTENT + ACTIVE_CONTEXT + the bound AIR_ARTIFACT + authority constraints. Before material receiver delivery, AIR reconciles OUTPUT_INTERPRETATION against the same current semantic commitments. DEP.INTENT_EXECUTION_ALIGNMENT_CURRENT is SATISFIED only when the boundary relevant to the route is current and PASS for the exact intent/context/artifact/action-or-output identities being used. Missing, stale, REVIEW, REJECT, contradictory, or materially ambiguous alignment fails closed for the affected route.

Semantic traceability is evidence-bounded: material intent elements and deltas trace only to RAW_INPUT, validated ACTIVE_CONTEXT, explicit user decisions, and authoritative source refs. AIR does not claim access to hidden reasoning or latent model representations as evidence of user meaning.

Universal natural-language intent/context translation is owned by RT.INPUT_TRANSLATE under AIR_MII_SEMANTIC_TRANSLATION_KERNEL_V1 and AIR_MII_SEMANTIC_FIDELITY_V1. AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR_V2 remains a specialized Capability Ecology translator for detailed human roles/frameworks/curricula/competencies/credentials/taxonomies/experience-derived knowledge. It may share this semantic doctrine but must not become a competing universal parser, duplicate Core ownership, or be mandatory for ordinary natural-language translation.

