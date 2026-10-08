==================================================
HANDOFF MODE SELECTION LAW
==================================================

Patch marker: AIR_HANDOFF_MODE_SELECTION_V1
Floor invariants reinforced: AIR-FLOOR-007, AIR-FLOOR-013, AIR-FLOOR-018, AIR-FLOOR-021, AIR-FLOOR-025, AIR-FLOOR-026

Purpose:
Handoff creation has two explicit assurance modes. STRICT_PROVENANCE preserves the rev19 durable-snapshot guarantee. PORTABLE_STATE provides a non-authorizing continuation file when qualifying durable provenance is unavailable or incomplete, without fabricating historical surfaced-object provenance or execution authority.

Request modes:
- GENERIC
- STRICT_PROVENANCE
- PORTABLE_STATE

Selected modes:
- STRICT_PROVENANCE
- PORTABLE_STATE
- BLOCKED

Mode-resolution dependencies:
- Common creation dependencies are DEP.CURRENT_STATE_RECONCILED, DEP.HANDOFF_SCHEMA_VALID, DEP.HANDOFF_GENERATION_EVALUATION, and DEP.HANDOFF_MODE_RESOLVED.
- STRICT_PROVENANCE additionally requires DEP.DURABLE_SURFACED_PROVENANCE_COMPLETE.
- PORTABLE_STATE additionally requires DEP.PORTABLE_HANDOFF_STATE_VALID.

Deterministic selection:
1. GENERIC + strict_handoff_eligibility = ELIGIBLE -> STRICT_PROVENANCE.
2. GENERIC + strict_handoff_eligibility = INELIGIBLE_UNAVAILABLE or INELIGIBLE_INCOMPLETE -> PORTABLE_STATE.
3. GENERIC + strict_handoff_eligibility = BLOCKED_FAILED_INTEGRITY -> BLOCKED and route to REVIEW/RECOVERY.
4. Explicit STRICT_PROVENANCE + ELIGIBLE -> STRICT_PROVENANCE; explicit strict never silently downgrades. Unavailable/incomplete strict state fails closed; FAILED_INTEGRITY blocks.
5. Explicit PORTABLE_STATE -> PORTABLE_STATE when current state is otherwise valid, except FAILED_INTEGRITY or independent state/schema/integrity failure blocks.

STRICT_PROVENANCE contract:
- preserve the complete committed pre-file surfaced-object history through the frozen cutoff
- every carried canonical snapshot must come from the verified durable provenance provider and re-hash to the committed ledger entry
- failure-mode history remains ledger-backed exact provenance
- no transcript, summary, memory, or semantic reconstruction substitutes for missing history

PORTABLE_STATE contract:
- produce the same downloadable AIR_HANDOFF_CARD.json file class and schema family, with handoff_mode_state.selected_mode = PORTABLE_STATE
- make no claim of complete historical surfaced-object provenance
- serialize surfaced_object_ledger_state.entries as empty and completeness_state = NOT_CLAIMED_PORTABLE_STATE; do not reconstruct missing snapshots
- serialize failure_mode_state.records as empty with history_completeness_state = NOT_CLAIMED_PORTABLE_STATE; current blockers, task/artifact state, sources, and continuation requirements remain explicit in their normal non-authorizing carriers
- do not synthesize historical AIR_GATE, AIR_ACTION_AUTHORIZATION, AIR_ACTION_RECEIPT, approval, binding, or effect authority
- all restored state remains UNVALIDATED_BOOTSTRAP_INPUT/non-authorizing until current HANDOFF_RESTORE alignment, validation, Artifact precheck, and rebinding complete
- file-only delivery, strict JSON parsing, duplicate-key rejection, exact post-write reopen validation, and delivery receipt requirements remain unchanged

FAILED_INTEGRITY is not equivalent to missing infrastructure. It blocks automatic portable downgrade because the observed provenance/integrity surface is contradictory or corrupt.

