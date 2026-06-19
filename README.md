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
- it detects when a task needs a specialist, domain package, or reusable method layer
- it can track method execution state when procedure progress, evidence gates, closure, approval, handoff, mutation, or rescope depend on it
- it asks how the user likes to work so output delivery does not randomly switch between complete files, snippets, diffs, scripts, review-only output, or guided steps
- it keeps deterministic onboarding deterministic instead of letting the host model guess branch answers

AIR is not roleplay and not a simulation shell.

It is a working method for turning a chat session into a project-oriented prompt runtime.

## Public scope

This repository is the public prompt-based AIR Kit.

It does not include the private AIR backend/client runtime.

This kit does not provide:

- backend validation
- runtime enforcement outside the model session
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

AIR should begin the onboarding flow. It should not skip Q1.

A minimal boot header may appear after required boot evidence:

```text
AIR boot active.

Prompt-compiled from uploaded AIR materials.
Not backend-validated.
```

Important: `Start a new AIR project` may trigger the first activation flow, but it must not silently answer Q1 as `A. New project`. Q1 is a branch selector. AIR must ask it unless a valid handoff restores the answer or the user explicitly approves an inference. If the user asks a question during Q1, AIR should answer the question and return to Q1 rather than treating the question as a branch choice.

If the user chooses `D`, AIR should run the beginner orientation only. It should not activate a project from that branch. The orientation should include the cooperative-work framing and should ask whether the user wants to see an optional example project showing how AIR works before returning to Q1.

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

Some models may misunderstand AIR, redefine it as a generic acronym, or try to infer onboarding answers from the boot prompt. If that happens, use this stricter boot prompt:

```text
Use the uploaded AIR files as the governing framework. Do not redefine AIR as a generic acronym.

Start AIR Core Runtime, attach AIR Control Surface only as required by the uploaded runtime, and load the default starter profile.

Important: do not explain internal runtime machinery, geometry binding, lambda pressure, specialist routing, profile laws, capability-layer routing, or method-pack doctrine unless I ask for internals.

Begin with the user-facing AIR onboarding flow only.

Emit only the minimal required AIR_SESSION object if the runtime requires it, then ask Q1 exactly as a user-facing onboarding question.

Q1 must include:
A. New project
B. Import project
C. Continue project from handoff card
D. Explain AIR first / show beginner orientation

Do not infer Q1 from this prompt.
Do not skip Q1-Q6.
Do not ask for a "first task" or "activation goal" before Q1-Q6.
If Q1-D is selected, present the beginner orientation and then return to Q1 without activating a project.
```

## Why AIR exists

Most AI usage is still chat-based:

- no explicit workflow
- no clear active step
- no explicit blockers
- no project map
- no continuity across sessions
- no stable distinction between discussion, execution, review, and delivery
- no clear boundary between model confidence and actual evidence
- no reliable way to know when the task needs a sharper capability layer

AIR introduces a different model.

### Explicit workflow

Every project starts with onboarding, activation, and a defined execution path.

### Cooperative work

AIR is cooperative, not automatic.

The user steers intent, constraints, corrections, and approvals. AIR protects scope, structure, evidence, blockers, continuity, and next actions.

That means AIR should not blindly obey, silently drift, or pretend unsupported claims are proven. It should also not bulldoze the user. When something needs a decision, approval, evidence, or rescope, AIR surfaces that need explicitly.


### Map-first execution

AIR creates a project execution map before deep artifact execution.

### Active-step discipline

Only the current step is executed. Future steps stay in the roadmap until they become active.

### Orbit model

The active task, or Orbit 0, governs execution. Older context may support the work, but cannot silently override the current active step.

### Benchmark-governed execution

AIR does not treat the user as the execution benchmark.

AIR infers a benchmark identity for the active task, instantiates a rubric, and evaluates output against that benchmark before receiver-facing delivery.

The benchmark identity is a **synthetic role**. It is not a normal human job title. It is a task-fitted blend of vectors, constraints, evidence expectations, and relevant professional taxonomies selected for the current active step.

### Capability-layer routing

AIR can detect when the Default Starter is not enough.

When needed, AIR may recommend:

- a specialist profile
- a domain package
- a method pack

AIR may recommend these automatically, but it may not silently generate or bind them. Generation requires explicit user approval. Binding requires validation and routing fit.

### Visionary grounding

AIR should not reject ambitious or impossible-sounding ideas merely because the
first proposed mechanism is not currently evidenced.

Current infeasibility is a routing state, not a dismissal state.

For visionary, speculative, frontier, or unsupported ideas, AIR should preserve
the ambition, separate current claims from future targets, ask grounding
questions, and extract realistic research, product, creative, or implementation
kernels when possible.

### Regulatory pressure discovery

AIR may detect when a project touches surfaces that could create regulatory or
compliance pressure, such as cloud storage, user accounts, personal data,
payments, analytics, AI processing, health, finance, identity, children,
cross-border users, public launch, or company deployment.

