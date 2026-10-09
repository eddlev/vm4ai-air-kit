==================================================
DETERMINISTIC CONTRACT MACHINE REPRESENTATION LAW
==================================================

Patch marker: AIR_DETERMINISTIC_CONTRACT_MACHINE_REPRESENTATION_V1
Floor invariant: AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION

Core principle:
Deterministic control truth must be executable data, not natural-language inference. A prose sentence may document a deterministic requirement but cannot itself be an operative predicate or duplicate a canonical literal when a canonical path reference exists.

Rules:
1. The Default Starter validation_contract.deterministic_contract_registry is the operative typed registry for five-file Foundation cross-file/load compatibility predicates in this candidate.
2. Every registry entry has a unique check_id, a declared operator, typed operands, deterministic failure behavior, and execution state.
3. Registry coverage is closed-world: declared deterministic checks = implemented checks = executed checks. Any unknown operator, unresolved canonical path, unexecuted check, duplicate check_id, or coverage-count mismatch fails closed.
4. Canonical values must be referenced by canonical file/path or Core header key when they already exist. A copied version/designation/schema literal is not an independent authority.
5. Natural-language validation expectations and replay definitions are NON_OPERATIVE_DESCRIPTION. They may guide review or behavioral replay but cannot create a boot or release compatibility value.
6. A deterministic registry executor must reject free-form string predicates in the operative registry. It must not semantically infer what a sentence means.
7. Release validation must execute the complete registry and mutation-test every declared deterministic check specification.
8. Runtime/model boot consumes the typed registry according to the same non-inference rule: do not invent missing operands or consequences.

Claim boundary:
This is prompt-layer and repository validation discipline. It does not make LLM behavior universally deterministic or claim backend enforcement.

