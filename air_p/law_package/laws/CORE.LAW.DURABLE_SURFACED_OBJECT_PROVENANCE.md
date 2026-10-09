==================================================
DURABLE SURFACED-OBJECT PROVENANCE LAW
==================================================

Patch marker: AIR_DURABLE_SURFACED_OBJECT_PROVENANCE_V1
Floor invariants tightened: AIR-FLOOR-007, AIR-FLOOR-010, AIR-FLOOR-017, AIR-FLOOR-018, AIR-FLOOR-021, AIR-FLOOR-026

Purpose:
Strict Handoff provenance must not depend on future random-access retrieval of verbatim prior chat turns. Exact canonical snapshots required by RT.HANDOFF_CREATE are therefore captured at or near first emission onto a durable retrieval surface whose bytes remain retrievable independently of model-context truncation.

Durability capability negotiation:
- Resolve AIR_SESSION.handoff_durability_state through AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1 no later than the first post-activation canonical formal-object emission and again after any provider/storage change. strict_handoff_durability_state is the normalized state inside that live Session carrier.
- Allowed states are AVAILABLE_VERIFIED, UNAVAILABLE, DEGRADED_INCOMPLETE, and FAILED_INTEGRITY.
- AVAILABLE_VERIFIED requires a runtime-controlled persistence provider that can write the exact canonical snapshot, read back the exact bytes/object, and retrieve it later by stable provenance identity without relying on conversation-window recall.
- The current prompt/context window, conversation summary, model memory, later ledgers, semantic state, and user-visible old-turn availability are not durable provenance providers.
- If no qualifying provider exists, AIR may continue otherwise-valid project work, but it must surface strict-Handoff durability as unavailable before provenance-dependent history accumulates. STRICT_PROVENANCE completion remains ineligible from that point; a generic or explicit portable Handoff may proceed only through AIR_HANDOFF_MODE_SELECTION_V1 when PORTABLE_STATE is otherwise valid. AIR must not defer discovery until Handoff creation and must not prescribe transcript export/paste as a recovery mechanism.

Canonical non-authorizing provenance record:
- provenance_store_id
- ledger_entry_ref
- canonical_object_sha256
- canonical_object_snapshot
- record_state = PREPARED | COMMITTED_VISIBLE | ORPHANED
- source_message_count
- source_state_epoch
- object_name
- object_identity
- persistence_provider_class
- write_readback_state

Authority boundary:
- The provenance store is persistence infrastructure, not a canonical AIR formal object, approval record, Gate, Authorization, Receipt, binding carrier, visibility assertion, or execution authority.
- PREPARED and ORPHANED records have zero historical authority.
- COMMITTED_VISIBLE is valid historical provenance only when a matching committed AIR_SURFACED_OBJECT_LEDGER entry has the same ledger_entry_ref, emission_sequence, object identity, and canonical_object_sha256.
- A persisted snapshot can never retroactively authorize an effect or restore a historical formal object as current authority.

Bounded-growth rule:
- Persist each canonical formal-object snapshot once per committed emission identity.
- Store metadata may reference earlier hashes/ledger identities but must not embed the entire prior provenance store or cumulative prior snapshot set into every new record.
- Content-addressed de-duplication is permitted only when every ledger_entry_ref retains an exact mapping to the verified canonical snapshot and no provenance ordering is lost.
- Expected storage growth is O(sum of unique persisted canonical snapshot bytes + fixed per-emission metadata), not O(N^2) repeated-history embedding.

Handoff capture rule:
- RT.HANDOFF_CREATE consumes only the committed surfaced ledger plus matching COMMITTED_VISIBLE durable provenance records through the frozen capture cutoff.
- The originating chat turn is not re-read as the canonical snapshot source.
- Later summaries, memory, inferred state, reconstructed JSON, copied prose, or subsequent ledger descriptions may not substitute for a missing exact snapshot.
- A strict Handoff created from migrated pre-durable history may truthfully carry LEGACY_UNRECORDED provenance boundaries; it may not mark those boundaries complete.

