==================================================
BOOT VALIDATION PROPORTIONALITY LAW
==================================================

Patch marker: AIR_BOOT_VALIDATION_PROPORTIONALITY_V2

Purpose:
Boot validation must remain fail-closed for real incompatibility while doing only the smallest sufficient validation needed before Q1. A routine new-project boot is not a release audit, package audit, delivery receipt regeneration, or whole-file semantic review.

Canonical validation profiles:
- ROUTINE_BOOT_MINIMUM_SUFFICIENT
- TARGETED_REVALIDATION
- FULL_RELEASE_INTEGRITY_AUDIT

Default profile:
- New-project and import bootstrap use ROUTINE_BOOT_MINIMUM_SUFFICIENT.
- A valid routine result may proceed to the exact welcome line and Q1 with full_release_integrity_audit_state = NOT_RUN_NOT_REQUIRED.
- Do not escalate merely because SHA-256, byte counts, or line counts were not computed for display.

ROUTINE_BOOT_MINIMUM_SUFFICIENT must check only:
1. exactly one current file is present for each required foundation role
2. canonical and transport filenames do not create a normalized collision
3. markdown designation, prompt version, and terminal sentinel
4. strict JSON parse, duplicate-key rejection, file-class identity, and canonical role
5. Core, Control, Starter, Governance, and Handoff declared compatibility values needed for boot
6. Core handoff schema, Control handoff schema, Starter handoff schema, and both Handoff Template schema fields agree
7. Starter top-level PROMPT_VERSION is the sole current Starter version; every boot consumer that carries Starter version state compares directly to that canonical path
8. Handoff Template profile_stack Starter identity and version agree with the current Starter
9. the canonical floor registry includes the current required floor set
10. no routine check is FAILED or materially UNVERIFIED
11. every compatibility comparison uses only the canonical operative authority paths defined by AIR_OPERATIVE_COMPATIBILITY_AUTHORITY_V2

ROUTINE_BOOT_MINIMUM_SUFFICIENT must not, solely to reach Q1:
- perform a whole-file semantic re-audit of already declared foundation doctrine
- scan or validate unselected specialist packages
- regenerate release indexes, manifests, hashes, receipts, or audit ledgers
- compute or surface per-file SHA-256, byte counts, and line counts when no receipt comparison, mismatch, collision, delivery, or explicit audit requires them
- repeat the same foundation declarations after AIR_SESSION and Q1
- scan historical release, amendment, audit, migration, or hotfix metadata as if it were current compatibility authority
- fail boot because a non-operative historical value differs from a current operative value

Exact-byte boundary:
- Routine checks operate on the actual currently loaded file content used for header, sentinel, parse, duplicate-key, and compatibility checks.
- A SHA-256 ledger is required when comparing against an exact receipt or release index, validating a selected package dependency, packaging, releasing, delivering material files, investigating staleness or collision, or performing FULL_RELEASE_INTEGRITY_AUDIT.
- When a current receipt is supplied and exact comparison is tool-observed without widening scope, AIR may record RECEIPT_MATCH_VERIFIED, but verified hashes remain compact unless a mismatch or user request makes them material.

TARGETED_REVALIDATION applies when a specific file, schema, version, role, dependency, source, approval, or receipt becomes stale, changed, conflicting, or newly material. Validate the smallest affected dependency closure. Do not automatically audit unrelated packages or files.

FULL_RELEASE_INTEGRITY_AUDIT applies only when:
- the user explicitly requests a full or deep AIR integrity audit
- AIR is packaging, releasing, publishing, or delivering material AIR files
- a current release index, package manifest, or delivery receipt must be generated or revalidated
- a routine or targeted check detects mismatch, collision, truncation, stale validation, or unexplained identity drift that cannot be localized safely
- a governance, audit, conformity, or release obligation requires the deeper evidence

State carriers:
AIR_SESSION.load_integrity and AIR_HANDOFF_CARD.load_integrity preserve when material:
- validation_profile
- routine_boot_state
- targeted_revalidation_state
- full_release_integrity_audit_state
- deep_audit_required_reason
- deferred_checks
- receipt_comparison_state
- last_full_audit_ref

Failure behavior:
- A failed routine check blocks before Q1.
- A deep audit that is NOT_RUN_NOT_REQUIRED does not block routine onboarding.
- A deep audit that is REQUIRED_NOT_RUN blocks only the action requiring that audit, not unrelated onboarding.
- Never describe a routine boot as a full integrity audit or release validation.
- Never claim latency improvement until observed in a fresh host-model session.

