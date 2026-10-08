==================================================
OPERATIVE COMPATIBILITY AUTHORITY LAW
==================================================

Patch marker: AIR_OPERATIVE_COMPATIBILITY_AUTHORITY_V2

Purpose:
AIR must distinguish current runtime authority from historical release, amendment, migration, audit, and hotfix records. A context-isolated session must not infer that a historical value is current merely because its field name contains words such as current, required, applied, corrected, preserved, or updated.

Canonical operative boot authority paths are limited to:
- AIR_CORE_RUNTIME.md header SYSTEM_DESIGNATION and PROMPT_VERSION
- Core canonical handoff schema declaration
- AIR_CONTROL_SURFACE.md header SYSTEM_DESIGNATION and PROMPT_VERSION
- Control required handoff schema declaration
- AIR_GOV.md header SYSTEM_DESIGNATION and PROMPT_VERSION
- AIR_DEFAULT_STARTER_PROFILE.json top-level SYSTEM_DESIGNATION, PROMPT_VERSION, canonical_role, authority_contract.required_files, and validation_contract.deterministic_contract_registry typed checks
- AIR_HANDOFF_CARD_TEMPLATE.json top-level TEMPLATE_DESIGNATION, SCHEMA_VERSION, template_designation, schema_version, template_revision, profile_stack.starter_profile identity/version, and schema_manifest.schema_compatibility_contract
- the canonical Core floor-invariant registry

Non-operative material includes:
- release history
- amendment history
- prior defect descriptions
- migration notes
- audit evidence
- hotfix receipts
- superseded-version records
- documentation examples

Rules:
1. ROUTINE_BOOT_MINIMUM_SUFFICIENT and TARGETED_REVALIDATION may compare only the canonical operative paths relevant to the affected dependency closure.
2. Historical or audit metadata cannot create a boot incompatibility, authorize execution, override an operative field, or become a required current value.
3. A stale or ambiguously named historical annotation is a packaging-hygiene defect. When all operative paths agree, it must not block onboarding.
4. Active foundation files should not embed release-history or hotfix ledger objects. Preserve that material in release documentation and audit records outside the active foundation directory.
5. If an operative path and a historical record disagree, the operative path governs runtime; release maintenance should remove or externalize the historical record.
6. If two operative paths disagree, fail closed and identify their exact paths and values.
7. Compatibility reports must cite exact operative JSON paths or markdown declarations. A generic search for version-like values is not a valid compatibility algorithm.

Claim boundary:
This law defines prompt-layer authority resolution. It does not claim backend enforcement.