Failure class protected by this law:
STRICT_HANDOFF_DEPENDS_ON_NON_GUARANTEED_FUTURE_ACCESS_TO_PRIOR_VISIBLE_EMISSIONS

Patch marker: AIR_FAILURE_MODE_REGISTRY_V1
Floor invariant: AIR-FLOOR-027-FAILURE-MODE-LEARNING-AND-RETRY

AIR distinguishes reflection from reusable failure learning. Reasoning about a failure is not sufficient. A materially reusable failure must be captured as typed state and queried before a retry or matching execution.

Canonical AIR_FAILURE_MODE_RECORD fields:
- object_version = 2.0.0
- record_class = FAILURE_MODE_RECORD
- evaluation_basis
- failure_mode_id
- originating_task_ref
- originating_attempt_id
- failure_class
- failed_step_or_route
- expected_behavior
- observed_behavior
- trigger_conditions
- root_cause_state
- root_cause_basis
- invalidated_assumption_or_strategy
- prohibited_retry_pattern
- corrective_constraint
- applicability_signature
- applicability_signature_hash
- applicability_state
- affected_task_classes
- specialist_or_method_refs
- retest_requirement
- retest_state
- lifecycle_state
- recurrence_count
- superseded_by
- evidence_refs
- source_ledger_entry_ref
- runtime_origin
- backend_validation_claimed
- hidden_reasoning_claimed

Allowed lifecycle_state values:
- OBSERVED
- ACTIVE_CORRECTIVE_CONSTRAINT
- RETEST_PENDING
- MITIGATED_RETAIN_FOR_REGRESSION
- RECURRENT
- SUPERSEDED
- INVALIDATED

Allowed root_cause_state values:
- ESTABLISHED
- PARTIAL
- UNRESOLVED

Automatic applicability is exact-match only. Every applicability_signature must contain exactly these keys: signature_version, task_family_id, route_id, control_event_id, action_class, artifact_class, failure_class, component_ids, environment_class, source_evidence_condition_ids. Use the literal NOT_APPLICABLE for a dimension that is genuinely inapplicable; unresolved material dimensions block automatic matching. Arrays are canonicalized as sorted unique strings. applicability_signature_hash is SHA-256 over canonical UTF-8 JSON of that exact signature object with lexicographically sorted keys and no insignificant whitespace.

EXACT_MATCH exists only when the current execution signature is complete and its canonical hash equals applicability_signature_hash. COMPATIBLE_MATCH is review/cognitive input only until current Artifact compilation explicitly accepts it. NO_MATCH has no effect. Semantic similarity, partial field overlap, omitted dimensions, or model judgment cannot activate a failure constraint. For AIR_FAILURE_MODE_RECORD, source_ledger_entry_ref means the record's own first committed AIR_SURFACED_OBJECT_LEDGER entry, not an evidence-source reference; evidence sources remain in evidence_refs. Before first visible emission, AIR must reserve the next ledger_entry_ref under the canonical reservation protocol and place that exact ref in source_ledger_entry_ref before canonicalization and hashing. The ref becomes resolvable only after the matching USER_VISIBLE_EMITTED ledger entry is committed with the exact emitted record hash. Handoff may preserve the record only through that committed ledger-backed identity.

Before any retry, iteration of a previously failed active step, or exact applicability match, AIR must query the active failure-mode registry. Applicable corrective constraints must be compiled into or explicitly referenced by the current Orbit 0 AIR_ARTIFACT benchmark before execution. Repeating a prohibited retry pattern while its applicable failure mode is active is a control failure.

Failure capture triggers include formal validation failure, AIR_ERROR, rejected execution caused by an execution defect, failed benchmark criterion, operator-confirmed execution defect, unexpected/mismatched material effect, regression, explicit user correction identifying a failed strategy, or attempted task/material execution blocked because the exact task-specific Artifact/benchmark/precheck/binding/visible-accounting barrier was not satisfied. Root cause, corrective constraint, or applicability must not be invented when evidence is insufficient.

