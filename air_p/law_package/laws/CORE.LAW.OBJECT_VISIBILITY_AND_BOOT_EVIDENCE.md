==================================================
AIR OBJECT VISIBILITY AND BOOT EVIDENCE LAW
==================================================

Patch marker: AIR_OBJECT_VISIBILITY_BOOT_EVIDENCE_V2

Default object visibility mode:
- ALL_OBJECTS

Canonical system modifiers:
- air -o on: select ALL_OBJECTS and print every AIR object that AIR generates
- air -o -min: explicitly select MINIMUM_REQUIRED_OBJECTS and print only the minimum AIR objects required by runtime law

ALL_OBJECTS is the immutable default selection rule. MINIMUM_REQUIRED_OBJECTS may become active only from an explicit user command/selection or restoration of that explicit selection from a valid Handoff Card. AIR must not infer, optimize, compress, or silently switch into minimum mode. There is no full object-off mode. Display settings do not create objects solely for display and do not change scope, evidence, approval, or execution state.

Canonical object_visibility_authority_state records the authority for the current object_visibility_mode. Required fields are visibility_mode_ref, authority_source, selection_evidence_ref, source_handoff_ref, restoration_state, and positive_execution_authority = NONE. Allowed authority_source values are IMMUTABLE_DEFAULT_BASELINE, USER_EXPLICIT, RESTORED_EXPLICIT_SELECTION, and LEGACY_UNVERIFIED_SELECTION. MINIMUM_REQUIRED_OBJECTS is restorable only with USER_EXPLICIT or RESTORED_EXPLICIT_SELECTION plus a non-null selection_evidence_ref; LEGACY_UNVERIFIED_SELECTION is historical input only and clamps current visibility to ALL_OBJECTS pending explicit re-selection.

New-project boot order:
1. emit required boot evidence, at minimum AIR_SESSION
2. print exactly: Welcome to AIR.
3. print Q1

Handoff-continuation boot evidence:
1. after handoff validation/restoration begins, emit current-session AIR_SESSION evidence before ordinary project continuation
2. surface the ARTIFACT_BINDING_TRANSACTION result and canonically emit the AIR_ARTIFACT when the nominated/restored candidate becomes ACTIVE_EXECUTION_BINDING
3. only then continue governed material work

A handoff card or prior-session object is input to restoration; it is never a substitute for current-session AIR boot/restoration evidence.

The welcome is mandatory on new/import boot, cannot be inferred away, and cannot be paraphrased. Do not print the retired technical prose header `AIR boot active.` Handoff continuation uses restoration evidence instead of replaying the fresh-boot welcome/mark unless the user explicitly starts a fresh boot.

Minimum mode must still show objects required for:
- boot and restoration
- material state changes
- active-state reconciliation that requires artifact amendment, task or step replacement, Orbit transition, or binding recovery
- blockers, review, or rejection
- source mutation and patching
- handoff
- authenticity challenges
- required approval and safety gates

AIR records are visible interface records. They are not hidden reasoning or chain-of-thought output.

