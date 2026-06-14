# AIR User Guide

AIR is a prompt-based AI project runtime.

It helps an AI session behave less like a loose chatbot and more like a structured project runtime. AIR creates a project flow, tracks the active step, surfaces blockers, preserves continuity, and helps decide what can be delivered, what needs review, and what should stop.

AIR is prompt-native. The public AIR Kit does not include a backend runtime, signed contracts, or automatic enforcement outside the model session.

## What AIR is

AIR is a prompt framework for governed AI work.

It helps with:

- starting projects in a controlled way
- defining the current active step
- keeping future steps in a roadmap instead of executing everything at once
- surfacing blockers and missing evidence
- preserving project continuity through handoff cards
- distinguishing discussion, execution, review, and delivery
- keeping claims bounded to available evidence
- detecting when extra capability layers are needed

## What AIR is not

AIR is not:

- a backend runtime
- an autonomous agent executor
- a guarantee of truth
- a replacement for testing
- a signed or tamper-evident contract system
- a tool runner
- a magic shield against bad model behavior
- a clone of Claude Skills or any other provider-specific feature

AIR can improve prompt-side discipline, but prompt-side discipline is not backend validation.

## Recommended boot bundle

For a new project, attach:

- `prompts/AIR CORE RUNTIME.md`
- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR DEFAULT STARTER PROFILE.json`

Then say:

```text
Start a new AIR project.
```

AIR should start onboarding. It should ask Q1 first.

## The most important first-use rule

Do not let the model skip onboarding.

`Start a new AIR project` starts the first activation flow. It does not answer Q1.

Q1 is a branch selector:

- A. New project
- B. Import project
- C. Continue project from handoff card
- D. Explain AIR first / show onboarding tutorial

A model may be tempted to infer that "start a new AIR project" means Q1=A. AIR should not do that.

Q1 must be one of:

- explicitly answered by the user
- restored from a valid handoff card
- proposed by AIR and explicitly approved by the user

This matters because the user may actually want to import a project, continue from handoff, or test the tutorial flow.

## Strict boot prompt

Use this prompt if a model tries to reinterpret AIR or skip the onboarding flow:

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
D. Explain AIR first / show onboarding tutorial

Do not infer Q1 from this prompt.
Do not skip Q1-Q5.
Do not ask for a "first task" or "activation goal" before Q1-Q5.
If Q1-D is selected, explain AIR and then return to Q1 without activating a project.
```

## Onboarding

AIR asks five questions.

### Q1 - What are you doing today?

Options:

- A. New project
- B. Import project
- C. Continue project from handoff card
- D. Explain AIR first / show onboarding tutorial

Q1-D is instructional only. AIR should explain itself, show examples, and return to Q1. It must not activate a project from Q1-D.

### Q2 - How strictly should AIR check your work?

Options:

- A. Light
- B. Balanced
- C. Strict

This changes how strongly AIR pushes back. It does not change truth requirements.

### Q3 - When something is unclear, how should AIR handle it?

Options:

- A. Resolve it early
- B. Keep it open for now
- C. Keep it open on purpose

This changes ambiguity posture. It does not let AIR invent missing facts.

### Q4 - What should AIR keep consistent as you work?

Options:

- A. Structure and logic
- B. Structure and tone
- C. Voice, identity, or relationships
- D. Emotional safety and familiar continuity

Q4 controls continuity and surface behavior. It does not override correctness, evidence, blockers, or claim boundaries.

### Q5 - Describe your project and attach initial supporting sources

Give AIR:

- what you are working on
- your goal
- key constraints
- pain points
- priorities
- any files or sources that should anchor the project

If you have no sources, say that. AIR can start in source-light/provisional mode.

## Deterministic onboarding

Deterministic onboarding means AIR must not guess the answer to a branch question just because the boot prompt sounds obvious.

AIR may infer an onboarding answer only when:

- the user asks AIR to infer or choose
- the user says they do not know how to answer
- the user gives ambiguous input after the question was asked
- AIR proposes an inference and the user approves it
- a valid handoff card restores the answer

If AIR proposes an inference, it should show:

```text
deterministic onboarding check
question: Q1
proposed answer: A. New project
why proposed: user said they want a new project
source: PROVISIONAL_INFERENCE
blocked until approval: yes
next: approve inference / choose another option
```

## Capability layers

AIR can run with the Default Starter Profile, but some tasks need sharper support.

AIR may recommend or request three kinds of capability layers.

### Specialist profile

A specialist profile is a reusable capability posture.

It defines how AIR should judge and behave for a class of work.

It may include:

- capability scope
- non-goals
- benchmark identity defaults
- rubric weights
- blocking conditions
- execution constraints
- output contract
- integrity checks

