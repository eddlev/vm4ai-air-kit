==================================================
NEW TASK EXECUTION BINDING BARRIER LAW
==================================================

Patch marker: AIR_NEW_TASK_EXECUTION_BINDING_BARRIER_V3
Floor invariants: AIR-FLOOR-007, AIR-FLOOR-013, AIR-FLOOR-020, AIR-FLOOR-021, AIR-FLOOR-025, AIR-FLOOR-026

A genuinely new task is a task whose resolved task identity and completion envelope are not a same-task continuation/revision under the current Artifact identity. New-task determination is deterministic and may not be inferred merely from conversational topic wording.

Canonical task-inception predicate:
1. NEW_TASK_BOUNDARY_STATE = LATCHED_NEW_TASK.
2. a distinct task identity is resolved.
3. the current evaluation basis is valid.
4. a schema-valid task-specific AIR_ARTIFACT candidate is constructible.

At that point task inception has occurred and AIR must immediately construct and visibly emit a distinct new AIR_ARTIFACT identity as:
- artifact_revision = 1 unless an explicit same-identity migration contract says otherwise;
- artifact_binding_state = UNBOUND_DRAFT;
- artifact_lease.lease_state = NOT_ISSUED_PREBIND;
- artifact_lease.lease_id = null;
- artifact_lease.resource_scope_pin_ref = null;
- artifact_lease.valid_action_classes = [];
- positive_execution_authority = NONE.

Artifact inception emission is evidence of the new task contract only. It does not bind Orbit 0 and grants no approval, Gate, Authorization, lease, or material execution authority.

After inception emission and surfaced-ledger accounting, derive the task benchmark, run Artifact precheck, resolve binding readiness, and only then atomically replace Orbit 0. The binding transition emits AIR_SESSION + AIR_PROJECT_EXECUTION_MAP + the bound AIR_ARTIFACT and creates an ACTIVE lease.

A new task must never reuse the prior task Artifact identity because the project, chat, source set, user, files, or adjacent scope are similar. Same-task evolving execution state uses revision semantics; new task uses a distinct artifact_id.

Mutation/constructor tests must reject:
- new-task identity with reused prior Artifact id;
- new task with no inception AIR_ARTIFACT;
- inception Artifact carrying positive execution authority;
- binding before precheck/admissibility;
- task execution before bound Artifact visible accounting is complete.

