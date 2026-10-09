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

AIR (**AI Resource**) is a prompt-based framework for sustained work with AI. It gives a project an explicit working structure: what is active, what evidence matters, what requires approval, and what should carry forward between sessions.

This branch is the **AIR Kit v0.8.1 source-synchronization candidate**. It aligns the public repository with the R23 AMRS-6 runtime that was promoted in v0.8.0, fixes release/CI drift, reconciles stale current Handoff metadata, and makes the supported boot commands explicit. It is not a published v0.8.1 release until the candidate completes acceptance and release governance.

## Start AIR-P

For normal use, load the AIR client/repository files required by your AI platform and send one short first message.

Default routine boot:

```text
Start a new AIR-P project.
```

Explicit boot profiles:

```text
Start a new AIR-P project. Tier0 boot.
Start a new AIR-P project. Tier1 boot.
Start a new AIR-P project. Tier2 boot.
Start a new AIR-P project. Tier3 boot.
```

The default command resolves to **Tier0 routine boot**. Tier0 is the normal starting point and should retrieve only the minimum dependency closure needed to establish valid boot state and reach Q1.

- **Tier0** — routine boot; minimum sufficient retrieval.
- **Tier1** — adds compact navigation/index material.
- **Tier2** — retrieves exact authoritative source for an explicit target. If no target is available, AIR asks for the smallest missing target instead of widening retrieval.
- **Tier3** — full release-integrity/deep-audit path.

Selecting the new-project entry path does **not** answer Q1. AIR still surfaces Q1 and waits for an allowed onboarding answer source.

## Retrieval boundary

Tier0, Tier1 and Tier2 use a closed retrieval plan. Exact section or JSON-subtree boundaries are hard limits for model-visible reads. If a host or retrieval tool returns adjacent context outside the allowed boundary, that context must be discarded before model-visible ingestion; if exact filtering cannot be established, the affected profile/case fails closed rather than silently widening retrieval.

## Current runtime identity

The v0.8.1 candidate retains the promoted R23 runtime identities unless explicitly changed by the candidate source delta:

- AIR Core Runtime **2.9.0**
- AIR Control Surface **2.7.0**
- AIR Governance Supplement **2.4.0**
- Default Starter **2.7.0**
- Handoff schema **2.3.0**, template revision **26**
- Runtime Route Map **1.2.5**
- Specialist Package Index **1.3.15**
- **83** stable law identities and **28** floor invariants
- five Specialist package distributions

The current v0.8.1 source candidate is derived from the exact R130 source tuple and changes only the bounded source files recorded in `release/SOURCE_DELTA_R130_TO_R131_V081_CANDIDATE.json`.

## Repository structure

```text
prompts/       current user-facing AIR Foundation prompt surfaces
catalog/       current route, law and Specialist discovery metadata
air_p/         checked-in non-executable client/runtime build
specialists/   five Specialist package distributions
evidence/      retained package validation evidence
source/        exact canonical source, compiler, tests and law-source bodies
release/       current source/repository candidate manifests
tools/         current validation plus retained historical release tooling
tests/         retained historical public validation evidence and fixtures
```

The old `profiles/` layout is superseded by `specialists/` for the v0.8.1 source candidate.

## Validation

The active v0.8.1 CI contract does not reuse the v0.7.4 release seal. It validates the current canonical source tuple, runs the canonical compiler tests, performs three deterministic compiler builds, compares the checked-in runtime against the generated build, verifies the Specialist carry-forward baseline, and runs mutation tests against the current repository contract.

Historical v0.7.x validators remain repository history/tooling only and are not current release authority.

## Human approval and material actions

AIR separates conversational agreement from material authorization. When an exact approval token is required, it authorizes only the stated scope. Approval does not prove execution; AIR separately reconciles the resulting effect and receipt evidence.

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for bounded public contribution attribution, including external behavioral QA contributions to the R23 hardening cycle.

## Community

Use [GitHub Issues](https://github.com/eddlev/vm4ai-air-kit/issues) for reproducible defects and [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) for questions and design discussion.

## License and brand

AIR's code and prompt materials are licensed under **Apache-2.0**. See [LICENSE](LICENSE) and [NOTICE](NOTICE). AIR and VM4AI names and brand marks are separate from the code license.

---

**Built with AIR, reviewed by a human.**
