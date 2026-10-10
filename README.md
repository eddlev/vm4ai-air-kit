<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=20260830-air250">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=20260830-air250" alt="AIR by VM4AI — Focused. Fluid. AIR. AI work, carried forward." width="100%">
  </picture>
</p>

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![AIR Kit](https://img.shields.io/badge/AIR%20Kit-0.8.1--candidate-C9A227?labelColor=1A1613)](VERSION)
[![Core](https://img.shields.io/badge/Core-2.9.0-C9A227?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)

**AI work, carried forward.**

AIR (**AI Resource**) is a prompt-based framework for sustained work with AI.

Instead of treating every chat as an isolated conversation, AIR gives the AI an explicit project structure: what you are trying to accomplish, what is active now, what evidence matters, what requires your approval, and what needs to carry forward.

You talk to AIR normally. AIR handles the structure.

AIR is not a separate application or service stack. Its baseline runtime needs a compatible AI platform and the AIR client files. Additional tools, sources, services or specialist capabilities are determined by the work you ask AIR to do.

[Get started](https://vm4ai.com/get-started.html) · [How AIR works](https://vm4ai.com/how-it-works.html) · [Documentation](https://vm4ai.com/air-docs.html) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) · [Issues](https://github.com/eddlev/vm4ai-air-kit/issues)

## Why AIR?

Long or complex AI work tends to drift.

Goals change inside long conversations. Earlier decisions become difficult to find. Assumptions can quietly turn into facts. A new session may need to reconstruct the project before useful work can continue.

AIR adds a visible working frame around that process.

It helps AI and humans:

- keep one material task clearly active at a time;
- preserve project purpose, scope, constraints and decisions;
- distinguish assumptions, sources and evidence;
- surface blockers instead of silently working around them;
- require explicit human approval for material actions when appropriate;
- carry recorded project state between sessions and compatible AI platforms;
- add focused Specialist capabilities when a task needs them.

## Current version — AIR Kit v0.8.1 release candidate

This repository carries the **AIR Kit v0.8.1 release candidate** (`R23-AMRS6-V0.8.1-R133-CANDIDATE-R3`). The latest published release remains [AIR Kit v0.8.0](https://github.com/eddlev/vm4ai-air-kit/releases/tag/v0.8.0); v0.8.1 becomes a release only after its acceptance checks pass and it is promoted.

v0.8.1 builds on the AMRS-6 R23 runtime promoted in v0.8.0 and:

- aligns this repository with that runtime — the compiled client runtime, canonical source, law-source package and Specialist distributions now live here, replacing the v0.7.4-era files;
- makes the five supported boot commands and the Tier0–Tier3 boot profiles explicit, with an exact-section retrieval guard for routine boots;
- reconciles the current Handoff metadata to template revision 26;
- binds 25 deterministic checks to exact SHA-pinned law-source bodies instead of the Core prompt;
- adds a **first-activation emission latch**: after the final onboarding answer, AIR must activate through `RT.ACTIVATE` and visibly emit its five first-activation records before starting any project work;
- replaces the v0.7.4 release seal in CI with a v0.8.1 source-and-runtime integrity contract.

It includes:

- AIR Core Runtime **2.9.0**
- AIR Control Surface **2.7.0**
- AIR Governance Supplement **2.4.0**
- Default Starter **2.7.0**
- Handoff schema **2.3.0**, template revision **26**
- Runtime Route Map **1.2.5**
- Specialist Package Index **1.3.15**
- **83** stable law identities, **28** floor invariants, **137** deterministic checks and **19** direct runtime-reference anchors
- the full five-Specialist client distribution

**Acceptance status.** The candidate passes static deterministic release closure. Fresh-session Tier3 audit, first-activation (Q6/Q6D → `RT.ACTIVATE`) behavioral acceptance and boot-performance acceptance have **not yet been run** for this candidate, so it is not promoted.

See [v0.8.1 release-candidate notes](RELEASE_NOTES_V0_8_1.md), [AMRS-6 patch notes](RELEASE_NOTES_AMRS6_R23.md) and [Contributors](CONTRIBUTORS.md).

### Best practices

**Cognitive scope authority isolation.** AIR keeps adaptive reasoning inside the current task Artifact's declared cognitive scope. Cognitive findings are candidate contributions, not control state: they cannot directly change task/Artifact identity, deterministic routing, approval, Gate/Authorization/Receipt state, lease/scope pin, Handoff authority, or failure-registry authority. A contribution becomes operative only after the declared validation and ingestion boundary accepts it. This is an authority boundary, not a request for or exposure of private chain of thought.

**Thinking Effort.** AIR does not currently require a specific ChatGPT Thinking Effort setting. For day-to-day AIR use, **High** is a reasonable starting point. **Extra High** may be useful for unusually difficult analysis or architecture work, but there is not currently evidence that Thinking Effort causes or prevents AIR runtime drift. Treat cross-effort observations as empirical host-behavior evidence, not AIR execution authority.

**Known ChatGPT presentation issue.** AIR formal records have occasionally been observed inside ChatGPT's collapsed **`Worked for ...`** section rather than in the main response. Expanding that section reveals the records. This has so far only been observed on ChatGPT; the cause has not been isolated between AIR response-surface behavior and host UI routing. AIR formal records are structured governance records, not hidden reasoning or chain of thought. If expected records appear missing in ChatGPT, check that section and include the behavior in any bug report.

## Start AIR

AIR v0.8.x runs from the complete **AIR-P client**. The client ZIP attached to each AIR Kit release from v0.8.0 onward is the supported way to load it. The repository carries the same runtime files in these directories, without the ZIP's boot manifest and release profile:

```text
prompts/       the five AIR Foundation files
catalog/       route, law-applicability and Specialist discovery catalogs
air_p/         the compiled AIR-P client runtime and law-source package
specialists/   the five Specialist packages
evidence/      Specialist validation evidence
```

Then send:

```text
Start a new AIR-P project.
```

That default command resolves to **Tier0 routine boot**, the normal starting point. You can also request a boot profile explicitly:

```text
Start a new AIR-P project. Tier0 boot.
Start a new AIR-P project. Tier1 boot.
Start a new AIR-P project. Tier2 boot.
Start a new AIR-P project. Tier3 boot.
```

- **Tier0** — routine boot; retrieves only the minimum dependency closure needed to reach the first onboarding question (Q1).
- **Tier1** — adds compact navigation/index material.
- **Tier2** — retrieves exact authoritative source for an explicit target. If no target is available, AIR asks for the smallest missing target instead of widening retrieval.
- **Tier3** — full release-integrity/deep-audit path.

Selecting the new-project entry path does **not** answer Q1. AIR still surfaces Q1 and waits for an allowed onboarding answer.

Tier0, Tier1 and Tier2 use a closed retrieval plan. Exact section or JSON-subtree boundaries are hard limits for model-visible reads; adjacent context returned outside those boundaries is discarded before ingestion, and if exact filtering cannot be established the profile fails closed rather than silently widening retrieval.

When onboarding completes, AIR activates the project and shows five first-activation records — `AIR_RUNTIME_BRIDGE`, `AIR_SESSION`, `AIR_PROJECT_INITIALIZATION_BRIEF`, `AIR_PROJECT_EXECUTION_MAP` and `AIR_ARTIFACT` — before any project work begins. Minimum display mode (`air -o -min`) does not hide them.

No special command syntax or prior AIR knowledge is required for normal project conversation.

## Human approval and material actions

AIR separates conversational agreement from material authorization.

When a material action requires your approval—such as binding a capability or changing an external resource—AIR opens a specific approval scope and provides exact response tokens:

```text
AIR_APPROVE::<approval-scope>
AIR_REJECT::<approval-scope>
```

The exact approval token authorizes only the scope AIR described. A version suffix such as `_V1` is optional; AIR must issue a new distinct scope ID if the material scope changes, so old tokens cannot silently authorize a different action.

A casual response such as “looks good” or “go ahead” does not silently become material authorization when exact approval is required.

Approval and execution are also separate: approving an action does not prove that the action succeeded. AIR records and evaluates the resulting effect separately.

This keeps **direction**, **approval**, and **execution evidence** distinct.

## Continue or import a project

### Continue with Handoff

AIR uses a Handoff Card (schema 2.3.0, template revision 26) to carry recorded project state into another session or compatible platform.

Load the current AIR client with the populated `AIR_HANDOFF_CARD.json` and choose the continuation route during onboarding.

Handoff can preserve project scope, the active task, decisions, blockers, working agreements, Specialist state and approval boundaries.

It transfers **recorded AIR state**. It does not transfer hidden model memory, hidden reasoning or previously granted execution authority. The receiving session validates and rebinds the project before material execution resumes.

Strict Handoff requires qualifying durable provenance to have been available while the relevant AIR history was created. Adding a durable provider later cannot reconstruct missing strict provenance. When strict provenance is unavailable or incomplete, AIR can use `PORTABLE_STATE` if the current continuation state is otherwise valid.

A Handoff file-delivery receipt proves the delivered file's observed transport and integrity state only. It carries no execution authority and cannot authorize, bind, approve, or restore authority in the receiving session.

### Import existing work

AIR can also structure a project that did not begin in AIR.

Start AIR, choose the import route, and provide the existing project material. AIR builds an explicit project frame from the sources you provide rather than pretending previous AIR state existed.

## Specialists

AIR Kit includes optional Specialist packages for work that benefits from more focused capability or review:

- AI Governance Specialist
- Capability Ecology Architect
- Grounding Specialist
- Public Surface Copywriting Specialist
- Specification-First Verification Specialist

Specialists are not autonomous agents.

A Specialist being present in the repository does not make it active. AIR evaluates task fit, validates the package, obtains any required approval, and binds the relevant capability to the active task.

## AIR's operating boundary

AIR operates at the prompt/project-runtime layer.

It can structure work, surface project state, preserve boundaries, manage approval flow, request evidence and carry recorded project context forward.

It does **not** by itself prove that:

- an external tool action succeeded;
- an external source is correct;
- a backend enforced an AIR rule;
- model inference is deterministic;
- every AI model or platform behaves identically;
- hidden model state moved between sessions.

Those claims require their own evidence.

Compatibility is therefore empirical and configuration-dependent. Model/provider versions, context limits, attachment handling, available tools and platform behavior can affect AIR.

## Repository structure

```text
prompts/       the five AIR Foundation files
catalog/       route, law-applicability and Specialist discovery catalogs
air_p/         checked-in, non-executable compiled client runtime
specialists/   the five Specialist package distributions
evidence/      retained Specialist validation evidence
source/        canonical source: prompts, catalogs, law-source bodies, compiler and compiler tests
release/       current source, client-runtime and Specialist manifests, plus source deltas
tools/         current v0.8.1 validation plus retained historical release tooling
tests/         retained historical validation evidence and fixtures
```

The `profiles/` layout used through v0.8.0 is superseded by `specialists/`.

## Validation

CI runs `python3 tools/validate_air_suite.py`, which enforces the v0.8.1 repository contract. It:

- verifies the canonical 126-file source tuple and its exact manifest closure;
- runs the canonical compiler tests and performs three compiler builds, which must be byte-identical;
- compares the checked-in `air_p/` runtime against the generated build;
- verifies the Specialist carry-forward baseline, the 25 pinned law-source bindings and the first-activation latch anchors;
- runs mutation tests against the repository contract.

Historical v0.7.x validators remain in `tools/` as repository history only and are not current release authority.

## Community and bugs

Use [GitHub Issues](https://github.com/eddlev/vm4ai-air-kit/issues) for reproducible defects.

Use [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) for questions, integrations, portability observations, design discussion and feature ideas.

When reporting behavioral issues, include the AIR Kit release, AIR Foundation version, AI model/provider, platform, reproduction steps, expected behavior and observed behavior where possible.

## License and brand

AIR's code and prompt materials are licensed under **Apache-2.0**. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

AIR and VM4AI names and brand marks are separate from the code license. Reusable brand assets are maintained in [eddlev/air-brand](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.**
