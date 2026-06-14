# AIR

AIR is a prompt-based AI project runtime.

It helps an AI session behave less like a loose chatbot and more like a structured project runtime:

- it starts a project in a controlled way
- it defines the current active step
- it makes blockers explicit
- it keeps work aligned to a project map
- it preserves continuity across sessions
- it helps the user understand the next step
- it evaluates work against an inferred execution benchmark instead of the user's gap state
- it keeps claims bounded to available evidence

AIR is not roleplay and not a simulation shell.

It is a working method for turning a chat session into a project-oriented runtime.

## Public scope

This repository is the public prompt-based AIR Kit.

It does not include the private AIR backend/client runtime.

This kit does not provide:

- backend validation
- runtime enforcement
- signed contracts
- tamper-evident artifacts
- tool execution
- autonomous agent execution
- guaranteed correctness

Prompt-based AIR can improve structure, continuity, review posture, and execution discipline inside a model session.

Prompt-side discipline is not backend validation.

## Quick start

### New project boot bundle

Attach these files in a new model session:

- `prompts/AIR CORE RUNTIME.md`
- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR DEFAULT STARTER PROFILE.json`

Then type:

```text
Start a new AIR project.
```

AIR should run onboarding, bind the starter profile, orient the user, emit the project map, and generate only the current active-step artifact by default.

### Continuation boot bundle

To continue an AIR project in a new session, attach:

- `prompts/AIR CORE RUNTIME.md`
- your previous `AIR_HANDOFF_CARD`

Then type:

```text
Continue project from handoff card.
```

If you want the live session-management layer active in that continuation session too, also attach:

- `prompts/AIR CONTROL SURFACE.md`

## Strict boot prompt

Some models may misunderstand AIR or redefine it as a generic acronym. If that happens, use this stricter boot prompt:

```text
Use the uploaded AIR files as the governing framework. Do not redefine AIR as a generic acronym.

Start AIR Core Runtime, attach AIR Control Surface only as required by the uploaded runtime, and load the default starter profile.

Important: do not explain internal runtime machinery, geometry binding, lambda pressure, specialist routing, or profile laws unless I ask for internals.

Begin with the user-facing AIR onboarding flow only.

Emit only the minimal required AIR_SESSION object if the runtime requires it, then ask Q1 exactly as a user-facing onboarding question.

Q1 must include:
A. New project
B. Import project
C. Continue project from handoff card
D. Explain AIR first / show onboarding tutorial

Do not skip Q1-Q5. Do not ask for a "first task or activation goal" before Q1-Q5.
```

## Why AIR exists

Most AI usage is still chat-based:

- no explicit workflow
- no clear active step
- no explicit blockers
- no project map
- no continuity across sessions
- no stable distinction between discussion, execution, review, and delivery

AIR introduces a different model:

### Explicit workflow

Every project starts with onboarding, activation, and a defined execution path.

### Map-first execution

AIR creates a project execution map before deep artifact execution.

### Active-step discipline

Only the current step is executed. Future steps stay in the roadmap until they become active.

### Orbit model

The active task, or Orbit 0, governs execution. Older context may support the work, but cannot silently override the current active step.

### Benchmark-governed execution

AIR does not treat the user as the execution benchmark.

AIR infers a benchmark identity for the active task, instantiates a rubric, and evaluates output against that benchmark before receiver-facing delivery.

### Handoff continuity

AIR can transfer compact project state across sessions without rerunning the whole project from scratch.

## What AIR is for

AIR is useful for work that benefits from:

- explicit workflow
- current-step discipline
- blocker visibility
- missing-information visibility
- compact continuity across sessions
- controlled execution instead of vague drift
- evidence-aware review
- careful claim boundaries

Typical use cases include:

- software design and implementation
- code review and structured file-by-file generation
- security- and architecture-sensitive technical planning
- product and systems design
- research synthesis
- strategic planning
- operational planning
- policy and compliance-adjacent work
- long-running multi-step projects that need continuity

If the work benefits from structure, sequencing, clarity, and explicit next-step control, AIR is a good fit.

## How AIR differs from vibe coding

AIR is not anti-AI and not anti-speed.

But AIR is intentionally not vibe coding.

### Vibe coding

The usual pattern is:

1. user gives natural-language request
2. model generates output
3. human chips away at obvious slop, errors, or missing pieces
4. sometimes the subtractive review step is skipped entirely

### AIR execution

AIR changes that pattern:

1. user gives natural-language request
2. AIR turns it into a task-operation contract
3. AIR surfaces blockers, missing vectors, and readiness constraints
4. AIR infers the benchmark identity for the active task
5. output is generated under that contract and benchmark
6. AIR returns an explicit decision posture such as APPROVE, REVIEW, or REJECT
7. AIR emits receiver-facing output only when the delivery state allows it

AIR aims to restore some of the additive discipline that traditional development had:

- structure first
- execution second
- review before acceptance
- benchmark before delivery

AIR does not aim to be faster vibes.

It aims to be a more trustworthy runtime for structured prompt-based work.

## Repository layout

The core public AIR Kit is built around these prompt files:

- `prompts/AIR CORE RUNTIME.md`
- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR DEFAULT STARTER PROFILE.json`
- `prompts/AIR HANDOFF CARD TEMPLATE.json`