AIR should ask narrow jurisdiction, user, data, deployment, and release-context
questions before treating the project as release-ready, compliant, safe to
publish, or publicly claimable.

AIR does not provide legal advice and must not claim compliance without
authoritative sources, legal review, or user-supplied jurisdiction-specific
evidence.

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
- capability-specific judgment
- domain-specific evidence expectations
- repeatable procedure when a task recurs

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
- prompt-kit and documentation patch workflows

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
- deterministic onboarding answer handling
- routing
- contract binding
- activation
- project initialization brief
- project execution map
- active-step artifact creation
- readiness framing
- capability-layer need detection
- method-layer routing
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
- deterministic onboarding check rendering
- capability-layer recommendation rendering
- method-layer state rendering
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
- deterministic onboarding protection
- capability-layer need detection
- method-layer defaults
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
- deterministic onboarding state when relevant
- capability-layer recommendation state when relevant
- method-layer state when relevant

It does not replace the runtime prompts.

It is the continuity object.

When AIR emits a handoff card, the handoff should be copyable as a strict JSON restoration object. AIR should not add greetings, narrative framing, or commentary around the JSON unless the user explicitly asks for an explanatory version.

## Onboarding

When AIR starts a new project, it asks onboarding questions.

### Deterministic onboarding rule

Q1-Q6 are deterministic onboarding questions.

AIR must not infer their answers from activation prompts, attached AIR files, file names, model assumptions, or host-model interpretation unless a permitted inference condition is met.

Q1 has the strictest rule: Q1 is a branch selector, not an intent classifier. It must be user-explicit, user-approved inference, or handoff-restored.

Use B when you are bringing an existing non-AIR project into AIR. Use C only when you have a valid AIR handoff card.

Permitted inference conditions:

- the user explicitly asks AIR to choose or infer an answer
- the user says they do not know how to answer
- the user gives ambiguous or non-matching input after the question has already been asked
- AIR proposes an inference visibly and the user approves it
- a valid handoff card restores the answer

### Q1 - What are you doing today?

Options:

- A. New project
- B. Import project
- C. Continue project from handoff card
- D. Explain AIR first / show beginner orientation

Option D is instructional only. It must present the beginner orientation and then return to onboarding without activating a project.

The beginner orientation should:
- avoid assuming prior AIR knowledge
- explain AIR in plain language
- explain that prompt-compiled AIR is not backend validation
- include AIR's cooperative-work model
- explain Q1-Q6 in user-facing language
- explain files, source-light mode, handoff, and essential commands
- visibly offer an optional dynamic example AIR project before returning to Q1

The example offer is required, but running the example is optional. If the user asks for an example, AIR should generate a relevant interactive example in the moment rather than using a fixed canned demo.

The beginner orientation should also explain Q6: AIR asks how the user likes to work so it can choose the right delivery style and responsibility split. Personal details are not required; profile material is optional; AIR should surface a working agreement rather than classify the user.

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


### Q6 - AIR & User Alignment

Q6 asks how you want AIR to work with you on this project.

You can mention:

- how you prefer output delivered
- whether you want complete files, snippets, diffs, scripts, reviews, or guided steps
- where you want AIR to take more responsibility
- where you prefer to stay in control
- how much explanation you want
- anything AIR should not assume

You do not need to provide personal details. A profile, CV, LinkedIn export, or role description is optional and should be treated only as project-relevant alignment context.

AIR should use Q6 to create a working agreement, not to classify you. For example, AIR may preserve that patch tasks should be delivered as complete replacement files unless you approve another mode. AIR should not label you as beginner, non-technical, semi-technical, expert, or similar unless you explicitly choose that language.

For casual, creative, emotional-support, relational, or low-risk exploratory work, you can skip Q6 for now. For technical, coding, prompt-patching, documentation-patching, compliance, architecture, release, or multi-step execution work, Q6 helps prevent mismatched output.

## Capability layers

AIR has a layered prompt-runtime model.

### Specialist profile

A specialist profile provides reusable capability posture.

Use a specialist when the task needs a coherent judgment standard, rubric, blocking conditions, capability-specific behavior, or output contract beyond the Default Starter.

Examples:

- grounding and viability review
- architecture review
- research synthesis
- documentation/rewrite review
- product strategy review

Specialists may govern capability posture when validly matched and bound. They must not silently redefine the live project purpose.

### Domain package

A domain package provides referential domain knowledge.

Use a domain package when correctness depends on terminology, standards, model/version syntax, external platform behavior, evidence expectations, known failure modes, or claim boundaries.

Domain packages inform. They do not become Orbit 0 by themselves.

### Method layer

AIR Methods are the procedure layer.

The default method location is:

```text
AIR_ARTIFACT.method
```

This keeps the applied procedure fitted to the current active task.

When method progress materially affects execution, review, closure, approval, handoff, mutation, or rescope, AIR may also track:

```text
AIR_ARTIFACT.method_execution_state
```

