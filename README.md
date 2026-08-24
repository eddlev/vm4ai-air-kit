<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=20260824-r4">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=20260824-r4" alt="AIR by VM4AI — Focused. Fluid. AIR. AI work, carried forward." width="100%">
  </picture>
</p>

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Foundation](https://img.shields.io/badge/foundation-2.4.3-C9A227?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)
[![Latest release](https://img.shields.io/github/v/release/eddlev/vm4ai-air-kit?label=release&labelColor=1A1613&color=FF5A1F)](https://github.com/eddlev/vm4ai-air-kit/releases)

**AI work, carried forward.**

**Carry complex AI projects across sessions and platforms without rebuilding the work every time.**

**[Download AIR](https://github.com/eddlev/vm4ai-air-kit/releases/latest/download/AIR-core.zip)** · [Get started](https://vm4ai.com/get-started.html) · [See how it works](https://vm4ai.com/how-it-works.html) · [Documentation](https://vm4ai.com/air-docs.html) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions)

AIR (**AI Resource**) is a prompt-based project runtime for sustained AI work. It keeps one material task active, makes the working contract explicit, surfaces evidence and approval boundaries, and carries recorded project state forward through Handoff.

It is not a replacement chat app, hidden memory system, or autonomous agent layer. The project state is meant to travel with the work instead of being trapped inside one session or provider.

---

## The idea in 30 seconds

| Focused | Fluid | AIR |
| --- | --- | --- |
| One material task stays active. | Continue from structured project state instead of reconstructing it. | Carry the project across sessions and compatible platforms. |

```text
Session A
  scope -> work -> decisions -> evidence -> approval state
                                      |
                                 Handoff Card
                                      |
                                      v
Session B / another compatible platform
  validate -> rebind -> continue from the recorded project state
```

AIR does not copy a transcript and call it memory. It makes the current working state explicit enough to validate, hand off, and continue.

## Start in two minutes

### Fastest route

1. **[Download `AIR-core.zip`](https://github.com/eddlev/vm4ai-air-kit/releases/latest/download/AIR-core.zip)** from the latest release.
2. Extract it.
3. Attach the five AIR foundation files to a capable AI session.
4. Send:

```text
Start a new AIR project.
```

AIR validates the supplied foundation and starts onboarding at Q1. The activation phrase does **not** silently answer Q1.

If the latest published release does not yet expose `AIR-core.zip`, use the five current files directly from [`prompts/`](prompts/) instead. [`START_HERE.md`](START_HERE.md) gives the short new-project, import, and Handoff paths.

> If AIR saves you from rebuilding a project, **star this repository** so other people can find it.

## Why use AIR?

AIR is useful when the cost of losing project state is higher than the cost of a little structure.

- **Keep one active task centered.** Orbit 0 holds the current executing task and its bound artifact.
- **Stop silent reconstruction.** Decisions, constraints, evidence, approvals, blockers, and next state stay explicit.
- **Bind how you and the AI work together.** Onboarding includes delivery, ambiguity, continuity, and working-agreement choices rather than leaving them to model habit.
- **Carry the project forward.** Handoff serializes recorded AIR state for validation and rebinding in another session.
- **Use capability without transferring authority.** Specialists, domain packages, methods, and executors can shape the task while the bound AIR artifact remains the execution authority.
- **Keep claims proportional to evidence.** AIR distinguishes prompt-layer records from external proof such as tests, repository state, deployments, sources, or operator actions.

For practical onboarding patterns—including Q5 and Q6 working-contract examples for code, research, writing, creative, brand, and strategy—see [Use cases](https://vm4ai.com/use-cases.html).

## Continue a project

An `AIR_HANDOFF_CARD` carries recorded AIR project state into a new compatible session. The receiving runtime validates and rebinds that state before execution resumes.

Load the current foundation together with the populated Handoff Card and choose the continuation route. Handoff preserves explicit transfer state; it does not promise hidden-state transfer or byte-for-byte identical inference.

## Current release and foundation

**Versioning:** AIR Kit releases use the public `v0.x` release line. The bundled runtime components keep their own component versions. **AIR Kit v0.5.0** packages Core/Control/Starter `2.4.3`, Governance/Handoff `2.2.0`, and the current specialist package line `2.3.6`.

| Component | Current version |
| --- | ---: |
| AIR Kit release | 0.5.0 |
| AIR Core Runtime | 2.4.3 |
| AIR Control Surface | 2.4.3 |
| AIR Governance Supplement | 2.2.0 |
| AIR Default Starter | 2.4.3 |
| AIR Handoff schema | 2.2.0 |

The five files under [`prompts/`](prompts/) are the boot foundation:

1. [`AIR_CORE_RUNTIME.md`](prompts/AIR_CORE_RUNTIME.md)
2. [`AIR_CONTROL_SURFACE.md`](prompts/AIR_CONTROL_SURFACE.md)
3. [`AIR_GOV.md`](prompts/AIR_GOV.md)
4. [`AIR_DEFAULT_STARTER_PROFILE.json`](prompts/AIR_DEFAULT_STARTER_PROFILE.json)
5. [`AIR_HANDOFF_CARD_TEMPLATE.json`](prompts/AIR_HANDOFF_CARD_TEMPLATE.json)

The complete required files must fit in the host interface without truncation. AIR does not claim one universal context-window threshold because attachment handling and tokenization vary by provider and model.

## Capability packages

Reusable non-agent capability packages live under [`profiles/`](profiles/). They are **available but unbound** until selected, compatibility-validated, approved when required, and compiled into the bound Orbit 0 artifact.

Current package families include:

- **Grounding Specialist**
- **AI Governance Specialist**
- **Capability Ecology Architect**
- **Specification-First Verification Specialist** — complete package, current package version **2.3.6**, including domain, method, specialist, executor, and package manifest components

Capability does not inherit project authority merely because it is loaded.

## Compatibility

AIR is prompt-based, so compatibility depends on the host being able to load the full foundation and follow the required instruction, object, and continuity discipline.

See [`COMPATIBILITY.md`](COMPATIBILITY.md) for the current maintainer-observed matrix, limitations, and a field-report format. Compatibility observations are not vendor certification or a guarantee that every model/version on a platform will behave identically.

## Assurance boundary

The public AIR Kit is prompt-based cooperative behavioral governance. It can materially shape how a host model frames, executes, reviews, and hands off work, but the prompt-only kit does not independently provide:

- deterministic backend or hook-level enforcement
- guaranteed tool execution
- tamper-evident or signed receipts
- hidden chain-of-thought or latent-state telemetry
- guaranteed correctness
- legal, regulatory, security, or production certification

When a claim depends on something outside the prompt runtime—tests, repository state, deployment state, a source, an operator action, a tool call, or a backend event—the matching external evidence is required.

## Test evidence and reproducibility

AIR separates the request to surface evidence from independent proof that an executable check was reproducible.

The repository's permanent reproducibility workflow executes the release manifest three times in separate network-disabled Docker containers and compares the resulting decision fingerprints. A bare statement such as `150/150 tests passed` is not enough to establish deterministic release evidence.

See [`tests/README.md`](tests/README.md) for the evidence contract and local commands.

The release asset pipeline is separate: [`tools/build_release_bundle.py`](tools/build_release_bundle.py) builds a deterministic `AIR-core.zip`, a Kit-versioned copy, a machine-readable file manifest, and SHA-256 checksums from the exact repository foundation. Pull requests verify that the bundle can be built before release publication.

## Canonical prompt-side controls

```text
air -o on
air -o -min
air -t on
air -t off
```

AIR defaults to `ALL_OBJECTS`. These controls change prompt-side visibility/evidence presentation; they do not bypass scope, approval, evidence, or release gates.

## Repository map

```text
prompts/                         current five-file AIR foundation
profiles/
  grounding specialist/
  governance specialist/
  capability ecology architect/
  specification first verification specialist/
tests/                           executable reproducibility harness
tools/build_release_bundle.py    deterministic release bundle builder
START_HERE.md                    shortest path from download to first AIR project
COMPATIBILITY.md                 maintainer-observed host compatibility notes
VERSION                          public AIR Kit release version
RELEASE_NOTES_0.5.0.md           release notes for AIR Kit v0.5.0
.github/workflows/               reproducibility + release-asset verification
```

## Community

Questions, field reports, implementation patterns, Q6 working contracts, compatibility results, and project showcases belong in [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions).

If you find a concrete defect in AIR itself, open an issue with the smallest reproducible example and the AIR version you used.

## License and brand

The project code and prompt materials are licensed under **Apache-2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

The AIR/VM4AI names and brand marks are separate from the code license. Reusable logos, visualizations, design tokens, and the “Made with AIR” mark live in the [AIR brand repository](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.** See [vm4ai.com](https://vm4ai.com/) for the product story, examples, and current public documentation.
