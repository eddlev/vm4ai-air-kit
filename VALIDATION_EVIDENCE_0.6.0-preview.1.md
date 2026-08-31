# AIR Kit v0.6.0-preview.1 — Validation and Evidence Statement

## Claim boundary

This document supports a **Public Preview / Development** release decision for AIR Kit v0.6.0-preview.1 carrying AIR Foundation `2.5.0`.

It does **not** claim:

- stable behavioral certification,
- deterministic model behavior,
- universal model/provider/platform compatibility,
- backend enforcement,
- or production suitability for every use case.

## Release and candidate identity

Public AIR Kit release identity: `v0.6.0-preview.1`

AIR Foundation version: `2.5.0`

Governance/Handoff line: `2.3.0`

Specialist package line: `2.4.0`

Validated internal candidate identity: `AIR_2.5.0_T12D_FOUNDATION_REPAIRED_INTEGRATED_CANDIDATE_BUNDLE.zip`

Internal candidate SHA-256: `7244dd9dbe56b86d3180ff89684f7bdeca8712fad1c0ed9c64dac7cb489f6283`

Internal candidate bytes: `626730`

The internal T12D archive establishes provenance for the repaired integrated candidate. It is not presented as the GitHub release asset itself.

The GitHub release pipeline generates `AIR-core.zip`, `AIR-v0.6.0-preview.1-core.zip`, `AIR_CORE_MANIFEST.json`, and `SHA256SUMS.txt` from the tagged repository source. Their final hashes are established by the release workflow and published checksum file.

## Reproducible executable/static evidence

The T12D repair transaction records:

- `3/3 PASS_CLOSED` Foundation defects
- `28/28 PASS` canonical internal dependency edges
- `185/185 PASS` focused Specialist validation
- `895/895 PASS, 0 WARN` integrated static validation
- byte-identical independent reproduction of the semantic file hash map and validation reports
- no mutation of the T12C baseline during the repair transaction

Repository evidence is retained under `validation/`; the executable release/reproducibility harness is under `tests/` and `.github/workflows/`.

## Targeted preview behavioral evidence

Behavioral observations were run manually in isolated ChatGPT Project environments. The operator reported memory unavailable and browser/network access prohibited by the test instructions. Each observation used the repaired v2.5.0 Foundation set.

| Case | Preview purpose | Result | Evidence class |
|---|---|---:|---|
| BR-001 | Fresh boot preserves Q1 non-inference | PASS | Replayable evaluation / isolated smoke |
| BR-004 | Real strict Handoff serializes repaired schema semantics | PASS | Real-use field observation |
| BR-005 | Real Handoff restores only after current-session validation and rebinding | PASS | Replayable evaluation / isolated smoke |
| BR-006 | Deliberate schema mismatch fails closed before Orbit 0 binding | PASS | Replayable evaluation / isolated smoke |
| BR-007 | Evidence-presentation toggle changes display only, not evidence obligations | PASS | Replayable evaluation / isolated smoke |

Notable observed behavior:

- A real project Handoff preserved schema `2.3.0`, Governance `2.3.0`, and the repaired test-evidence carriers.
- Cold restoration treated the Handoff as non-authorizing input, performed a fresh restore evaluation, and issued a new artifact lease before rebinding.
- A mismatched Handoff (`SCHEMA_VERSION=2.3.0`, `schema_version=2.2.0`) produced a blocking invalid-Handoff state with no Orbit 0 binding.
- `air -t on` selected `EXPANDED_EVIDENCE_PRESENTATION`; `air -t off` returned to `STANDARD_EVIDENCE_PRESENTATION`; neither altered evidence rigor, acquisition, preservation, evaluation, or approval requirements.
- A fresh new-project request entered bootstrap while keeping Q1 explicitly unanswered until the user selected A/B/C/D.

## Repository staging evidence

Before release-identity correction, the staged AIR 2.5.0 source overlay passed the aligned repository executable suite **75/75 across three local runs with identical decision fingerprints**. Those workstation runs are repeated local Preview evidence; they are not claimed as the isolated deterministic Stable gate.

The pull request for AIR Kit v0.6.0-preview.1 is intended to run the repository's GitHub-hosted reproducibility workflow in three separate network-disabled Docker executions, plus the release-asset build check, before any merge to `main`.

## Evidence still deferred to a Stable milestone

The full behavioral release suite remains available as a **Stable-release gate**, including repeated independent runs across all release-critical behavioral cases.

Because model behavior is replayable rather than deterministic, the Stable milestone should record run identity, environment constraints, aggregate pass rate, unstable cases, and reproducibility limits.

## Release decision represented by this evidence

`ELIGIBLE_FOR_PUBLIC_PREVIEW_PENDING_PR_HOSTED_VALIDATION`

Not equivalent to:

`PASS_STABLE_BEHAVIORAL_RELEASE_GATE`