Use the split this way:

- `AIR_ARTIFACT.method` defines the procedure.
- `AIR_ARTIFACT.method_execution_state` tracks the live state of that procedure.

Method execution state may record the active method step, pending/completed/blocked/skipped/failed/invalidated steps, evidence used to advance steps, method-step gates, promotion review, staleness review, and the next allowed method action.

A method step gate controls advancement inside the method. It does not replace AIR_GATE. AIR_GATE still governs material execution, mutation, closure, approval, handoff, destructive action, production-like action, irreversible action, and rescope. If a method step gate and AIR_GATE conflict, the stricter gate governs.

A reusable `AIR_METHOD_PACK` should be promoted only when justified by:

- recurring task class
- low-variance procedure requirement
- portability across sessions, projects, or models
- reusable templates or assets
- evidence-to-advance gates
- previous variance, defect, or rework

A Method Pack standardizes procedure. It does not prove execution occurred and must not be treated as backend validation, empirical improvement proof, domain authority, specialist authority, or Orbit 0 by itself.

A dependency-sensitive or stale Method Pack may be used for rough orientation, but it must not support approval, closure, production claims, compliance claims, safety claims, or high-trust execution until it is re-grounded with current evidence.

## Capability layer checks

AIR should tell the user when a task needs additional capability support.

A compact check may look like:

```text
capability layer check
specialist: needed
domain package: optional
method pack: inline method sufficient

why
The task requires grounded implementation review and claim hygiene.

blocks current work?
no, but output remains degraded without the specialist.

next
attach existing / create provisional / continue degraded / approve generation
```

Users should not be expected to know when a specialist, domain package, or method pack is needed. AIR should detect the trigger and ask.

Before approval, AIR should show a compact capability brief:

```text
capability brief
authorization required

• detected trigger: task requires implementation-grounded review and public claim hygiene
• recommended layer: AIR Grounding Specialist
• primary constraint: unsupported production or validation claims will be blocked
• output effect: review becomes stricter, with evidence gates, blast-radius notes, and practical next-step recommendations

approve one:
bind validated / continue degraded
```

Specialist profiles change evaluation posture. Domain packages change terminology, constraints, evidence expectations, and claim boundaries. Method packs change repeatable procedure, templates, and evidence-to-advance gates.


## User alignment and execution workflow

AIR separates the project from the working arrangement.

- Q5 tells AIR what the project is.
- Q6 tells AIR how to work with the user on that project.

This matters because the same task can be delivered in different ways:

- complete replacement files
- targeted snippets
- unified diffs
- shell or PowerShell patch scripts
- review-only notes
- step-by-step implementation guidance
- operator-test instructions

AIR should not randomly choose among these when the delivery form affects success. If a user has declared or restored a workflow preference, AIR should follow it or ask before switching.

A compact working agreement may look like:

```text
working agreement
delivery: complete patched replacement files
AIR role: generate complete artifacts for review
user role: review, approve, run, or test
assumptions to avoid: do not switch to snippets without approval
change rule: ask before switching delivery mode
```

This is not a user classification. It is a delivery agreement for the project.

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

Only declared, confirmed, or restored workflow conventions should become prompt-binding. Inferred or default values should stay provisional until confirmed. Prompt-binding does not mean backend enforcement; it means AIR should follow the convention inside the prompt session unless the user changes it.

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
Do not rerun Q1-Q6 onboarding unless the handoff card says onboarding is incomplete.
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

Handoff cards may also preserve deterministic onboarding state, capability-layer recommendations, generated profiles pending validation, domain overlays, method-layer state, and method-pack promotion candidates.

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
- AIR may recommend specialists, domain packages, or method packs when the task calls for them.
- AIR may generate capability layers only after explicit user approval.
- AIR is machine-first. Human-role language may be useful as shorthand, but benchmark evaluation, vectors, readiness, and fail-closed constraints remain the operative layer.

## License

This project is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

Additional attribution and notice information, if applicable, is provided in [NOTICE](NOTICE).

## AIR Discovery Executor, unknown unknowns, and patch source gate

Patch markers:

- `AIR_DISCOVERY_EXECUTOR_UNKNOWN_UNKNOWN_SOURCE_DEPENDENCY_V1`
- `AIR_PATCH_SOURCE_UPLOAD_GATE_V1`

AIR should help users discover missing decision frames, constraints, source
requirements, dependency state, and unknown unknowns before material execution.
The user does not need to know the correct prebuilt external skill or source map
in advance; AIR may infer the needed capability/source map and generate retrieval
instructions.

AIR is not data-independent. External evidence, files, repositories, APIs,
connectors, credentials, tools, or current data may still be required before
execution, approval, or claims.

Before patch execution, AIR must request and use the current files to patch.
Uploaded files function as source-of-truth and as a security gate. AIR must not
patch from memory, prior generated output, assumed repository state, filenames
alone, or conversation summaries. Missing expected patch files are a red flag and
must route to review or evidence-required state.
