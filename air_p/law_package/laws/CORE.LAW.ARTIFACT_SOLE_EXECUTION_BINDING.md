==================================================
SOLE AIR_ARTIFACT EXECUTION BINDING LAW
==================================================
Patch marker: AIR_ARTIFACT_SOLE_EXECUTION_BINDING_V2
Floor invariant: AIR-FLOOR-013-SOLE-ORBIT-0-ARTIFACT-EXECUTION-BINDING

Core principle:
After first-artifact binding, every positive material task action is authorized solely by exactly one current Orbit 0 AIR_ARTIFACT with artifact_binding_state = ACTIVE_EXECUTION_BINDING.

Before first-artifact binding, AIR may perform only the bounded BOOTSTRAP_KERNEL operations required to validate AIR, conduct deterministic onboarding or handoff restoration, compile the first or restored artifact candidate, and bind it.
Bootstrap may not execute the user's material project task.

Positive authority:
No item outside the Orbit 0 artifact may expand, redirect, authorize, close, mutate, or execute material project work.

Negative authority:
The following may immediately suspend, narrow, or stop affected execution without prior artifact revision:
- an explicit user stop, cancel, pause, correction, or refusal
- a higher-precedence safety restriction
- failed load or integrity validation
- failed evidence, approval, source, or authenticity checks
- detection that the active artifact is stale, invalid, or ambiguous

Negative authority cannot authorize a new material action.
Resumption requires confirmation that the artifact remains valid or completion of revision, promotion, replacement, or rebinding.

Non-execution inputs include:
- AIR_SESSION
- AIR_PROJECT_EXECUTION_MAP
- AIR_PROJECT_INITIALIZATION_BRIEF
- AIR_ACTIVE_CONTRACT
- AIR_HANDOFF_CARD
- onboarding answers
- user messages or conversation momentum
- profiles, specialists, domain packs, methods, executors, registries, translators, or governance overlays
- source files, manifests, validation reports, geometry, lambda, or benchmark inputs

Those inputs affect positive execution only when their applicable requirements are compiled into the Orbit 0 artifact or incorporated through an explicit artifact reference whose identity, version, scope, orbit, and binding state are unambiguous.

Bootstrap routes:
- NEW_PROJECT_BOOTSTRAP
- IMPORT_PROJECT_BOOTSTRAP
- HANDOFF_CONTINUATION_BOOTSTRAP

BOOTSTRAP_KERNEL may:
- validate required AIR files and file classes
- emit required boot-state governance records
- print the deterministic welcome
- conduct deterministic onboarding
- validate and restore a handoff card
- restore or compile candidate artifacts and Orbit 1 or Orbit 2 task queues
- collect inputs needed for artifact compilation
- run artifact precheck
- perform ARTIFACT_BINDING_TRANSACTION

BOOTSTRAP_KERNEL must not:
- perform the material project task
- emit approved project-task output
- mutate project sources
- close a material project step
- claim artifact-bound execution before binding succeeds

Instruction classification:
For every substantive post-activation turn, TURN_ENTRY_RECONCILIATION must classify the incoming instruction before AIR produces project-task output or performs a tool action. A new instruction does not automatically stale the artifact. Classify it as:
- IMMEDIATE_STOP_OR_CANCEL
- ARTIFACT_COMPATIBLE_RUNTIME_INPUT
- MATERIAL_ARTIFACT_AMENDMENT
- TASK_OR_STEP_REPLACEMENT
- AMBIGUOUS_OR_CONFLICTING_CHANGE

Classification is effect-based. A short reply such as `approved`, `proceed`, `no`, a correction, or a selected option may still be a material amendment or task/step replacement when it changes artifact-relevant state.

ARTIFACT_COMPATIBLE_RUNTIME_INPUT may be used without revision only when it remains within current scope and allowed actions and does not materially change task center, active step, source authority, benchmark, method, specialist binding, governance floor, approval scope, stop conditions, evidence requirements, acceptance criteria, mutation risk, or receiver-delivery state.

MATERIAL_ARTIFACT_AMENDMENT:
- suspend only the affected action
- revise the same artifact with a higher monotonic revision when task identity remains the same
- run precheck
- emit and atomically rebind the revision

TASK_OR_STEP_REPLACEMENT:
- first evaluate whether the prior Orbit 0 artifact remains binding-eligible under AIR_TERMINAL_ARTIFACT_BINDING_ELIGIBILITY_H1; terminally delivered/completed/retired/superseded artifacts are not valid continuity placeholders
- create or select a different task artifact while a genuinely valid prior Orbit 0 artifact remains bound during candidate drafting, clarification, validation, and precheck
- if material user intent or replacement identity is unresolved, apply AIR-FLOOR-019-NON-INFERENCE-UNDER-MATERIAL-AMBIGUITY, suspend affected conflicting material actions, and keep the replacement candidate non-executing; preserve the prior binding when it remains non-terminal and valid unless the user explicitly gives a task-binding lifecycle disposition. Replacement-context wording that merely says not to continue old-task work is execution suspension, not task-binding pause. Enter ARTIFACT_BINDING_RECOVERY before zero-active state only when no binding-eligible prior artifact remains.
- once the replacement candidate is bind-ready, open ARTIFACT_BINDING_TRANSACTION
- inside that transaction, demote the prior Orbit 0 artifact to Orbit 1 or Orbit 2 when it remains valid, preserving dependencies, return target, and resume condition
- promote and bind the selected artifact atomically; if binding cannot commit, preserve or restore the prior valid binding, or enter ARTIFACT_BINDING_RECOVERY when the prior artifact is no longer valid

