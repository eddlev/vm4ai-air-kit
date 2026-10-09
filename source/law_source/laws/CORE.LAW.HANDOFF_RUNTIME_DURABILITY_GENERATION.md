==================================================
HANDOFF RUNTIME DURABILITY AND GENERATION CONTRACT
==================================================

Patch marker: AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1
Floor invariants reinforced: AIR-FLOOR-007, AIR-FLOOR-013, AIR-FLOOR-014, AIR-FLOOR-017, AIR-FLOOR-018, AIR-FLOOR-021, AIR-FLOOR-025, AIR-FLOOR-026

Purpose:
Make Handoff durability discovery, strict eligibility, generation evaluation, portable-state validation, and file-delivery receipt semantics typed and deterministic from live Session state through file creation and restoration.

Canonical live-session owner:
- AIR_SESSION.handoff_durability_state is the sole canonical live-session owner of Handoff durability state.
- AIR_HANDOFF_CARD.handoff_mode_state and surfaced_object_ledger_state.provenance_capture are serialized transfer projections only. They never become the target session's live durability owner on restore.
- On fresh activation and HANDOFF_RESTORE, the target runtime must negotiate its own provider state and write the result into the current AIR_SESSION.handoff_durability_state before any provenance-dependent canonical formal-object emission.

Typed provider adapter state:
DURABLE_PROVENANCE_PROVIDER_ADAPTER_STATE is Core-owned typed non-formal runtime state. It is persistence capability state, not an AIR formal object and not execution authority.
Required fields:
- adapter_contract = AIR_DURABLE_PROVENANCE_PROVIDER_ADAPTER_V1
- discovery_state = NOT_EVALUATED | PROVIDER_ABSENT | PROVIDER_PRESENT_UNVERIFIED | PROVIDER_VERIFIED | PROVIDER_FAILED_INTEGRITY
- provider_identity
- provider_class
- provider_generation
- exact_write_capability = PASS | FAIL | NOT_AVAILABLE | NOT_EVALUATED
- exact_readback_capability = PASS | FAIL | NOT_AVAILABLE | NOT_EVALUATED
- stable_identity_retrieval_capability = PASS | FAIL | NOT_AVAILABLE | NOT_EVALUATED
- coverage_state = COMPLETE_TO_CURRENT_COMMITTED_LEDGER | INCOMPLETE | NOT_APPLICABLE_NO_PROVIDER | FAILED_INTEGRITY | NOT_EVALUATED
- probe_evidence_refs
- last_verified_state_epoch
- positive_execution_authority = NONE

Discovery/adapter procedure:
1. Probe the configured runtime persistence surface; do not infer provider availability from onboarding answers, model memory, transcript visibility, summaries, or prompt context.
2. When no qualifying persistence provider exists, set discovery_state = PROVIDER_ABSENT.
3. When a provider exists, verify exact write, exact readback, and later stable-identity retrieval independently of the model context window.
4. Any readback/hash/identity contradiction or provider claim contradicted by observed bytes sets discovery_state = PROVIDER_FAILED_INTEGRITY.
5. Re-evaluate after provider/storage identity changes. Provider-generation changes invalidate prior capability probes until reverified.

Deterministic durability and strict-eligibility transition table:
- PROVIDER_ABSENT -> strict_handoff_durability_state = UNAVAILABLE -> strict_handoff_eligibility = INELIGIBLE_UNAVAILABLE.
- PROVIDER_PRESENT_UNVERIFIED, or qualifying provider with incomplete committed-history coverage -> DEGRADED_INCOMPLETE -> INELIGIBLE_INCOMPLETE.
- PROVIDER_VERIFIED + exact write PASS + exact readback PASS + stable identity retrieval PASS + COMPLETE_TO_CURRENT_COMMITTED_LEDGER coverage -> AVAILABLE_VERIFIED -> ELIGIBLE.
- PROVIDER_FAILED_INTEGRITY, any canonical snapshot hash mismatch, stable-identity mismatch, contradictory provider identity, or impossible coverage claim -> FAILED_INTEGRITY -> BLOCKED_FAILED_INTEGRITY.
- A provider that becomes available after provenance-dependent canonical emissions were committed without qualifying durable capture cannot retroactively create native strict history. The current session remains DEGRADED_INCOMPLETE / INELIGIBLE_INCOMPLETE for that uncaptured history unless an explicit supported legacy boundary already exists; AIR never synthesizes the missing snapshots.

AIR_SESSION.handoff_durability_state minimum fields:
- contract = AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1
- provider_adapter_contract = AIR_DURABLE_PROVENANCE_PROVIDER_ADAPTER_V1
- provider_identity
- provider_class
- provider_generation
- discovery_state
- strict_handoff_durability_state
- strict_handoff_eligibility
- coverage_state
- last_verified_state_epoch
- probe_evidence_refs
- positive_execution_authority = NONE

Typed dependency producers and predicates:
- DEP.HANDOFF_GENERATION_EVALUATION producer = current RT.HANDOFF_CREATE alignment/evaluation transaction. SATISFIED only when AIR_HANDOFF_CARD.evaluation_basis is populated from the current HANDOFF_CREATE evaluation with evaluation_id, evaluation_profile = HANDOFF_CREATE, current state_epoch, alignment_check_ref, validation_report_ref, and dependency_state = SATISFIED. Stale, prior-session, template, missing, or non-HANDOFF_CREATE evaluation basis fails closed.
- DEP.HANDOFF_MODE_RESOLVED producer = deterministic AIR_HANDOFF_MODE_SELECTION_V1 using request mode plus AIR_SESSION.handoff_durability_state.strict_handoff_eligibility. No onboarding answer or serialized source-session durability projection may substitute for the live Session owner.
- DEP.DURABLE_SURFACED_PROVENANCE_COMPLETE predicate = selected mode is STRICT_PROVENANCE AND live strict_handoff_durability_state = AVAILABLE_VERIFIED AND strict_handoff_eligibility = ELIGIBLE AND durable canonical-snapshot coverage is complete through the frozen pre-file ledger cutoff with exact readback/hash/identity correspondence.
- DEP.PORTABLE_HANDOFF_STATE_VALID predicate = selected mode is PORTABLE_STATE AND live durability state is not FAILED_INTEGRITY AND current state/schema integrity is valid AND surfaced_object_ledger_state.entries is empty AND surfaced_object_ledger_state.completeness_state = NOT_CLAIMED_PORTABLE_STATE AND failure_mode_state.records is empty AND failure_mode_state.history_completeness_state = NOT_CLAIMED_PORTABLE_STATE AND no historical Gate/Authorization/Receipt/approval/binding/effect authority was reconstructed AND handoff_mode_state.positive_execution_authority = NONE AND current handoff generation evaluation is satisfied.

Serialized generation-evaluation carrier:
- AIR_HANDOFF_CARD.evaluation_basis is the sole root serialized carrier for the current Handoff generation evaluation.
- A separate root handoff_generation_evaluation field is prohibited in current generated cards. The dependency name DEP.HANDOFF_GENERATION_EVALUATION names the producer/predicate, not an additional serialized root field.
- Serialized evaluation_basis is transfer provenance only. It never becomes current execution authority after HANDOFF_RESTORE.

Restore rule:
- HANDOFF_RESTORE validates the source card's serialized durability and mode projections as transfer evidence only.
- The target session independently executes provider discovery/adapter negotiation and writes a fresh AIR_SESSION.handoff_durability_state before strict eligibility can be used.
- Source-session AVAILABLE_VERIFIED does not imply target-session AVAILABLE_VERIFIED; target-session absence, incompleteness, or integrity failure is surfaced according to this contract.

