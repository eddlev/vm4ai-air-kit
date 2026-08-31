# AIR v2.5.0-preview.1

**Release channel:** Public Preview / Development

AIR v2.5.0-preview.1 is a preview release of the repaired AIR 2.5.0 candidate. It is intended for active use, field testing, integration experiments, and rapid feedback while AIR continues to evolve.

This release is **not labeled as a stable behavioral certification**. The full release-grade behavioral matrix is reserved for a later stable milestone so that fast-moving development is not blocked by repeatedly invalidated long-form manual test cycles.

## What changed

This preview closes three Foundation consistency defects identified after the prior specialist-layer closure:

1. **Handoff Governance version drift** — strict handoff state now aligns with Governance/Floor version `2.3.0`.
2. **Handoff restoration schema drift** — Core restoration semantics now use the schema-2.3 carriers `presentation_mode`, `presentation_mode_source`, and `evidence_capture_gaps`.
3. **Evidence-presentation semantic contradiction** — evidence sufficiency is now explicitly independent of whether presentation is standard or expanded.

The Runtime Route Map and downstream Specialist dependency closure were resealed against the repaired Foundation hashes. Specialist package versions remain `2.4.0`; the Specialist Index remains `1.1.1`.

## Validation completed

### Static validation

- Foundation defects: **3/3 closed**
- Canonical internal dependency edges: **28/28 PASS**
- Focused Specialist validation: **185/185 PASS**
- Integrated static validation: **895/895 PASS, 0 warnings**
- Independent reproduction: semantic hash map and validation reports reproduced byte-identically
- Original T12C baseline remained unchanged

### Targeted isolated behavioral smoke

The preview candidate was also exercised manually in isolated ChatGPT Project sessions with memory unavailable and browser/network access prohibited by the test instructions.

The targeted preview smoke covered:

- **BR-001** — fresh AIR boot and Q1 non-inference: **PASS**
- **BR-004** — real strict handoff creation from an active AIR project: **PASS**
- **BR-005** — cold restore/revalidation/rebinding from that real handoff: **PASS**
- **BR-006** — deliberately mismatched handoff schema fails closed: **PASS**
- **BR-007** — evidence-presentation state plus `air -t on/off` semantics: **PASS**

These are **replayable model observations**, not deterministic executable proof. They support the preview release decision but do not replace the fuller stable-release behavioral gate.

## Release artifact

Primary archive:

`AIR_v2.5.0-preview.1.zip`

SHA-256:

`7244dd9dbe56b86d3180ff89684f7bdeca8712fad1c0ed9c64dac7cb489f6283`

The archive bytes are identical to the internally validated T12D corrected integrated candidate; only the external release filename is changed.

## Known boundaries

- AIR remains a **prompt-compiled runtime**; no backend AIR enforcement is claimed.
- Universal cross-model/cross-host behavioral parity is not yet established.
- Specialist behavioral coverage remains broader than the targeted preview smoke.
- Preview users should treat named platform/model compatibility as empirical rather than guaranteed.
- Security-sensitive findings should not be posted publicly with exploitable details; use the repository's private security reporting path where available.

## Feedback

This preview intentionally uses real-world field feedback as part of AIR's development loop. Please report reproducible bugs through GitHub Issues and use GitHub Discussions for questions, design discussion, integration experiences, and feature ideas.

When reporting a behavioral issue, include the AIR release, model/provider, host/platform, exact prompt or reproduction sequence, expected behavior, observed behavior, and visible AIR output when possible.
