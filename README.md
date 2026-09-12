<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=20260830-air250">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=20260830-air250" alt="AIR by VM4AI — Focused. Fluid. AIR. AI work, carried forward." width="100%">
  </picture>
</p>

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Foundation](https://img.shields.io/badge/foundation-2.6.1-C9A227?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)
![Channel](https://img.shields.io/badge/channel-release-56B581?labelColor=1A1613)

**AI work, carried forward.**

AIR (**AI Resource**) is a prompt-based framework for sustained work with AI.

Instead of treating every chat as an isolated conversation, AIR gives the AI an explicit project structure: what you are trying to accomplish, what is active now, what evidence matters, what requires your approval, and what needs to carry forward.

You talk to AIR normally. AIR handles the structure.

AIR is not a separate application or service stack. Its baseline runtime needs a compatible AI platform and the AIR Foundation. Additional tools, sources, services or specialist capabilities are determined by the work you ask AIR to do.

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

## Current release — AIR Kit v0.7.1

The current release is **AIR Kit v0.7.1**.

It includes:

- AIR Foundation **2.6.0**
- Handoff schema **2.3.0**, revision 16
- Specialist packages **2.5.0**
- Runtime Route Map **1.1.0**
- Specialist Package Index **1.3.0**

v0.7.1 is a hardening release over v0.7.0 and closes 74 audited findings across the AIR Foundation, Handoff, runtime contracts, Specialist packages and release tooling.

See the [v0.7.1 release](https://github.com/eddlev/vm4ai-air-kit/releases/tag/v0.7.1) for the detailed change and validation record.


## Development candidate - AIR Kit v0.7.2

This branch prepares **AIR Kit v0.7.2**. The latest published release remains v0.7.1 until a v0.7.2 tag/release is actually published.

v0.7.2 hardens AIR's control spine around new-task Artifact binding, exact task-to-Artifact action checks, failure capture, repository patch reconciliation, approval-scope identity reuse, Handoff revision 17, and required formal-object visibility.

### Best practices

**Cognitive scope authority isolation.** AIR v0.7.2 keeps adaptive reasoning inside the current task Artifact's declared cognitive scope. Cognitive findings are candidate contributions, not control state: they cannot directly change task/Artifact identity, deterministic routing, approval, Gate/Authorization/Receipt state, lease/scope pin, Handoff authority, or failure-registry authority. A contribution becomes operative only after the declared validation and ingestion boundary accepts it. This is an authority boundary, not a request for or exposure of private chain of thought.


**Thinking Effort.** AIR does not currently require a specific ChatGPT Thinking Effort setting. For day-to-day AIR use, **High** is a reasonable starting point. **Extra High** may be useful for unusually difficult analysis or architecture work, but there is not currently evidence that Thinking Effort causes or prevents AIR runtime drift. Treat cross-effort observations as empirical host-behavior evidence, not AIR execution authority.

**Known ChatGPT presentation issue.** AIR formal records have occasionally been observed inside ChatGPT's collapsed **`Worked for ...`** section rather than in the main response. Expanding that section reveals the records. This has so far only been observed on ChatGPT; the cause has not been isolated between AIR response-surface behavior and host UI routing. AIR formal records are structured governance records, not hidden reasoning or chain of thought. If expected records appear missing in ChatGPT, check that section and include the behavior in any bug report.

## Start AIR

Load the five required AIR Foundation files from [`prompts/`](prompts/):

```text
AIR_CORE_RUNTIME.md
AIR_CONTROL_SURFACE.md
AIR_GOV.md
AIR_DEFAULT_STARTER_PROFILE.json
AIR_HANDOFF_CARD_TEMPLATE.json
```

For normal use, also load the two recommended bootstrap catalogs from [`catalog/`](catalog/):

```text
AIR_RUNTIME_ROUTE_MAP.json
AIR_SPECIALIST_PACKAGE_INDEX.json
```

The five Foundation files govern AIR. The catalogs improve route and Specialist discovery but do not gain execution authority.

Then send:

```text
Start a new AIR project.
```

AIR validates the loaded Foundation and starts onboarding.

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

AIR uses a Handoff Card to carry recorded project state into another session or compatible platform.

Load the current AIR Foundation with the populated `AIR_HANDOFF_CARD.json` and choose the continuation route during onboarding.

Handoff can preserve project scope, the active task, decisions, blockers, working agreements, Specialist state and approval boundaries.

It transfers **recorded AIR state**. It does not transfer hidden model memory, hidden reasoning or previously granted execution authority. The receiving session validates and rebinds the project before material execution resumes.

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
prompts/   the five-file AIR Foundation
catalog/   route and Specialist discovery metadata
profiles/  optional Specialist capability packages
tools/     deterministic validation and release tooling
tests/     replayable contract, mutation and regression fixtures
```

## Community and bugs

Use [GitHub Issues](https://github.com/eddlev/vm4ai-air-kit/issues) for reproducible defects.

Use [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) for questions, integrations, portability observations, design discussion and feature ideas.

When reporting behavioral issues, include the AIR Kit release, AIR Foundation version, AI model/provider, platform, reproduction steps, expected behavior and observed behavior where possible.

## License and brand

AIR's code and prompt materials are licensed under **Apache-2.0**. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

AIR and VM4AI names and brand marks are separate from the code license. Reusable brand assets are maintained in [eddlev/air-brand](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.**
