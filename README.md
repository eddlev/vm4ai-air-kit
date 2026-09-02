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

## Current release

**AIR Kit v0.6.0** carries the repaired and coordinated AIR Foundation **2.5.0** release set.

| Component | Version |
| --- | ---: |
| AIR Kit | `0.6.0` |
| Core Runtime | `2.5.0` |
| Control Surface | `2.5.0` |
| Default Starter | `2.5.0` |
| Governance Supplement | `2.3.0` |
| Handoff schema | `2.3.0` |
| Specialist packages | `2.4.0` |
| Runtime Route Map | `1.0.0` |
| Specialist Package Index | `1.1.3` |

Release status means the public AIR Kit distribution is internally coherent and release-sealed. It does **not** claim universal behavioral certification across every provider/model, deterministic LLM behavior, universal host compatibility, or backend AIR enforcement. Behavioral compatibility remains empirical and configuration-dependent.

## What changed in AIR Foundation 2.5.0

AIR 2.5.0 is a Foundation-consistency release focused on making continuation, evidence state, object ownership, and downstream package identity agree across the runtime.

The repaired Foundation closes the consistency defects identified during integrated validation, including:

1. **Handoff Governance alignment** — strict Handoff state aligns with Governance/Floor version `2.3.0`.
2. **Handoff restoration schema alignment** — Core restoration semantics use the schema-2.3 carriers `presentation_mode`, `presentation_mode_source`, and `evidence_capture_gaps`.
3. **Evidence-presentation semantics** — evidence sufficiency is explicitly independent of whether evidence presentation is standard or expanded.
4. **Canonical object-contract alignment** — Core and Starter consistently reference `AIR_CANONICAL_OBJECT_CONTRACTS_V4`.
5. **Handoff rev14 ownership alignment** — the active Handoff compatibility contract and Governance approval-scope carrier follow the rev14 single-owner transfer model.
6. **Atomic task-switch surface alignment** — Control mirrors Core's rule that a still-valid Orbit 0 artifact is demoted only inside the binding transaction after the replacement is bind-ready.

The Runtime Route Map and all four released Specialist packages were resealed against the repaired Foundation identity. Specialist package versions remain `2.4.0`; the Specialist Package Index is `1.1.3`.

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

Optional reusable Specialist capability packages:

- Capability Ecology Architect
- AI Governance Specialist
- Grounding Specialist
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

When reporting a behavioral issue, include the AIR Kit release, AIR Foundation version, model/provider, host/platform, reproduction sequence, expected behavior, observed behavior, and visible AIR output where possible.

Do not post exploitable security details publicly.

## License and brand

The project code and prompt materials are licensed under **Apache-2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

AIR/VM4AI names and brand marks are separate from the code license. Reusable brand assets live in [eddlev/air-brand](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.**