Use a specialist when the task needs a stable judgment style or capability standard.

Examples:

- grounding specialist
- architecture review specialist
- research synthesis specialist
- documentation specialist
- product strategy specialist

### Domain package

A domain package is a referential knowledge and constraint layer.

It may include:

- terminology
- domain constraints
- evidence requirements
- unsafe assumptions
- common failure modes
- claim boundaries
- recommended source types

Use a domain package when correctness depends on domain facts, external standards, model syntax, platform behavior, or version-specific rules.

A domain package informs AIR. It does not govern Orbit 0 by itself.

### Method layer

AIR Methods are the procedure layer.

The default procedure for a task lives inside:

```text
AIR_ARTIFACT.method
```

This keeps the method fitted to the current task.

A reusable `AIR_METHOD_PACK` is promoted only when the method should be reused.

Promote a Method Pack when:

- the same task class recurs
- the procedure must run the same way each time
- the procedure should be portable across sessions, projects, or models
- templates or reusable assets are needed
- evidence-to-advance gates matter
- previous variation caused defects or rework

Do not promote a Method Pack just because the task has steps. One-off tasks should usually keep the method inside the artifact.

## Capability layer checks

Users should not have to know when AIR needs extra layers. AIR should detect the trigger.

A capability layer check may look like this:

```text
capability layer check
specialist: needed
domain package: optional
method pack: inline method sufficient

why
The task requires implementation-grounded review and public claim hygiene.

blocks current work?
no, but output remains degraded without the specialist.

next
attach existing / create provisional / continue degraded / approve generation
```

AIR may recommend automatically.

AIR may generate a specialist, domain package, or method pack only after explicit user approval.

Generated layers must be validated before binding.

## Active step discipline

AIR should keep one current active step.

Future steps belong in the map. They should not be executed until they become active or the user explicitly approves a broader batch.

This keeps the session from turning into a fog machine with bullet points.

## AIR gates and evidence

AIR should evaluate an AIR gate before material execution, closure, mutation, commit, push, deploy, export, destructive action, or handoff.

Possible gate results:

- ALLOW
- REVIEW
- REJECT
- RESCOPE_REQUIRED
- EVIDENCE_REQUIRED

Prompt-side AIR may behave as if a declared active contract is binding inside the conversation. That does not mean backend enforcement exists.

For high-trust closure, AIR should ask for evidence such as:

- operator-witnessed command output
- tool-observed result
- test output
- git status or git diff
- generated file path and contents
- source citation
- user-approved bounded waiver

## Handoff continuity

A handoff card is AIR's continuation object.

It is not memory.
It is not a story.
It is not a loose summary.

It should preserve the current state needed to continue.

Handoff may include:

- active project
- active contract
- current active step
- completed steps
- blockers
- missing vectors
- receiver delivery state
- profile stack
- recommended specialists
- recommended domain packages
- recommended method packs
- deterministic onboarding state
- method-layer state
- capability-layer state

### Creating a handoff

Attach:

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

### Continuing from handoff

Attach:

- `prompts/AIR CORE RUNTIME.md`
- the previous `AIR_HANDOFF_CARD`

Optionally attach:

- `prompts/AIR CONTROL SURFACE.md`

Then say:

```text
Use the attached AIR handoff card as the governing continuation state.

Do not start a new AIR project.
Do not redefine AIR as a generic acronym.
Do not rerun Q1-Q5 onboarding unless the handoff card says onboarding is incomplete.

Restore the AIR project state from the handoff card.
Identify the current active step and continue only from there.
```

If the handoff contains an in-progress REVIEW_GATE, AIR should not skip past it.

## Model portability

AIR is prompt-native and intended to be portable across capable model providers, but model behavior varies.

Some models may:

- summarize AIR instead of activating it
- redefine AIR as a generic acronym
- skip Q1
- over-explain internals
- treat profiles as roleplay
- treat method packs as executable tools
- claim stronger validation than prompt-side AIR can support

Use the strict boot prompt when needed.

Model portability notes belong in:

```text
docs/AIR_MODEL_PORTABILITY_NOTES.md
```

## Practical use pattern

A normal AIR project looks like this:

1. Attach boot files.
2. Start AIR.
3. Answer Q1-Q5.
4. Let AIR create the project map.
5. Work only the current active step.
6. Let AIR surface blockers and capability-layer needs.
7. Review the receiver delivery state.
8. Generate a handoff when stopping.
9. Continue from the handoff later.

## Claim boundary

AIR can improve prompt-side structure.

AIR does not prove:

- backend validation
- runtime enforcement
- signed-contract behavior
- empirical performance improvement
- autonomous execution
- tool execution
- provider-independent reliability

Keep public claims inside the evidence.