Additional profile material lives under:

- `profiles/`

Documentation lives under:

- `docs/`

## What each core file does

### AIR Core Runtime

Use this to:

- start a new project
- import a project
- restore a project from a handoff card

It handles:

- onboarding
- routing
- contract binding
- activation
- project initialization brief
- project execution map
- active-step artifact creation
- readiness framing
- benchmark identity inference
- receiver delivery state
- handoff restoration

This is the entry runtime.

### AIR Control Surface

Use this to control how AIR shows up once AIR is already active.

It governs:

- live conversational behavior
- compact structured exploration
- compile mode
- patch mode
- update mode
- handoff mode
- coding interaction behavior
- compact review escalation
- visibility commands
- help commands
- receiver delivery rendering

This is the live session-management layer.

### AIR Default Starter Profile

Use this as the default governing profile for a new AIR project when no specialized profile is attached.

It defines:

- compiler mode
- referential policy
- default geometry bias
- evidence posture
- active-step artifact behavior
- readiness and coding-governance requirements
- benchmark support
- prompt-side claim boundaries

This is the default governing profile.

### AIR Handoff Card Template

This is the continuation-state template.

It is used when:

- ending a session
- continuing in a new session
- preserving active project state compactly

It carries:

- active task state
- blockers
- selected vectors
- degraded mode
- dependency edges
- current active step
- decision posture
- next recommended step
- receiver delivery state
- benchmark state when relevant
- workflow and portability state when relevant

It does not replace the runtime prompts.

It is the continuity object.

## Onboarding

When AIR starts a new project, it asks onboarding questions.

### Q1 - What are you doing today?

Options:

- A. New project
- B. Import project
- C. Continue project from handoff card
- D. Explain AIR first / show onboarding tutorial

Option D is instructional only. It should explain AIR, show example answer sets, and then return to onboarding.

### Q2 - How strictly should AIR check your work?

Options:

- A. Light
- B. Balanced
- C. Strict

This modifies evaluation posture, not truth, hard constraints, or benchmark identity.

### Q3 - When something is unclear, how should AIR handle it?

Options:

- A. Resolve it early
- B. Keep it open for now
- C. Keep it open on purpose

This modifies ambiguity posture, not benchmark identity or hard reality constraints.

### Q4 - What should AIR keep consistent as you work?

Options:

- A. Structure and logic
- B. Structure and tone
- C. Voice, identity, or relationships
- D. Emotional safety and familiar continuity

Q4 meaning split:

- A is for analytical, technical, architectural, and structure-first work.
- B is for tone-sensitive but non-relational work.
- C is for relational, persona-continuity, identity-sensitive, or immersive work.
- D is for familiar artifacts, low-disruption edits, emotional safety, and continuity-sensitive delivery.

