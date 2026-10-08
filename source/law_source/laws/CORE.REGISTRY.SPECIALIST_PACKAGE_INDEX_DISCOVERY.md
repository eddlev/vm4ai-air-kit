==================================================
AIR SPECIALIST PACKAGE INDEX DISCOVERY CONTRACT
==================================================
Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_DISCOVERY_V1

Purpose:
Allow AIR to discover which reusable Specialist packages exist in the current AIR release without loading every Specialist prompt into every session.

Canonical discovery artifact:
- designation: AIR_SPECIALIST_PACKAGE_INDEX_V1
- canonical filename: AIR_SPECIALIST_PACKAGE_INDEX.json
- role: compact release-level discovery metadata only
- execution authority: NONE
- binding authority: NONE

Minimum index entry:
- package_identity
- specialist_designation
- manifest_filename
- package_version
- manifest_sha256 when release-sealed
- canonical_component_filenames
- capability_tags
- short_activation_summary
- short_non_activation_summary
- foundation_compatibility_identity
- availability_state in { RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION, RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION, RELEASE_CATALOG_ENTRY }

Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1
Candidate-to-release lifecycle:
- RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION = candidate bytes are discoverable but current deterministic/static validation has not passed; this is not a released catalog entry.
- RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION = current deterministic/static validation has passed for the candidate bytes, but required replayable/model-host behavioral evidence remains pending; this is not a released catalog entry.
- RELEASE_CATALOG_ENTRY = release-sealed catalog entry. This state may be emitted only after the release process closes every validation requirement declared by that release and the release-sealed index carries the exact manifest receipt.
- Candidate states are discovery metadata only and never grant selection, approval, binding, or execution authority.

Index rules:
- Index presence does not make any Specialist package present, selected, validated for the current task, approved, or bound.
- An index entry may establish that a package identity exists in the release catalog and provide its expected manifest identity; actual package bytes must still be supplied/available and validated before use.
- The index must remain compact; it is a discovery directory, not a copy of Specialist profiles.
- The current release index should identify AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2 as the canonical reusable-Specialist construction route.
- If the index is absent, stale, or incompatible, AIR may use only Specialist identities independently established by current validated session/package state. It must not fabricate catalog completeness or claim that no matching package exists solely because the index is unavailable.
- When specialist discovery becomes material and the index is unavailable, state discovery as degraded; request the smallest resolving input only when current validated state cannot determine the route.
- A final release that claims offline deterministic Specialist discovery must ship a current release-sealed AIR_SPECIALIST_PACKAGE_INDEX.json.

