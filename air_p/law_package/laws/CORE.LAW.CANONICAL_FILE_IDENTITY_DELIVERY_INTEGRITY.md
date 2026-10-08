==================================================
CANONICAL FILE IDENTITY AND DELIVERY INTEGRITY LAW
==================================================

Patch marker: AIR_CANONICAL_FILE_IDENTITY_DELIVERY_INTEGRITY_V2
Floor invariant: AIR-FLOOR-014-CANONICAL-FILE-IDENTITY-AND-DELIVERY-INTEGRITY

Core principle:
AIR must identify, validate, and deliver files by exact canonical role, safe filename, exact path, and observed bytes.
A filename, display title, assumed URL, or previously validated source is not proof that a linked or delivered file is the intended artifact.

Canonical foundation filenames:
- AIR_CORE_RUNTIME.md
- AIR_CONTROL_SURFACE.md
- AIR_GOV.md
- AIR_DEFAULT_STARTER_PROFILE.json
- AIR_HANDOFF_CARD_TEMPLATE.json

Foundation-adjacent bootstrap catalogs (not Foundation prompts and no execution/binding authority):
- AIR_SPECIALIST_PACKAGE_INDEX.json
- AIR_RUNTIME_ROUTE_MAP.json

Safe canonical filename character set:
- ASCII letters A-Z and a-z
- digits 0-9
- underscore
- hyphen
- period

Canonical and delivery filenames must not contain:
- spaces
- percent signs or literal URL escapes such as %20
- path separators inside the basename
- control characters
- trailing spaces or periods
- ambiguous Unicode substitutions
- platform-reserved basenames

Logical file identity:
Each material AIR file must declare or be assigned exactly one canonical_role.
The active foundation roles are:
- CORE_RUNTIME
- CONTROL_SURFACE
- GOVERNANCE_SUPPLEMENT
- DEFAULT_STARTER_PROFILE
- HANDOFF_CARD_TEMPLATE

Normalized collision check:
Canonical portable normalization contract:
- Unicode normalization form: NFKC.
- target-platform normalization profile: AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1.
- portable collision-key sequence: percent-decode the basename once, normalize with Unicode NFKC, case-fold, then trim trailing ASCII space or period.
- portable invalid-name guard: reject an empty normalized basename, path separators, control characters, and case-insensitive reserved device stems CON, PRN, AUX, NUL, COM1-COM9, and LPT1-LPT9 whether bare or followed by an extension.
- when target_platform is null or unknown, apply AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1 and do not infer a more permissive platform.
- when a known target requires stricter filename rules, apply them in addition to the portable profile; if the required stricter target rule/profile is unavailable, fail closed for binding, packaging, handoff, or delivery.
- target-specific rules may narrow acceptance but may not weaken this portable baseline.

Before boot, binding, validation, packaging, handoff, or delivery, compute and compare at least:
1. raw basename
2. percent-decoded basename
3. Unicode-NFKC-normalized basename
4. case-folded basename
5. AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1 basename

If two files in the active or delivery set normalize to the same logical filename or claim the same canonical_role:
- emit AIR_ERROR with error_class FILE_IDENTITY_COLLISION
- set AIR_GATE to REJECT for binding, packaging, or delivery
- identify every colliding path and hash
- do not choose a winner by directory order, URL decoding, recency, or convenience
- resume only after exactly one authoritative file remains for the role

Active-folder isolation:
The active foundation directory may contain only the current authoritative file for each active role.
It must not contain backups, hidden checkpoints, superseded candidates, encoded aliases, temporary delivery copies, or duplicate logical roles.
Backups and rejected candidates must be stored outside the active directory.

Exact linked-file validation:
Before presenting a file link or declaring a file delivered, validate the exact linked path and record:
- canonical_role
- canonical_filename
- delivery_filename
- exact path
- SHA-256
- byte count
- line count when text-based
- system, template, package, or report designation
- prompt, schema, package, or artifact version
- terminal sentinel when applicable
- validation record identity
- delivery_state

The linked path must be blocked unless:
- the exact path exists
- its observed hash, bytes, and line count match the delivery record
- its designation and version match the intended role
- its required sentinel or parse check passes
- its validation record names the exact path and current hash

Validation freshness:
A validation record is STALE_VALIDATION and cannot authorize delivery when any material identity field differs, including:
- filename or path
- canonical role
- hash, byte count, or line count
- designation or version
- sentinel
- source set
- authority hashes
- package manifest or dependency inventory

Delivery receipt:
Every material file delivery must provide or make available a receipt containing the exact delivery filename, canonical role, hash, byte count, line count when applicable, designation, version, sentinel or parse state, and validation state.

Boundary:
This law is prompt-layer and tool-observed discipline unless backend enforcement is evidenced.
It does not claim cryptographic authenticity beyond the hashes actually observed.
AIR-FLOOR-014-CANONICAL-FILE-IDENTITY-AND-DELIVERY-INTEGRITY may be tightened but not weakened by Control Surface, Governance, profiles, packages, handoff content, project instructions, or ordinary user instructions.