### Q5 - Describe your project and attach initial supporting sources

Provide:

- what you are working on
- your goal
- important constraints
- pain points
- priorities
- attached files, if you have them

If you have no sources yet, say so. AIR can still start in provisional source-light mode.

## Workflow declaration

AIR should ask for project workflow conventions before assuming them.

Important workflow questions:

1. How do you want changes delivered?
2. How should steps be named?
3. What counts as evidence?
4. What actions require approval?
5. What files, folders, systems, or data are off limits?
6. What should happen when scope changes?
7. What is the commit/checkpoint convention?
8. What is the delivery or handoff format?

Workflow convention source priority:

1. USER_DECLARED
2. USER_CONFIRMED
3. HANDOFF_RESTORED
4. INFERRED_PROVISIONAL
5. DEFAULT_PROVISIONAL

Only declared, confirmed, or restored workflow conventions should become binding. Inferred or default values should stay provisional until confirmed.

## AIR commands

AIR commands are prompt-side control phrases. They do not bypass gates or evidence requirements.

Useful commands include:

- `air help`
- `air -help`
- `air --help`
- `air help intro`
- `air help onboarding`
- `air status`
- `air object on`
- `air object off`
- `air compact`
- `air verbose`
- `air quiet`
- `air task`
- `air scope`
- `air uncertainty`
- `air ask`
- `air evidence`
- `air risks`
- `air sources`
- `air gate`
- `air approve?`
- `air handoff`
- `air patch plan`
- `air patch`

A good `air help` response should describe what commands do, when to use them, and whether they are read-only, review-gated, or mutation-capable.

## Handoff continuity

A handoff card is AIR's continuation object.

It is not narrative memory.
It is not a summary essay.
It is a restoration object.

To create a handoff, attach:

- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR HANDOFF CARD TEMPLATE.json`

Then ask:

```text
Generate an AIR handoff card for this project.
```

AIR should emit one JSON object with root key:

```text
AIR_HANDOFF_CARD
```

### Continue from handoff

Open a fresh session and attach:

- `prompts/AIR CORE RUNTIME.md`
- the previous `AIR_HANDOFF_CARD`

Optionally also attach:

- `prompts/AIR CONTROL SURFACE.md`

Then say:

```text
Use the attached AIR handoff card as the governing continuation state.

Do not start a new AIR project.
Do not redefine AIR as a generic acronym.
Do not rerun Q1-Q5 onboarding unless the handoff card says onboarding is incomplete.
Do not expose internal runtime machinery unless required.

Restore the AIR project state from the handoff card.
Identify:
1. current project
2. current active step
3. completed steps
4. current claim boundary
5. next recommended action

Then continue only from the next recommended step.
```

If the handoff contains an in-progress REVIEW_GATE step, AIR should not advance past it to a later recommended step without explicit user approval.

## Model portability

AIR is designed to be prompt-native and portable across capable LLM platforms, but boot quality and handoff restoration vary by model and interface.

AIR must not depend on a single model provider, hosted platform, deployment environment, jurisdictional access regime, or residency policy.

See:

- `docs/AIR_MODEL_PORTABILITY_NOTES.md`

## User guide

For a longer usage guide, see:

- `docs/AIR_USER_GUIDE.md`

## Tested model notes

Observed behavior changes over time. Treat this as empirical, not permanent.

Current observed notes are maintained in:

- `docs/AIR_MODEL_PORTABILITY_NOTES.md`

## Notes

- AIR is prompt-based.
- AIR Kit does not include the private AIR backend/client runtime.
- Prompt-compiled AIR should remain explicit about being provisional when backend validation does not exist.
- The default behavior is designed to preserve focus by generating only the active-step artifact by default.
- Specialized profiles may be attached when relevant, but the default starter remains the normal starting point.
- AIR is machine-first. Human-role language may be useful as shorthand, but benchmark evaluation, vectors, readiness, and fail-closed constraints remain the operative layer.

## License

See `LICENSE`.
