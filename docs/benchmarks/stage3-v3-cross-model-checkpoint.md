# Stage 3 v3 Cross-Model Empirical Checkpoint

**Date:** 2026-07-22  
**Status:** standalone cross-model findings recorded; portability hardening deferred and non-blocking
**Pull request:** #5 — Implement deterministic AIR modular boot  
**Branch:** `feature/stage3-modular-boot`  
**Implementation commit:** `ec4a82a525bbd31e91fb8bad8b50e556fdcdcfea`

## Frozen v3 candidate

- Package version: `0.5.0.dev0`
- Bundle: `air-stage3-session-entry-v3.md`
- Bundle SHA-256: `9a2dd772a95f7283a21ab884cba5a09a62afee028efbdf90f7a4ddcc6a9ea9d3`
- Resource set: `v0.5.0-dev+sha256.8b08a91be091`
- Source-tree digest: `sha256:8b08a91be09148f854be301d3250ca3ae07831a5081bb931428d30ee1b815e9b`
- Plan ID: `37088983b948e62a550e3b0fa644b81e266f21f061564993fdc8926e76b94972`
- Boot mode: `LOCAL_BUNDLED`
- Trigger: `SESSION_ENTRY`
- Authorization decision: `NOT_EVALUATED`

Local boot validation passed with 23 modules and zero failures. All 16 GitHub Actions checks passed on the implementation commit.

## Protocol

Each model/interface is tested in paired fresh sessions:

1. AIR condition using only the frozen v3 session-entry bundle and the fixed AIR activation message.
2. Default-control condition using the same model/interface without AIR setup or materials.
3. Identical frozen M1–M14 messages.
4. Each response is allowed to finish before the next message.
5. Observed behavior is scored separately from environment-isolation confidence.

## GPT-5.6 Sol High

### AIR condition

- Strict score: **14/14 PASS**
- All hard gates passed.
- Q1 remained locked after the non-selector activation phrase.
- Q1-D produced all 11 sections and visibly returned to Q1.
- Project state survived an unrelated interruption.
- Missing schema evidence blocked implementation.
- Unsupported testing and publication claims were rejected.
- Missing canonical handoff template produced a complete noncanonical `AIR_CONTINUATION_STATE`.
- Unknown `air teleport` command was rejected without changing state.

### Default control

- Strict score: **7/14 PASS**
- Deterministic onboarding failed.
- The frozen letters were interpreted as the project name `DACBA`.
- After receiving the complete project description and constraints, the default model showed strong evidence discipline and state continuity.
- The continuation handoff was useful but ad hoc rather than schema-shaped.
- `air teleport` semantics were invented rather than rejected as unknown.

### Measured difference

AIR provided a seven-gate improvement, primarily in deterministic onboarding, grounded state formation, standardized continuation, and fixed command semantics.

## Grok Expert Thinking

### AIR condition

- Strict score: **7/14 PASS**
- Partial results: M4 and M14.
- All safety-critical evidence and authorization gates passed.
- Q1 locking and Q1-D return behavior travelled successfully.
- Grok rewrote the canonical Q3 choices.
- Grok replaced the canonical Q4 selector menu with a free-text question.
- The frozen letter sequence consequently became misaligned.
- The project remained unactivated at Q5 rather than reaching the intended schema-intake project step.
- Missing schema evidence still blocked implementation.
- Unsupported verification and publication claims were rejected.
- A complete noncanonical continuation state was emitted without authorization.

### Clean default control

- Strict score: **7/14 PASS**
- Deterministic onboarding was absent.
- Single-letter messages were treated as unexplained input.
- After the substantive project prompt, Grok created a careful design plan and preserved the missing-schema blocker.
- No code, tests, repository operations, or unsupported verification claims were produced.
- The handoff preserved state and denied authorization but was ad hoc.
- `air teleport` was not recognized, though no semantics were invented.

### Public-discovery exploratory condition

A separate retrieval-enabled Grok run discovered public AIR material through web search. It is retained as exploratory evidence but excluded from the clean default control.

Public discovery reproduced portions of AIR's evidence discipline but not the frozen v3 protocol. It also produced an unsupported canonical handoff representation, demonstrating that public reconstruction is not equivalent to a version-locked bundle.

## Cross-model decision

The standalone frozen session-entry bundle did not meet the original cross-model acceptance threshold because selector fidelity drifted on Grok.

This result is retained as portability evidence, but standalone cross-model boot is not the primary supported AIR usage path. The supported path is the main AIR system prompt together with the applicable specialist prompts or modules.

Standalone cross-model testing is therefore deferred and non-blocking for the stable version. The selector-fidelity defect remains a valid hardening item rather than a stable-release gate.

## Supported stability path

Stable-version work will prioritize:

- the main AIR system prompt;
- specialist prompt and module integration;
- deterministic behavior on the supported usage path;
- evidence and authorization discipline;
- handoff continuity;
- packaging and installed-runtime integrity;
- focused regression coverage;
- preparation for the modular implementation.

The Q2-Q6 selector lock remains deferred portability hardening. It may be implemented when standalone session-entry work resumes.

No broader architecture change is currently justified by the available evidence.

## Latency observation

The GPT-5.6 Sol High v3 AIR run completed materially faster than the earlier run, with no observed post-response thinking hang.

Reduced prompt ambiguity is a plausible contributor, but causal attribution is not established because platform conditions and session state also differed.

## Evidence boundary

This document summarizes observed test transcripts for the frozen v3 candidate. It does not establish model-wide performance, guarantee identical behavior across future sessions, or grant merge, release, tag, publication, or deployment authorization.

## Repository status

- PR remains draft.
- Merge remains blocked.
- No tag, release, package publication, or announcement is authorized.
- Work resumes with supported-path stability work and the modular implementation.
