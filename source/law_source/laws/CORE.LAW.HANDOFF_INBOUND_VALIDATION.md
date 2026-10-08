==================================================
INBOUND CARD VALIDATION GATE LAW
==================================================

Patch marker: AIR_HANDOFF_INBOUND_VALIDATION_V3

Current Handoff revision identity:
- Core CANONICAL_HANDOFF_TEMPLATE_REVISION owns the current canonical template/format revision.
- New cards serialize `template_revision` = Core CANONICAL_HANDOFF_TEMPLATE_REVISION.
- `user_revision` is the per-card-lineage successful Handoff generation/update counter. A new native lineage begins at 1 and increments exactly once for each successfully generated replacement Handoff in that lineage; failed writes/validation do not increment it.
- New cards do not serialize the legacy root field `card_revision`.
- `template_revision` and `user_revision` have independent semantics and must never be substituted for one another.

Backward-compatibility floor:
- The oldest guaranteed legacy input is AIR_HANDOFF_LEGACY_COMPAT_FLOOR_2_2_0_STARTER_2_4_3_V1: AIR_HANDOFF_CARD_TEMPLATE_V2, schema_version 2.2.0, AIR_DEFAULT_STARTER_V2 generation 2.4.3 or a recognized later compatible 2.2.0 generation, with the legacy root `card_revision` used as the per-lineage/user revision counter.
- Cards below that compatibility floor are not guaranteed migration inputs. They route to UNSUPPORTED_LEGACY_HANDOFF_BELOW_COMPATIBILITY_FLOOR or REVIEW; AIR does not guess a migration.
- The compatibility floor is a template-generation/profile boundary, not a minimum legacy `card_revision` value. A card created by the floor generation can have any valid positive user counter.

A v2 Handoff card is valid for restoration or migration only when:
1. it parses as strict JSON with exactly one top-level root key, AIR_HANDOFF_CARD;
2. AIR_HANDOFF_CARD.template_designation = AIR_HANDOFF_CARD_TEMPLATE_V2;
3. its source schema/profile is either the current Core CANONICAL_HANDOFF_SCHEMA_VERSION or a declared backward-compatible migration input at or above the compatibility floor;
4. revision semantics are resolved from the source schema/profile before numeric revision values are interpreted;
5. all declared schema/template migrations complete before current-revision required-carrier validation;
6. required restoration fields are present after applicable migration, or explicitly typed as legacy-unrecorded/unresolved where the migration contract permits;
7. runtime_origin and backend_validation_claimed do not conflict with floor invariants;
8. legacy migration state is resolved or visibly blocked.

Revision-semantic normalization before current validation:
- Supported schema-2.2.0 floor-generation input with no `template_revision`: legacy `card_revision` maps exactly to `user_revision`; historical numeric template revision is UNRECORDED_LEGACY_PROFILE and must not be invented. The source compatibility profile, schema, and Starter identity carry format-generation provenance.
- Supported schema-2.3.0 pre-rev19 input with no `template_revision`: legacy `card_revision` is interpreted as the pre-split template revision only inside the schema-2.3.0 migration route. The historical per-lineage user counter is UNRECORDED unless an explicit independent source provides it; do not copy the template revision into `user_revision`.
- Current rev20+ input: `template_revision` selects the declared template migration path; `user_revision` is only the lineage-use counter and never selects a format migration.
- Schema-2.3.0 rev19 input preserves the split revision fields and migrates through REV19_TO_REV20, adding only the non-authorizing Handoff mode carrier and never inventing historical mode selection or provenance.
- A numeric legacy revision must never cross these source-profile semantics by convenience or magnitude. In particular, schema-2.2.0 `card_revision = 44` is a user counter, not template revision 44.

