<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=20260830-air250">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=20260830-air250" alt="AIR by VM4AI — Focused. Fluid. AIR. AI work, carried forward." width="100%">
  </picture>
</p>

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Foundation](https://img.shields.io/badge/foundation-2.5.0-C9A227?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)
![Channel](https://img.shields.io/badge/channel-release-56B581?labelColor=1A1613)

**AI work, carried forward.**

AIR (**AI Resource**) is a prompt-compiled project runtime for sustained AI work. It gives an AI session an explicit working contract, keeps one material task bound at a time, preserves approval and evidence boundaries, and carries recorded project state forward across sessions and compatible AI platforms through Handoff.

AIR is not hidden model memory and it is not a backend enforcement layer. Its runtime behavior is governed by the loaded AIR Foundation together with the host model, platform instructions, available context, and tools.

[Get started](https://vm4ai.com/get-started.html) · [How AIR works](https://vm4ai.com/how-it-works.html) · [Documentation](https://vm4ai.com/air-docs.html) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) · [Issues](https://github.com/eddlev/vm4ai-air-kit/issues)

## Current tagged release

**AIR Kit v0.6.0** is the current tagged public release and carries AIR Foundation **2.5.0**.

The `set004-target-readiness-step-optimality` branch is an **unreleased release candidate**. It keeps the component versions at AIR Foundation `2.5.0` / Specialist packages `2.4.0`, while resealing the coordinated object-contract identity as `AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004`.

| Component | Tagged v0.6.0 | Set-004 candidate |
| --- | ---: | ---: |
| AIR Kit | `0.6.0` | unreleased candidate |
| Core Runtime | `2.5.0` | `2.5.0` |
| Control Surface | `2.5.0` | `2.5.0` |
| Default Starter | `2.5.0` | `2.5.0` |
| Governance Supplement | `2.3.0` | `2.3.0` |
| Handoff schema | `2.3.0` | `2.3.0` rev15 |
| Specialist packages | `2.4.0` | `2.4.0` |
| Runtime Route Map | `1.0.0` | `1.0.1` |
| Specialist Package Index | `1.1.4` | `1.2.0` |

Release status does **not** claim universal behavioral certification across every provider/model, deterministic LLM behavior, universal host compatibility, or backend AIR enforcement. Behavioral compatibility remains empirical and configuration-dependent.

## Set-004 candidate changes

The set-004 candidate adds target-readiness and step-optimality semantics to AIR's completion architecture. In maturity-bearing work, current AMRS tells AIR where the work is while target AMRS helps define what eventual sufficiency must include. Stage completion requires both task-sufficiency and a bounded step-optimality pass under the active benchmark; this is not a claim of global optimization.

The candidate also:

1. carries Handoff schema `2.3.0` revision 15;
2. updates the Runtime Route Map to `1.0.1`;
3. reseals the four existing Specialist packages against the set-004 Foundation receipts;
4. adds the reusable **Public Surface Copywriting Specialist** package;
5. expands the Specialist Package Index to five packages at `1.2.0`.

## Start AIR

Attach all five files from [`prompts/`](prompts/) to a fresh compatible AI session:

1. `AIR_CORE_RUNTIME.md`
2. `AIR_CONTROL_SURFACE.md`
3. `AIR_GOV.md`
4. `AIR_DEFAULT_STARTER_PROFILE.json`
5. `AIR_HANDOFF_CARD_TEMPLATE.json`

Then send:

```text
Start a new AIR project.
```

AIR validates the loaded Foundation and starts the fresh-project onboarding route. The activation phrase selects the route; it does not silently answer onboarding questions for you.

### Continue an AIR project

Load the same current five-file Foundation together with the populated `AIR_HANDOFF_CARD` from the previous AIR session and choose the continuation route.

Handoff carries **recorded AIR project state**, not hidden model state or previously earned execution authority. The destination session validates the current Foundation and Handoff, evaluates the restored state in the new session, and rebinds the nominated artifact before material execution resumes.

### Import an existing non-AIR project

Load the current Foundation and choose the import route during onboarding. Supply the existing project material as source input. AIR reconstructs an explicit project contract from the material you provide rather than inventing prior AIR state.

## Public repository structure

```text
catalog/   discovery metadata for routes and Specialist packages
profiles/  optional reusable Specialist capability packages
prompts/   canonical five-file AIR Foundation
```

The public repository is intentionally small. Engineering validation reports, test harnesses, evaluation protocols, release-build tooling, and historical release-process material are not part of the public AIR runtime surface.

### `prompts/`

The canonical AIR Foundation. These five files are the complete normal boot set for AIR:

- `AIR_CORE_RUNTIME.md`
- `AIR_CONTROL_SURFACE.md`
- `AIR_GOV.md`
- `AIR_DEFAULT_STARTER_PROFILE.json`
- `AIR_HANDOFF_CARD_TEMPLATE.json`

### `catalog/`

Foundation-adjacent discovery metadata:

- `AIR_RUNTIME_ROUTE_MAP.json`
- `AIR_SPECIALIST_PACKAGE_INDEX.json`

The catalog improves route and Specialist discovery. It does not independently create semantic, selection, approval, binding, or execution authority. Core remains authoritative for runtime route semantics.

### `profiles/`

Optional reusable Specialist capability packages in the set-004 candidate:

- AI Governance Specialist
- Capability Ecology Architect
- Grounding Specialist
- Public Surface Copywriting Specialist
- Specification-First Verification Specialist

A package being present does not mean it is automatically selected or bound. AIR still evaluates package identity, Foundation compatibility, task fit, and any required approval before use.

## AIR's operating boundary

AIR separates the state and decisions represented inside the prompt runtime from claims about the world outside it.

A surfaced AIR record can establish what AIR declared, evaluated, approved, or bound in the session. It does not by itself prove that an external tool call succeeded, a deployment happened, a factual source is correct, or a backend enforced an AIR gate.

Likewise:

- deterministic or static file checks do not make model inference deterministic;
- a successful session does not prove universal model or platform compatibility;
- Handoff does not transfer hidden model state;
- human approval authorizes an AIR action boundary but does not prove an external effect that was not independently observed.

## Compatibility

Compatibility is empirical and configuration-dependent. Provider/model versions, context budget, attachment handling, system instructions, available tools, and host behavior can all affect AIR.

For implementation guidance, compatibility notes, testing methodology, and release information, use the [VM4AI documentation](https://vm4ai.com/air-docs.html) and GitHub Releases.

## Community and bugs

Use [GitHub Issues](https://github.com/eddlev/vm4ai-air-kit/issues) for reproducible AIR defects and [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) for questions, integrations, portability observations, design discussion, and feature ideas.

When reporting a behavioral issue, include the AIR Kit release or candidate identity, AIR Foundation version, model/provider, host/platform, reproduction sequence, expected behavior, observed behavior, and visible AIR output where possible.

Do not post exploitable security details publicly.

## License and brand

The project code and prompt materials are licensed under **Apache-2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

AIR/VM4AI names and brand marks are separate from the code license. Reusable brand assets live in [eddlev/air-brand](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.**
