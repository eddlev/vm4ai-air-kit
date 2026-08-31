<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=20260830-air250">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=20260830-air250" alt="AIR by VM4AI — Focused. Fluid. AIR. AI work, carried forward." width="100%">
  </picture>
</p>

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Foundation](https://img.shields.io/badge/foundation-2.5.0-C9A227?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)
[![Channel](https://img.shields.io/badge/channel-preview-FF5A1F?labelColor=1A1613)](RELEASE_CHANNEL_POLICY.md)

**AI work, carried forward.**

**Carry complex AI projects across sessions and compatible platforms without rebuilding the work every time.**

[Get started](https://vm4ai.com/get-started.html) · [How AIR works](https://vm4ai.com/how-it-works.html) · [Documentation](https://vm4ai.com/air-docs.html) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) · [Issues](https://github.com/eddlev/vm4ai-air-kit/issues)

AIR (**AI Resource**) is a prompt-based project runtime for sustained AI work. It keeps one material task active, makes the working contract explicit, surfaces evidence and approval boundaries, and carries recorded project state forward through Handoff.

AIR is not a hidden-memory system or backend enforcement layer. It is prompt-compiled and host-model governed. Compatibility depends on the host being able to load and sustain the AIR contract.

## Current public channel

**AIR v2.5.0-preview.1** is the current Preview / Development source line.

| Component | Current version |
| --- | ---: |
| Public channel | `v2.5.0-preview.1` |
| AIR Core Runtime | `2.5.0` |
| AIR Control Surface | `2.5.0` |
| AIR Governance Supplement | `2.3.0` |
| AIR Default Starter | `2.5.0` |
| AIR Handoff schema | `2.3.0` |
| Specialist package line | `2.4.0` |
| Runtime Route Map | `1.0.0` |
| Specialist Index | `1.1.1` |

The preview/stable distinction is intentional. Preview releases use static validation, change-sensitive regression checks, a small core behavioral smoke set, and field feedback. A stronger Stable designation is reserved for the broader repeated behavioral gate described in [RELEASE_CHANNEL_POLICY.md](RELEASE_CHANNEL_POLICY.md).

## Start in two minutes

Use the complete current five-file Foundation from [`prompts/`](prompts/):

1. `AIR_CORE_RUNTIME.md`
2. `AIR_CONTROL_SURFACE.md`
3. `AIR_GOV.md`
4. `AIR_DEFAULT_STARTER_PROFILE.json`
5. `AIR_HANDOFF_CARD_TEMPLATE.json`

Attach all five to a fresh compatible AI session and send:

```text
Start a new AIR project.
```

AIR validates the Foundation and starts onboarding at Q1. The activation phrase selects the fresh-start route but does **not** silently answer Q1.

See [`START_HERE.md`](START_HERE.md) for the shortest new-project, import, and Handoff paths.

## What v2.5.0-preview.1 changes

This preview closes the remaining AIR 2.5.0 Foundation-consistency defects found during integrated repair:

- strict-Handoff Governance metadata now aligns to Governance/Floor `2.3.0`;
- Handoff restoration uses the schema-2.3 evidence carriers `presentation_mode`, `presentation_mode_source`, and `evidence_capture_gaps`;
- evidence sufficiency is explicitly independent of standard vs expanded evidence presentation.

The Runtime Route Map and all four Specialist package dependency closures were resealed against the repaired Foundation hashes. Specialist package versions remain `2.4.0`.

## Validation boundary

For this preview, the repaired candidate completed:

- Foundation defects: **3/3 closed**
- canonical internal dependency edges: **28/28 PASS**
- focused Specialist validation: **185/185 PASS**
- integrated static validation: **895/895 PASS, 0 warnings**
- independent reproduction of the semantic file hash map and validation reports: **byte-identical**
- targeted isolated/field smoke: **BR-001, BR-004, BR-005, BR-006, BR-007 PASS**

The behavioral observations are `REPLAYABLE_EVALUATION` / field evidence, not deterministic model proof. This preview does **not** claim stable behavioral certification, universal model/provider/platform compatibility, backend enforcement, or guaranteed correctness. See [`VALIDATION_EVIDENCE_2.5.0-preview.1.md`](VALIDATION_EVIDENCE_2.5.0-preview.1.md).

## Continue a project

An `AIR_HANDOFF_CARD` carries recorded AIR project state into a new compatible session. The receiving runtime validates the card and current sources, performs a current-session restore evaluation, and rebinds the nominated artifact before material execution resumes.

State may travel; execution authority must be re-earned in the destination environment. Handoff does not claim transfer of hidden model state or byte-for-byte identical inference.

## Capability packages

Reusable non-agent capability packages live under [`profiles/`](profiles/):

- Grounding Specialist
- AI Governance Specialist
- Capability Ecology Architect
- Specification-First Verification Specialist

The current Specialist package line is **2.4.0**. Availability does not automatically create selection, approval, compilation, binding, or execution authority.

Discovery metadata is under [`catalog/`](catalog/):

- `AIR_RUNTIME_ROUTE_MAP.json`
- `AIR_SPECIALIST_PACKAGE_INDEX.json`

These are discovery/salience surfaces; operative authority remains with the validated Foundation and the bound Orbit 0 artifact.

## Evidence and assurance

AIR separates prompt-runtime records from evidence about the world outside the prompt runtime. A surfaced AIR record may prove what AIR declared; it does not by itself prove that a tool call happened, a deployment succeeded, a source is correct, or a backend enforced a gate.

Likewise:

- deterministic/static checks do not make LLM inference deterministic;
- successful model sessions do not prove static package integrity;
- human approval does not prove external events the reviewer did not observe.

See [`validation/`](validation/), [`tests/`](tests/), and the website's Testing & Evidence page for the evidence boundary.

## Compatibility

Compatibility is empirical and configuration-dependent. Provider/model versions, context budget, attachment handling, system instructions, available tools, and host behavior can all affect AIR.

See [`COMPATIBILITY.md`](COMPATIBILITY.md). A successful observation is evidence for the tested configuration, not vendor certification or a promise about every model/version.

## Repository map

```text
prompts/        canonical five-file AIR Foundation
catalog/        runtime route map + Specialist package index
profiles/       four Specialist package families
validation/     current T12D static + preview smoke evidence
tests/          public reproducibility harness
evals/          replayable empirical evaluation protocol
tools/          release and validation tooling
```

## Community and bugs

Use [GitHub Issues](https://github.com/eddlev/vm4ai-air-kit/issues) for reproducible AIR defects and [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) for questions, integrations, portability observations, design discussion, and feature ideas.

See [`BUG_REPORTING.md`](BUG_REPORTING.md) for the report format. Do not post exploitable security details publicly.

## License and brand

The project code and prompt materials are licensed under **Apache-2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE). AIR/VM4AI names and brand marks are separate from the code license; reusable brand assets live in [eddlev/air-brand](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.**