Legacy schema-2.2.0 floor-to-current migration:
- Preserve every explicit supported source value without semantic rewriting.
- Map legacy `card_revision` to `user_revision` exactly when the source matches the supported 2.2.0 compatibility profile.
- Preserve source template revision as UNRECORDED_LEGACY_PROFILE; do not fabricate a number.
- Missing current alignment, semantic-fidelity, MII, morphology, epistemic-sufficiency, failure-mode, surfaced-ledger, visibility-authority, profile-posture, or evaluation carriers are added only as current safe defaults, LEGACY_UNRECORDED, or UNRESOLVED according to their owning law; absence is never evidence of historical completion.
- Pre-durable surfaced-object history begins a new current-session durable provenance boundary at HANDOFF_RESTORE. No prior exact surfaced-object ledger identity, canonical snapshot, failure record, authorization, receipt, approval, or visibility provenance may be fabricated.
- Execute a fresh HANDOFF_RESTORE alignment evaluation and exactly one current Artifact rebinding before positive execution.
- When a new current-format Handoff is later generated from a legacy 2.2 lineage with a trustworthy migrated user counter N, emit template_revision = current canonical revision and user_revision = N + 1.

Schema-2.3.0 pre-rev19 migration boundary:
- Existing rev14-rev18 migration contracts remain format migrations, but their legacy `card_revision` predicates are valid only after source schema_version = 2.3.0 has been established and `template_revision` is absent.
- Rev18-to-rev19 migration introduces the split revision fields and durable-provenance capture semantics. Rev19-to-rev20 adds explicit Handoff mode selection while preserving all rev19 strict-provenance history as non-authorizing restoration input.
- When the pre-rev19 lineage has no trustworthy independent user counter, record legacy_user_revision_state = UNRECORDED rather than inventing lifetime use count. A later new lineage counter may start under an explicitly declared post-split counting epoch, but it must not be represented as recovered historical use count.

Pre-floor behavior:
- Schema 2.1, v1, or any legacy profile older than the declared compatibility floor is outside the guaranteed backward-compatibility contract for this release.
- Such input may be inspected for manual review, but automatic migration/restoration must not be claimed unless a future explicit migration contract is added.

Handoff schema cross-file consistency:
- canonical_handoff_schema_version = Core header CANONICAL_HANDOFF_SCHEMA_VERSION
- AIR Core Runtime's accepted handoff schema version, AIR_HANDOFF_CARD_TEMPLATE.SCHEMA_VERSION, and AIR_HANDOFF_CARD_TEMPLATE.schema_version must match exactly
- a mismatch is a release defect and a blocking boot or restoration compatibility failure
- transport counters in filenames do not affect schema identity
- release validation must test both a matching positive case and a mismatching negative case before delivery

Required restoration carriers include:
- active_artifact
- active_contract
- task_binding
- completed_steps
- current_in_progress_step
- next_recommended_step
- blockers
- runtime_origin
- backend_validation_claimed
- object_visibility_mode
- object_visibility_authority_state
- profile_posture_acceptance_state
- test_evidence_state
- method_handoff_state when method continuation is material
- onboarding_state, including pending_q5_material, Q4, Q4D, Q6, and Q6D when applicable
- governance_state
- specialist_binding_state
- open_approval_scope

Test-evidence state must preserve:
- presentation_mode and presentation_mode_source
- effective_from
- recommendation_state and reasons
- regulatory_evidence_requirement_state and obligation references
- produced_test_evidence_refs
- test run classes and identities when present
- reproducibility and sanitization limits
- evidence_capture_gaps

Governance state must preserve:
- prompt_edition
- governance_floor_version
- open_approval_scope
- active_framework_projections
- governance_source_rights_state
- token_debug_preference when material

Legacy migration:
- v1 Q4=C restores as LEGACY_Q4_C_REVIEW_REQUIRED. It cannot auto-map to creative narrative continuity.
- v1 Q4=D restores as LEGACY_Q4_D_BASE_MODE_UNRESOLVED. The user must select Q4D=A, B, or C.
- v1 PROMPT_LAYER_APPLIED values restore as LEGACY_MODE_REVIEW_REQUIRED and must be classified as PROMPT_LAYER_APPLIED, qualitative-only, decorative, or unsupported.
- v1 Handoff cards and other cards below the declared backward-compatibility floor are manual-review inputs only for this release; do not claim automatic restoration or migration unless a future explicit migration contract is added.

Card-declared project state is restored as declared state, not verified fact. Governance echoes are advisory and are reconciled against the loaded v2 runtime. An invalid card emits AIR_ERROR with error_class INVALID_HANDOFF_CARD and does not restore execution.