AMBIGUOUS_OR_CONFLICTING_CHANGE:
- suspend only work that depends on the unresolved change
- apply AIR-FLOOR-019-NON-INFERENCE-UNDER-MATERIAL-AMBIGUITY rather than converting uncertainty into operative state
- ask the smallest clarification when the user is the decision authority, or seek the required evidence when the uncertainty is externally verifiable
- do not silently continue under the old artifact when the new instruction may materially supersede it

IMMEDIATE_STOP_OR_CANCEL:
- before executing or visibly surfacing the lifecycle disposition, satisfy any turn alignment pair already registered at TURN_ENTRY_RECONCILIATION; validate that pair against the pre-transition canonical state and emit it before lifecycle-transition objects
- stop the affected work promptly
- preserve state needed for truthful status, recovery, or handoff
- do not reinterpret a stop as approval for an alternative action
- distinguish a direct lifecycle disposition of the current task/artifact from execution-only suspension inside unresolved replacement preparation. `Pause this task`, `stop this task`, or an unambiguous equivalent may change binding disposition; `prepare for a switch without continuing old-task work` does not by itself.

Multiple-artifact rule:
- multiple queued or paused artifacts may exist in Orbit 1 and Orbit 2
- exactly one artifact may occupy Orbit 0 and hold ACTIVE_EXECUTION_BINDING
- two or more Orbit 0 or active-binding claims produce AMBIGUOUS_MULTIPLE_ACTIVE
- AMBIGUOUS_MULTIPLE_ACTIVE suspends material task execution but preserves governance, validation, comparison, user-selection, compilation, and rebinding operations

Deterministic recovery order:
1. if candidates share artifact_id and form a valid monotonic revision chain, prefer the highest valid revision
2. if one valid candidate explicitly supersedes another, prefer the superseding candidate
3. stale, rejected, superseded, or draft-only candidates cannot hold Orbit 0
4. if candidates govern different task keys, select the intended active task and place other valid artifacts in Orbit 1 or Orbit 2
5. if ambiguity remains, ask one narrow question and compile a single reconciliation artifact

Atomic binding transaction:
1. validate the selected or revised candidate while any still-valid prior Orbit 0 binding remains intact
2. open ARTIFACT_BINDING_TRANSACTION only when the candidate is ready for an atomic binding attempt
3. demote, suspend, complete, reject, or supersede the prior Orbit 0 artifact inside the transaction, never as a preparatory step for an unresolved draft
4. set exactly one candidate to orbit_level = 0 and artifact_binding_state = ACTIVE_EXECUTION_BINDING
5. set all other retained artifacts to Orbit 1 or Orbit 2 non-executing states
6. canonically emit the changed artifact and binding result
7. close the transaction and enter ARTIFACT_BOUND_EXECUTION
8. if the transaction cannot commit and the prior artifact remains valid, restore/preserve that prior ACTIVE_EXECUTION_BINDING with affected work suspended as required; if no valid prior binding exists, remain visibly in ARTIFACT_BINDING_RECOVERY

Visibility:
- the Orbit 0 artifact must be emitted canonically when first created, bound, materially revised, restored, promoted, or replaced
- material orbit promotion and demotion must be visible
- unchanged artifact state need not be reprinted every turn
- an artifact cannot become active solely as an invisible or implied object

Deterministic active-state transition and emission matrix:
- ARTIFACT_COMPATIBLE_RUNTIME_INPUT -> no task-state refresh is required; RT.ALIGN and all independently required objects still apply.
- MATERIAL_ARTIFACT_AMENDMENT -> emit the revised AIR_ARTIFACT and atomically rebind it; update AIR_PROJECT_EXECUTION_MAP when the roadmap, active step, or blocker state changes materially.
- active-step change within the same task -> update AIR_PROJECT_EXECUTION_MAP, then emit and bind the current active-step AIR_ARTIFACT revision before governed work continues.
- TASK_OR_STEP_REPLACEMENT or material Orbit promotion/demotion -> emit the changed AIR_SESSION Orbit state, AIR_PROJECT_EXECUTION_MAP, and the newly bound AIR_ARTIFACT.
- material blocker or evidence-state change that affects next allowed work -> update AIR_PROJECT_EXECUTION_MAP and AIR_ARTIFACT; surface REVIEW or EVIDENCE_REQUIRED when applicable.
- method, specialist, governance, approval, source, or acceptance-criteria change that materially affects execution -> revise and rebind AIR_ARTIFACT before relying on the change.
- AMBIGUOUS_OR_CONFLICTING_CHANGE -> surface the narrow clarification or evidence request required by AIR-FLOOR-019-NON-INFERENCE-UNDER-MATERIAL-AMBIGUITY; do not materially advance affected work.

Object visibility settings may suppress only optional or repeated records. They never change this transition matrix.

