# AIR v2.5.0-preview.1 — Validation and Evidence Statement

## Claim boundary

This document supports a **Public Preview / Development** release decision for AIR v2.5.0-preview.1.

It does **not** claim:

- stable behavioral certification,
- deterministic model behavior,
- universal model/provider/platform compatibility,
- backend enforcement,
- or production suitability for every use case.

## Candidate identity

Public release filename: `AIR_v2.5.0-preview.1.zip`

Validated internal candidate identity: `AIR_2.5.0_T12D_FOUNDATION_REPAIRED_INTEGRATED_CANDIDATE_BUNDLE.zip`

SHA-256: `7244dd9dbe56b86d3180ff89684f7bdeca8712fad1c0ed9c64dac7cb489f6283`

Bytes: `626730`

The public-named archive is a byte-identical copy of the validated internal candidate.

## Reproducible executable/static evidence

The T12D repair transaction records:

- `3/3 PASS_CLOSED` Foundation defects
- `28/28 PASS` canonical internal dependency edges
- `185/185 PASS` focused Specialist validation
- `895/895 PASS, 0 WARN` integrated static validation
- byte-identical independent reproduction of the semantic file hash map and validation reports
- no mutation of the T12C baseline during the repair transaction

Evidence files are included under `evidence/`.

## Targeted preview behavioral evidence

Behavioral observations were run manually in isolated ChatGPT Project environments. The operator reported memory unavailable and browser/network access prohibited by the test instructions. Each observation used the repaired v2.5.0 Foundation set.

| Case | Preview purpose | Result | Evidence class |
|---|---|---:|---|
| BR-001 | Fresh boot preserves Q1 non-inference | PASS | Replayable evaluation / isolated smoke |
| BR-004 | Real strict handoff serializes repaired schema semantics | PASS | Real-use field observation |
| BR-005 | Real handoff restores only after current-session validation and rebinding | PASS | Replayable evaluation / isolated smoke |
| BR-006 | Deliberate schema mismatch fails closed before Orbit 0 binding | PASS | Replayable evaluation / isolated smoke |
| BR-007 | Evidence-presentation toggle changes display only, not evidence obligations | PASS | Replayable evaluation / isolated smoke |

Notable observed behavior:

- A real project handoff preserved schema `2.3.0`, Governance `2.3.0`, and the repaired test-evidence carriers.
- Cold restoration treated the handoff as non-authorizing input, performed a fresh restore evaluation, and issued a new artifact lease before rebinding.
- A mismatched handoff (`SCHEMA_VERSION=2.3.0`, `schema_version=2.2.0`) produced a blocking invalid-handoff state with no Orbit 0 binding.
- `air -t on` selected `EXPANDED_EVIDENCE_PRESENTATION`; `air -t off` returned to `STANDARD_EVIDENCE_PRESENTATION`; neither altered evidence rigor, acquisition, preservation, evaluation, or approval requirements.
- A fresh new-project request entered bootstrap while keeping Q1 explicitly unanswered until the user selected A/B/C/D.

## Evidence still deferred to a stable milestone

The full behavioral release suite remains available as a **stable-release gate**, including repeated independent runs across all release-critical behavioral cases.

Because model behavior is replayable rather than deterministic, the stable milestone should record run identity, environment constraints, aggregate pass rate, unstable cases, and reproducibility limits.

## Release decision represented by this evidence

`ELIGIBLE_FOR_PUBLIC_PREVIEW`

Not equivalent to:

`PASS_STABLE_BEHAVIORAL_RELEASE_GATE`
