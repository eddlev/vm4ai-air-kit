# AIR 2.5.0 Object Responsibility Audit

Target: `eddlev/vm4ai-air-kit` / `air250-preview-stage-t12d`

Decision: **BLOCK PRE-MAIN — object contract hardening required**

## Audit rule

Each formal AIR object must own only the data required by its semantic responsibility. Cross-object state is permitted only as:

- an explicit reference,
- a clearly non-authoritative derived projection,
- a comparison datum required by a receipt or decision,
- or transfer-only serialization inside `AIR_HANDOFF_CARD`.

Common self-describing provenance fields (`object_version`, `record_class`, `runtime_origin`, claim-boundary fields, and `evaluation_basis` when required) are not improper redundancy.

## Cross-cutting defects

1. Most formal objects use **minimum-field contracts**, not closed allowed-field schemas. Nothing generally forbids unrelated extra fields.
2. `record_class` is described as object identity even though both project brief and execution map use `PROJECT_STATE_RECORD`.
3. Formal-label reservation sets are stale/incomplete. Core omits `AIR_ACTIVE_CONTRACT`, `AIR_GATE`, `AIR_REQUIRED_INPUT_REQUEST`; Control omits more. `AIR_PRIMED_ONBOARDING` is reserved but is not a canonical formal object.
4. Starter's AIR_ARTIFACT field registry is not synchronized with Core. Core requires `artifact_lease` and `action_governance_state` on every bound artifact, while Starter does not list them as unconditional artifact fields.
5. Starter deliberately fans the same test-evidence fields across Brief, Map, Artifact, and Validation Report; prior-effect state is similarly fanned across Session, Artifact, Prior Effect Record, and Handoff.
6. Recent emitted AIR alignment/validation objects in this project did not meet the current Core minimum schemas, which is field evidence that the current contracts are not constraining shape strongly enough.

## Per-object result

| Object | Result | Primary responsibility issue |
|---|---|---|
| `AIR_RUNTIME_BRIDGE` | HARDEN | Transition record contains full downstream state carriers rather than transition facts + refs. |
| `AIR_SESSION` | HARDEN | Session-level object carries task-level semantic/epistemic/prior-effect state without a strict aggregate/ref boundary. |
| `AIR_PROJECT_INITIALIZATION_BRIEF` | REDESIGN | No exact field schema; duplicates Execution Map heavily. |
| `AIR_PROJECT_EXECUTION_MAP` | HARDEN | Roadmap duplicates active-artifact blockers/readiness/evidence without marking them derived. |
| `AIR_ARTIFACT` | PASS WITH SCHEMA REPAIR | Correct broad owner for task execution, but Starter registry is stale and conditional extras leak in. |
| `AIR_ACTIVE_CONTRACT` | REDESIGN | Alias mismatch with `execution_contract`; misleading `binding_state`; current receiver state leaks into contract terms. |
| `AIR_GATE` | REDESIGN | Repeats Artifact/Contract policy state instead of referencing it and owning only checks/decision. |
| `AIR_VALIDATION_REPORT` | HARDEN | Core is clean, but Control/Starter add fields not consistently defined; patch planning leaks into validation results. |
| `AIR_ALIGNMENT_CHECK` | PASS WITH CLOSED SCHEMA | Responsibility is clean; needs unknown-field rejection. |
| `AIR_ERROR` | PASS WITH CLOSED SCHEMA | Responsibility is clean; needs unknown-field rejection. |
| `AIR_ACTION_AUTHORIZATION` | REDESIGN | No exact Core schema and partly duplicates Gate; should be a compact single-use ticket. |
| `AIR_ACTION_RECEIPT` | PASS WITH EXACT SCHEMA | Concept is clean; exact schema missing. |
| `AIR_PRIOR_EFFECT_RECORD` | REDESIGN | Canonical object has no exact schema; recovery state is also duplicated elsewhere. |
| `AIR_REQUIRED_INPUT_REQUEST` | HARDEN | Mostly clean, but responsive-binding conditional fields are not formally defined in its Core schema. |
| `AIR_HANDOFF_CARD` | NORMALIZE | Transfer duplication is necessary, but several data points have multiple independent carriers/owners. |

## Recommended patch sequence

1. Add a Core closed-world object ownership/schema law and one canonical object registry.
2. Normalize `AIR_ACTIVE_CONTRACT` -> `AIR_ARTIFACT.execution_contract` names and ownership.
3. Split Initialization Brief and Execution Map responsibilities.
4. Slim Gate and Action Authorization to refs plus their own decision/ticket data.
5. Define exact Authorization, Receipt, and Prior Effect schemas.
6. Repair Starter typed registries and multi-plane conditional duplication.
7. Normalize Handoff duplicate carriers and canonical precedence.
8. Synchronize formal-label reservations and remove/define `AIR_PRIMED_ONBOARDING`.
9. Add static schema ownership tests and emitted-object fixtures.
10. Rerun static/Specialist/executable validation plus targeted object-emission smoke.