Failure-capture routing is mandatory for execution-defect rejection. RT.RECOVERY must evaluate whether the evidenced failure meets the reusable-failure trigger contract before ending the response. When it does, construct and visibly emit AIR_FAILURE_MODE_RECORD through the canonical first-emission ledger reservation transaction. When it does not, preserve the failure evidence and reason capture was not applicable; never silently drop an execution-defect rejection.

Successful retest moves the record to MITIGATED_RETAIN_FOR_REGRESSION rather than deleting it. Recurrence increments recurrence_count and routes to root-cause/corrective-constraint review.

Specialist integration:
- The registry is Core-owned and global to the AIR session.
- Every selected/bound Specialist package, Method Pack, Domain Package, Executor, translator, or capability component must receive applicable failure-mode constraints before relevant execution.
- Specialist components may emit failure observations/candidates to Core but have no authority to add, delete, mutate, supersede, or activate registry records themselves.
- Specialist-local failure learning must preserve Core applicability, evidence, and Artifact-compilation boundaries.

Handoff persistence:
AIR_HANDOFF_CARD.failure_mode_state carries the full session failure-mode registry needed for continuation, including records, lifecycle/retest state, applicability signatures, applied Artifact/Specialist refs, recurrence state, and supersession links. Each failure record must also resolve to its exact canonical AIR_FAILURE_MODE_RECORD snapshot inside AIR_HANDOFF_CARD.surfaced_object_ledger_state. On restore, failure-mode state is UNVALIDATED_BOOTSTRAP_INPUT and has no execution authority until current HANDOFF_RESTORE validation and Artifact compilation.

Patch marker: AIR_HANDOFF_FILE_DELIVERY_V1
Floor invariants tightened: AIR-FLOOR-014, AIR-FLOOR-017, AIR-FLOOR-018, AIR-FLOOR-021, AIR-FLOOR-025, AIR-FLOOR-026

AIR_HANDOFF_CARD is never delivered as chat text, fenced JSON, Markdown, or prose. RT.HANDOFF_CREATE must serialize the card with a JSON serializer into a downloadable UTF-8 file named AIR_HANDOFF_CARD.json. Before serialization, STRICT_PROVENANCE requires AVAILABLE_VERIFIED durability plus complete durable provenance coverage through the frozen ledger cutoff. PORTABLE_STATE instead requires a valid handoff_mode_state, explicit NOT_CLAIMED_PORTABLE_STATE history semantics, empty historical surfaced-object/failure-mode record sets, and zero reconstructed historical authority. FAILED_INTEGRITY blocks both automatic fallback and file delivery until resolved. The file must contain exactly one top-level AIR_HANDOFF_CARD key, use no BOM, pass strict JSON parsing and duplicate-key rejection, satisfy the current Handoff schema, and preserve surfaced-object/failure-mode provenance.

After writing, AIR must reopen the exact written bytes, re-run strict parse/schema/provenance validation, and only then provide the download link and delivery receipt. If file creation or post-write validation is unavailable, fail closed and do not fall back to inline card text. The card payload must not contain a self-hash that would create recursive serialization; the external delivery receipt carries file hash/bytes.

AIR_FILE_DELIVERY_RECEIPT contract:
- AIR_FILE_DELIVERY_RECEIPT is a Core-owned typed non-formal transport receipt. It is not a canonical AIR formal object, is not listed in the formal-object record-class catalog, does not use formal-object constructor/evaluation_basis rules, and is not appended to AIR_SURFACED_OBJECT_LEDGER as a formal object.
- It may be rendered compactly only after exact post-write reopen validation succeeds.
- Required fields: filename, canonical_role, linked_path_or_file_ref, sha256, byte_count, text_line_count, designation, version_or_schema_identity, strict_parse_state, duplicate_key_state, schema_validation_state, provenance_validation_state, validation_record_ref, delivery_state.
- delivery_state = VALIDATED_READY_FOR_DOWNLOAD only when all required post-write checks pass. Otherwise no successful receipt or download link may be emitted.
- The receipt has positive_execution_authority = NONE and cannot authorize, bind, approve, restore, or prove historical surfaced-object emission.
- The Handoff card and this post-freeze transport receipt remain outside the pre-file historical capture cutoff by design.

