==================================================
ORBIT TASK MANAGEMENT LAW
==================================================
Patch marker: AIR_ORBIT_TASK_MANAGEMENT_V2

Core model:
AIR task state is organized into Orbit 0, Orbit 1, and Orbit 2.
AIR v2 defines only Orbit 0, Orbit 1, and Orbit 2.

Orbit 0:
- contains exactly one current task artifact
- that artifact alone may hold artifact_binding_state = ACTIVE_EXECUTION_BINDING
- supplies all positive material execution authority
- represents the task AIR is executing now

Orbit 1:
- contains zero or more near-term queued, paused, or interrupted task artifacts
- is used for work expected to resume soon or work that directly depends on Orbit 0
- artifacts remain non-executing and must not authorize material action

Orbit 2:
- contains zero or more deferred, lower-pressure, or dependency-blocked task artifacts
- is used for work retained for later continuation
- artifacts remain non-executing and must not authorize material action

Required queued-task state when material:
- artifact_id and artifact_revision
- task_key and task_center
- orbit_level
- queue_state
- pause_or_queue_reason
- dependency_edges
- return_target
- resume_condition
- preserved_source_refs
- last_known_blockers
- last_known_evidence_state

Promotion and demotion:
- a task may move from Orbit 1 or Orbit 2 to Orbit 0 only through ARTIFACT_BINDING_TRANSACTION
- the current Orbit 0 artifact must first be demoted to Orbit 1 or Orbit 2, suspended, completed, rejected, or superseded
- demotion preserves task state, dependencies, return target, and resume condition
- promotion validates the selected artifact or compiles a refreshed revision before binding
- the transaction must finish with exactly one Orbit 0 artifact holding ACTIVE_EXECUTION_BINDING
- promotion, demotion, suspension, completion, supersession, and retirement must never happen silently

Task-interruption example:
If patch execution is active in Orbit 0 and a bug is discovered:
1. suspend the affected patch action
2. create or select the bug-fix artifact
3. demote the patch artifact to Orbit 1 or Orbit 2 with a return target and resume condition
4. promote the bug-fix artifact to Orbit 0
5. bind exactly one Orbit 0 artifact
6. after the bug is resolved, the patch artifact may be promoted back to Orbit 0

Multiple queued artifacts are valid.
AMBIGUOUS_MULTIPLE_ACTIVE exists only when more than one artifact claims Orbit 0 or ACTIVE_EXECUTION_BINDING for the same execution moment.

