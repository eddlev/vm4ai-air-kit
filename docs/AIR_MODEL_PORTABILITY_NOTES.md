# AIR Model Portability Notes

AIR is designed to be prompt-native and portable across capable LLM platforms, but boot quality and handoff restoration vary by model and interface.

This document records observed behavior and recommended prompts.

## Portability principle

AIR must treat model/provider availability as a dependency, not an assumption.

Negative rule:

AIR must not depend on a single model provider, hosted platform, deployment environment, jurisdictional access regime, or residency policy.

Positive principle:

AIR should preserve project continuity through portable state, local-first artifacts, provider fallback notes, and model-specific boot guidance.

## Status labels

- `CURRENT_SESSION_BASELINE` - the model currently driving AIR development work.
- `TESTED_BOOT_OK` - booted successfully in observed testing.
- `TESTED_BOOT_WITH_STRICT_PROMPT` - booted successfully only with stricter wording.
- `TESTED_HANDOFF_OK` - restored a full handoff cleanly.
- `TESTED_HANDOFF_OK_SLOW` - restored correctly but slowly.
- `TESTED_HANDOFF_PARTIAL` - partially restored, with limitations.
- `TESTED_HANDOFF_DRIFT_RISK` - restored some state but drifted or regressed.
- `NOT_RECOMMENDED_FOR_FULL_AIR_HANDOFF_CONTINUATION` - not recommended for large handoff restoration.
- `NOT_TESTED` - no reliable test yet.

## Observed model notes

### ChatGPT-5.5 Thinking

Status: `CURRENT_SESSION_BASELINE`

Use:

- primary observed AIR development session
- strong long-context continuity
- prompt-doctrine design
- bounded implementation planning
- claim-boundary preservation
- git/test gate coordination when working with an operator

Caution:

- still prompt-side unless backed by repo/runtime evidence
- model behavior is not backend validation or runtime enforcement

### Claude / Opus 4.8 High

Status: `TESTED_HANDOFF_OK_SLOW`

Use:

- complex continuation
- deep state recovery
- truncated-card detection
- claim-boundary preservation

Observed:

- correctly detected truncated handoff card
- refused to fabricate completed steps or next action
- recovered later state from a complete transcript/handoff
- preserved prompt/backend claim boundaries

Caution:

- slow boot and slow large-card processing
- patience advised

### Grok

Status: `TESTED_HANDOFF_OK`

Use:

- full handoff continuation
- compact restoration
- prompt-side project state continuation

Observed:

- restored STEP 2B.4e from full handoff
- preserved completed-step chain and claim boundary
- asked for confirmation before proceeding

Caution:

- may generalize next action when the card is truncated

### Kimi

Status: `TESTED_HANDOFF_GOOD_BUT_ADVANCES_TOO_EARLY`

Use:

- structured restoration
- compact AIR_SESSION rendering
- claim-boundary preservation

Observed:

- restored completed 2B.1 through 2B.4d
- preserved no-LEVEL_3 boundary
- selected a later next step while an in-progress REVIEW_GATE step still existed

Caution:

- tell Kimi explicitly not to advance past an in-progress REVIEW_GATE step

Recommended addition:

```text
If the handoff contains an in-progress REVIEW_GATE step, do not advance to the later recommended step. Restore the in-progress step as current.
