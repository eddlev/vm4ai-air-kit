==================================================
HANDOFF CONTINUATION FLOW
==================================================
Patch marker: AIR_HANDOFF_CONTINUATION_BOOTSTRAP_V2

A valid AIR_HANDOFF_CARD is a first-class continuation-bootstrap input for a new session or platform.
It is a serialized transfer record, not an execution authority.

When a handoff card is attached or explicitly supplied:
1. enter BOOTSTRAP_NO_ARTIFACT with bootstrap_route = HANDOFF_CONTINUATION
2. validate strict JSON shape, template designation, schema version, source identity, and declared integrity state
3. restore only explicitly represented project, onboarding, working-agreement, governance, source, artifact, and orbit state
4. canonically emit a current-session AIR_SESSION restoration object using the exact Core-owned object schema; a key/value summary or prior-session object does not satisfy this step
5. restore candidate artifacts and Orbit 1 or Orbit 2 queue entries when their identity and serialized state are sufficient
6. identify the artifact nominated for Orbit 0, if the card declares one
7. validate or reconstruct that artifact as an UNBOUND_DRAFT candidate
8. run artifact precheck and ARTIFACT_BINDING_TRANSACTION
9. atomically bind exactly one artifact into Orbit 0
10. canonically emit the newly bound AIR_ARTIFACT using the exact Core-owned object schema and record_class before ordinary governed continuation
11. keep all other valid task artifacts non-executing in Orbit 1 or Orbit 2
12. continue material execution only after binding succeeds and required current-session formal objects have been canonically emitted

The handoff card may restore:
- project and platform identity
- prompt, schema, and package versions
- task keys and task centers
- artifact IDs, revisions, binding history, and queue state
- Orbit 0 nomination and Orbit 1 or Orbit 2 entries
- dependency edges, return targets, and resume conditions
- onboarding, Q4, Q4D, Q6, and Q6D state
- selected and bound specialists or methods as declared inputs
- sources, source rights, and evidence state
- blockers, uncertainty, approval scope, and receiver-delivery state

The handoff card must not:
- execute the project task
- directly grant ACTIVE_EXECUTION_BINDING
- turn a stale, rejected, superseded, or incomplete artifact into an active artifact
- silently resolve conflicting Orbit 0 claims
- fabricate absent queued tasks, sources, approvals, or evidence

If the card declares no usable Orbit 0 candidate:
- preserve valid Orbit 1 and Orbit 2 state
- compile a new Orbit 0 candidate from the restored project state and current user direction
- require normal precheck and binding

If the card declares more than one Orbit 0 or active-binding candidate:
- enter ARTIFACT_BINDING_RECOVERY
- suspend material task execution
- preserve governance, validation, comparison, user-selection, and rebinding operations
- resolve to exactly one valid Orbit 0 artifact before continuation

If the user changes the intended active task during continuation bootstrap:
- treat the user selection as bootstrap input
- promote or compile the selected task candidate through ARTIFACT_BINDING_TRANSACTION
- place the previously nominated task in Orbit 1 or Orbit 2 when it remains valid

Do not re-run onboarding fields that the valid handoff restores completely.
Ask only for missing or conflicting continuation state that materially affects binding.
Do not reinterpret the handoff narratively.

