# AIR AMRS-6 Patch Notes — R23

> Public AIR Kit version: **v0.8.0**.  
> Promoted runtime artifact: `AIR_P_COMPLETE_CLIENT_RELEASE_20261008_R23_BOOT_PROFILE_CANDIDATE_V5.zip`  
> SHA-256: `c7b11af137d4fb284afba11ef23c41c0d3812f49cffcfd8a7a51aa24e6042d64`  
> AMRS readiness: **AMRS-6 — Production Approved**

## What changed

AMRS-6 is a production-readiness hardening release for AIR's prompt/runtime governance model. The patch closes the AMRS-6 requirement set across runtime intent and acceptance, execution steering, bounded response transactions, state lifecycle, formal-object construction, approval/control-plane integrity, provenance, response termination, startup, Specialist distribution, trust/authenticity, compatibility, and validation.

### Runtime and execution governance

- Added explicit AMRS intent/readiness and acceptance architecture.
- Hardened Execution Steering and checkpointed task orchestration.
- Tightened bounded response-transaction behavior and material-action sequencing.
- Clarified Artifact lease lifecycle, pre-binding approval/Gate handling, formal-object constructor dependency closure, and ledger/provenance behavior.
- Preserved fail-closed authority separation between direction, approval, authorization, effect, receipt, and reconciliation.

### State normalization and lifecycle

- Separated canonical current state, durable derived rules, and historical evidence so superseded/historical state cannot compete with operative state.
- Added stronger persistent-state lifecycle, supersession, invalidation, retirement/GC, handoff, restoration, and provenance discipline.

### Response sufficiency and interaction recovery

- Added a receiver-facing completion-envelope stop rule once the requested work is complete unless a real blocker, safety/governance need, required next action, or explicit user request requires continuation.
- Topic/task switches invalidate prior conversational material that is no longer needed.
- Corrections repair the affected state locally instead of replaying unrelated history.
- Helpfulness cannot silently expand a completed scope.

### Progressive retrieval and boot profiles

- Added proportional runtime retrieval with `TIER_0_ROUTINE`, `TIER_1_NAVIGATION`, `TIER_2_TARGETED_SOURCE`, and `TIER_3_DEEP_AUDIT` boot profiles.
- Added closed retrieval planning so navigation and targeted-source work do not automatically pull unrelated authoritative bodies into model context.
- Routine Tier0 boot reaches onboarding readiness without blanket full-package verification unless a real escalation trigger requires it.

### Package, law and Specialist integration

- Completed package-enabled law-source ownership and Router83 integration.
- Preserved exact law-package identity and fail-closed source resolution.
- Includes the five catalogued Specialist package distributions and compact runtime navigation/reference surfaces.
- Client distribution excludes compiler/test executable source and script payloads.

## Validation and acceptance

The promoted R23 V5 artifact passed:

- deterministic static release closure;
- **5/5** required fresh-session functional acceptance cases;
- full Tier3 pinned-package audit;
- boot-performance acceptance at **121 seconds**, against a **300-second** limit.

Release boundary:

- 181 distribution files;
- 179 boot-manifest pins;
- 140 `air_p` client files;
- 115 law-package files;
- zero script payloads.

## External QA contribution — Monica Angiuli

**Monica Angiuli — External AI QA Auditor – Behavioral & Interaction Testing**

Monica's external behavioral QA identified interaction and state-management failure modes that informed specific AMRS-6 hardening work. Her supported contribution trace includes:

- **R04/M04** — state-plane normalization and canonical current-vs-historical separation;
- **R05/M05** — persistent-state lifecycle, supersession and stale-state hardening as an architecture response to the state defects exposed by testing;
- **R10/M10** — response sufficiency and termination, including completion stopping, topic-switch invalidation, local correction repair, and prevention of helpfulness-driven post-completion scope expansion.

Public profile: https://mony2026.substack.com/

This recognition does not imply employment, code co-authorship, ISO/regulatory/certification auditing, or customer endorsement, and it does not attribute unrelated AMRS-6 architecture to Monica.

## Release identity and provenance

The promoted bytes retain the original candidate filename and build-time metadata for provenance. Their post-acceptance status is established by the AIR promotion designation, not by rewriting the archive.

`AIR_P_COMPLETE_CLIENT_RELEASE_20261008_R23_BOOT_PROFILE_CANDIDATE_V5.zip`  
SHA-256: `c7b11af137d4fb284afba11ef23c41c0d3812f49cffcfd8a7a51aa24e6042d64`