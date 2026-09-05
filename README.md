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

## AIR Kit v0.7.1

**AIR Kit v0.7.1** is a patch hardening release over v0.7.0. It closes a prompt-runtime formal-object emission loophole, strengthens permanent release validation, normalizes reusable Method/Specialist contracts, and repairs stale package identity metadata without representing AIR as backend-enforced or deterministic.

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

Foundation identity for this candidate is `AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005`. Governance remains 2.3.0 because Core owns route, object-constructor, alignment, binding, action, and handoff-restoration semantics.

Release status does **not** claim universal behavioral certification across every provider/model, deterministic LLM behavior, universal host compatibility, or backend AIR enforcement. Static validation and replayable behavioral evaluation remain separate evidence classes.

## What's in v0.7.1

1. adds a Core-owned closed-world `RESPONSE_EMISSION_CLOSURE` so the alignment pair cannot satisfy a response while other route/lifecycle objects are silently dropped;
2. mirrors the closure in Control, Default Starter, and Runtime Route Map without creating a second semantic owner;
3. advances Handoff schema 2.3.0 to revision 16 and closes root-field/schema-manifest declaration coverage;
4. normalizes reusable Method Packs to Core's canonical `ordered_steps`, staleness, handoff, and binding carriers;
5. completes the Specification-First Verification Specialist's canonical Specialist profile surfaces;
6. strengthens Public Surface Copywriting with explicit required-input, knowledge-to-execution, MII, synthetic-benchmark, and observable anti-generic delta contracts;
7. repairs stale sibling/peer compatibility identities and removes construction-time peer manifest hash snapshots from operative runtime packages;
8. makes release publication state externally verified rather than a stale runtime-catalog assertion; and
9. adds a permanent deterministic release-contract validator plus replayable regression fixture definitions; and
10. moves operative five-file Foundation compatibility predicates into a typed deterministic contract registry with closed-world coverage accounting and per-check mutation tests, leaving prose validation expectations explicitly non-operative.

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
tools/     deterministic public release-contract validator
tests/     replayable regression fixture definitions
```

The public repository is intentionally small. It includes one deterministic release-contract validator and replayable regression fixture definitions so shipped runtime/package claims can be checked against the actual tree. Private evaluation logs, hidden model traces, and historical release-process material are not part of the public AIR runtime surface.

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

Optional reusable Specialist capability packages in AIR Kit v0.7.0:

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
