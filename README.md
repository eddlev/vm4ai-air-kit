<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=20260830-air250">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=20260830-air250" alt="AIR by VM4AI — Focused. Fluid. AIR. AI work, carried forward." width="100%">
  </picture>
</p>

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Foundation](https://img.shields.io/badge/foundation-2.6.0-C9A227?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)
![Channel](https://img.shields.io/badge/channel-release-56B581?labelColor=1A1613)

**AI work, carried forward.**

AIR (**AI Resource**) is a prompt-compiled project runtime for sustained AI work. It gives an AI session an explicit working contract, keeps one material task bound at a time, preserves approval and evidence boundaries, and carries recorded project state forward across sessions and compatible AI platforms through Handoff.

AIR is not hidden model memory and it is not a backend enforcement layer. Its runtime behavior is governed by the loaded AIR Foundation together with the host model, platform instructions, available context, and tools.

[Get started](https://vm4ai.com/get-started.html) · [How AIR works](https://vm4ai.com/how-it-works.html) · [Documentation](https://vm4ai.com/air-docs.html) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) · [Issues](https://github.com/eddlev/vm4ai-air-kit/issues)

## AIR Kit v0.7.1

**AIR Kit v0.7.1** is a patch-hardening release over v0.7.0. It carries AIR Foundation **2.6.0**, Handoff schema **2.3.0 revision 16**, Specialist packages **2.5.0**, and the coordinated Foundation identity `AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005`.

The v0.7.1 hardening pass closes **74 audited source findings** across the Foundation, Handoff, runtime catalogs, Specialist packages, package construction paths, lifecycle metadata, validation contracts, and release tooling. The release preserves AIR's prompt-runtime authority boundary: no package, catalog, Handoff record, or deterministic validator becomes backend execution authority.

| Component | v0.7.0 | v0.7.1 |
| --- | ---: | ---: |
| AIR Kit | `0.7.0` | `0.7.1` |
| Core Runtime | `2.5.0` | `2.6.0` |
| Control Surface | `2.5.0` | `2.6.0` |
| Default Starter | `2.5.0` | `2.6.0` |
| Governance Supplement | `2.3.0` | `2.3.0` |
| Handoff schema | `2.3.0` rev15 | `2.3.0` rev16 |
| Specialist packages | `2.4.0` | `2.5.0` |
| Runtime Route Map | `1.0.1` | `1.1.0` |
| Specialist Package Index | `1.2.0` | `1.3.0` |

Foundation identity for this release is `AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005`. Governance remains 2.3.0 because Core owns route, object-constructor, alignment, binding, action, and Handoff-restoration semantics.

Release status does **not** claim universal behavioral certification across every provider/model, deterministic LLM behavior, universal host compatibility, or backend AIR enforcement. Deterministic/static checks and model/host behavior remain distinct evidence classes. Release acceptance for v0.7.1 is based on the completed audit/remediation suite together with maintainer acceptance through active AIR use.

## What's in v0.7.1

The v0.7.1 remediation was completed in eight bounded repair phases:

1. **Foundation deterministic spine** — repairs route delimiters, control-event binding, deterministic-route membership, boot/version checks, alignment reachability, registry coverage, Route Map anchors, and route prerequisites.
2. **Formal objects and authorization** — closes the formal-object registry, normalizes Gate and Authorization semantics, registers Artifact fields correctly, and gives failure records a deterministic ledger-backed construction path.
3. **Handoff and restoration** — validates exact approval-token derivation, adds executable rev15→rev16 migration before required-carrier validation, preserves visibility/profile authority provenance, fixes conditional predicates, and supplies typed Method-Pack restoration contracts.
4. **Shared package schema normalization** — normalizes MII morphology carriers, Executor interfaces, Method interfaces, Specialist surfaces, and Session Domain Overlay representation without expanding package authority.
5. **Capability Ecology constructor chain** — makes the canonical 44-field Domain Package contract consistent across fixtures, Translator output, Architect construction, negative mutations, and typed evidence-waiver handling.
6. **Package-local behavioral contracts** — makes Governance input acquisition conditional on actual gaps and gives Public Surface Copywriting an explicit proportional stopping/step-optimality loop.
7. **Lifecycle, version, history, and reseal truth** — aligns current Foundation identities, package readiness mirrors, candidate/release lifecycle vocabulary, historical records, component receipts, and dependency-graph resealing.
8. **Presentation and portability cleanup** — restores canonical sentinel references and boot-mark ownership, exposes all four system modifiers, pins NFKC filename normalization, and hardens unknown-target/reserved-name portability behavior.

The repository also carries permanent deterministic validation, mutation/meta tests, behavioral transaction contract checks, release-contract validation, and dependency-graph reseal verification so the shipped source can be checked against its declared contracts.

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
tools/     deterministic validators, remediation/reseal tooling, and regression runners
tests/     replayable contract, mutation, and regression fixtures
```

The public repository contains the deterministic validation and regression material needed to check the shipped AIR contracts against the actual tree. Private evaluation logs, hidden model traces, and historical working/audit artifacts are not part of the public AIR runtime surface.

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

Optional reusable Specialist capability packages in AIR Kit v0.7.1:

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

When reporting a behavioral issue, include the AIR Kit release, AIR Foundation version, model/provider, host/platform, reproduction sequence, expected behavior, observed behavior, and visible AIR output where possible.

Do not post exploitable security details publicly.

## License and brand

The project code and prompt materials are licensed under **Apache-2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

AIR/VM4AI names and brand marks are separate from the code license. Reusable brand assets live in [eddlev/air-brand](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.**
