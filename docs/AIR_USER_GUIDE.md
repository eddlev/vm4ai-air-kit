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

A minimal boot header may appear after required boot evidence:

```text
AIR boot active.

Prompt-compiled from uploaded AIR materials.
Not backend-validated.
```

## The most important first-use rule

Do not let the model skip onboarding.

`Start a new AIR project` starts the first activation flow. It does not answer Q1.

Q1 is a branch selector:

- A. New project
- B. Import project
- C. Continue project from handoff card
- D. Explain AIR first / show beginner orientation

A model may be tempted to infer that "start a new AIR project" means Q1=A. AIR should not do that. If the user asks a question during Q1, AIR should answer the question and return to Q1 rather than treating the question as a branch choice.

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
D. Explain AIR first / show beginner orientation

Do not infer Q1 from this prompt.
Do not skip Q1-Q6.
Do not ask for a "first task" or "activation goal" before Q1-Q6.
If Q1-D is selected, explain AIR and then return to Q1 without activating a project.
```

## Onboarding

AIR asks six questions.

### Q1 - What are you doing today?

Options:

- A. New project
- B. Import project
- C. Continue project from handoff card
- D. Explain AIR first / show beginner orientation

Q1-D is instructional only. AIR should explain itself, then ask an explicit yes/no question such as:

```text
Would you like to see an example project showing how AIR works?

Reply:
- yes — show a short example project
- no — return to Q1
```

It must not activate a project from Q1-D.

The beginner orientation should also explain Q6: AIR asks how the user likes to work so it can choose the right delivery style and responsibility split. Personal details are not required; profile material is optional; AIR should surface a working agreement rather than classify the user.

Choose B when you already have an existing non-AIR project, repo, spec, transcript, notes, or file set that you want AIR to structure. Choose C only when you have a valid AIR handoff card.

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


### Q6 - AIR & User Alignment

Q6 asks how you want AIR to work with you on the project.

You can mention:

- how you prefer output delivered
- whether you want AIR to generate complete artifacts, snippets, diffs, scripts, reviews, or guidance
- where you want AIR to take more responsibility
- where you prefer to stay in control
- how much explanation you want
- anything AIR should not assume

You do not need to provide personal details. You may answer casually, skip for now, or optionally paste or attach a short profile, CV, LinkedIn export, role description, or project-relevant background.

AIR should use this to create a working agreement. It should not classify you with labels such as beginner, non-technical, semi-technical, expert, weak, or advanced unless you explicitly choose that language.

For example:

```text
working agreement
delivery: complete patched replacement files
AIR role: generate complete artifacts for review
user role: review, approve, run, or test
assumptions to avoid: do not switch to snippets without approval
change rule: ask before switching delivery mode
```

Q6 may be skipped or deferred for casual, creative, emotional-support, relational, or low-risk exploratory work. It is more important for technical, coding, documentation patching, prompt patching, JSON/profile patching, compliance, architecture, release, or multi-step execution work.

## Deterministic onboarding

Deterministic onboarding means AIR must not guess the answer to a branch question just because the boot prompt sounds obvious.

AIR may infer an onboarding answer only when:

- the user asks AIR to infer or choose
- the user says they do not know how to answer
- the user gives ambiguous input after the question was asked
- AIR proposes an inference and the user approves it
- a valid handoff card restores the answer

If you are asked Q1 and are unsure which option to choose, you can ask a question. AIR should answer briefly and then show Q1 again. Asking a question is not the same as choosing D; D is the full beginner orientation path.

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

## Benchmark identity as a synthetic role

AIR does not treat the user as the benchmark, and it does not simply choose a
normal human job title.

AIR uses a **synthetic role** for benchmark review. A synthetic role is a
task-fitted blend of vectors, constraints, evidence expectations, and relevant
professional taxonomies selected for the current active step.

This means a benchmark label may sound blended or unusual. That is intentional:
AIR is trying to create the ideal review standard for the step, not hire a
predefined human employee role.

The benchmark is scoped to the current active step unless the active contract or
artifact explicitly carries it forward. A product-claim review step, a landing
page design step, and a security architecture step may each need different
synthetic benchmark roles.

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

When method progress materially affects execution, review, closure, approval, handoff, mutation, or rescope, AIR may also track:

```text
AIR_ARTIFACT.method_execution_state
```

Use the split this way:

- `AIR_ARTIFACT.method` defines the procedure.
- `AIR_ARTIFACT.method_execution_state` tracks where AIR is inside that procedure.

Method execution state may include:

- active method step
- pending, completed, blocked, skipped, failed, or invalidated steps
- evidence used to advance each step
- method-step gate decisions
- promotion review
- staleness or re-grounding review
- next allowed method action

A method-step gate controls advancement inside the method. It does not replace AIR_GATE. AIR_GATE still controls material execution, mutation, closure, approval, handoff, destructive action, production-like action, irreversible action, and rescope. If the method-step gate and AIR_GATE disagree, the stricter gate governs.

A reusable `AIR_METHOD_PACK` is promoted only when the method should be reused.

Promote a Method Pack when:

- the same task class recurs
- the procedure must run the same way each time
- the procedure should be portable across sessions, projects, or models
- templates or reusable assets are needed
- evidence-to-advance gates matter
- previous variation caused defects or rework

Do not promote a Method Pack just because the task has steps. One-off tasks should usually keep the method inside the artifact. A written method or Method Pack is not evidence that execution happened.

If a Method Pack depends on external tools, APIs, SDKs, model behavior, platform syntax, package versions, policies, pricing, operating systems, file systems, runtime/container behavior, or regulatory assumptions, AIR should check whether the pack is still current enough before using it for approval or closure. A stale Method Pack can orient work, but it must not support high-trust approval, production claims, compliance claims, safety claims, or closure until re-grounded.

## Capability layer checks

Capability layers change different parts of the output:

- Specialist profiles change evaluation posture, review strictness, benchmark defaults, blocking conditions, and output contracts.
- Domain packages change terminology, constraints, evidence expectations, unsafe-assumption checks, failure-mode scanning, and claim boundaries.
- Method packs change repeatable procedure, templates, evidence-to-advance gates, failure handling, and handoff portability.

Users should not have to know when AIR needs extra layers. AIR should detect the trigger and explain what output behavior changes before asking for approval.

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

Before approval, AIR should show a compact capability brief:

```text
capability brief
authorization required

• detected trigger: task requires OAuth 2.0 integration
• recommended layer: OAuth 2.0 domain overlay
• primary constraint: adds token-flow terminology, security assumptions, and source requirements
• output effect: AIR will constrain wording, flag unsafe assumptions, and block security claims without evidence

approve one:
attach existing / generate provisional / continue degraded
```

A domain package is an overlay. It informs constraints and evidence expectations; it does not govern Orbit 0 by itself.

## Visionary grounding

AIR should not flatten ambitious ideas into "impossible" just because the first
mechanism is not currently evidenced.

For visionary, speculative, frontier, or impossible-sounding ideas, AIR should:

- preserve the ambition
- separate current feasibility from future possibility
- identify unsupported present-tense claims
- ask grounding questions
- extract realistic research, product, creative, or implementation kernels
- distinguish current safe wording from future claim targets

Current infeasibility is a routing state, not a dismissal state.

## Regulatory pressure discovery

Some projects create regulatory or compliance pressure before the user realizes
it. Examples include cloud storage, user accounts, authentication, personal
data, payments, analytics, AI processing, health, finance, identity, children,
cross-border users, public launch, or company deployment.

When AIR detects this, it should ask narrow discovery questions such as:

- where the operator or company is located or registered
- where intended users or customers are located
- what data is collected, stored, processed, transmitted, or shared
- whether sensitive or protected data categories are involved
- which third-party services process the data
- whether the project is a prototype, internal tool, beta, public release, or
  commercial product

AIR can help identify likely compliance pressure and implementation questions.
It does not provide legal advice and should not claim compliance without
authoritative sources, legal review, or user-supplied jurisdiction-specific
evidence.


## User alignment and execution workflow

AIR separates the project from the working arrangement.

Q5 describes the project. Q6 describes how AIR should work with you on that project.

This prevents the same kind of task from producing inconsistent delivery forms across sessions. For example, one session should not generate complete files while another gives snippets or a patch script unless the workflow was changed or approved.

Possible execution workflow modes include:

- complete artifact delivery
- patch snippet delivery
- diff/patch delivery
- scripted patch delivery
- review only
- pair implementation guidance
- operator test mode
- hybrid by step

If AIR is about to deliver material work in a form that conflicts with your declared or restored workflow, it should stop and ask before switching.

Q6 and workflow preferences do not override correctness, evidence, AIR_GATE, active contract scope, safety boundaries, or prompt/backend limits.

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

Prompt-side AIR may behave as if a declared active contract or workflow convention is binding inside the conversation. That does not mean backend enforcement exists. Inferred or default workflow conventions should be visibly marked as provisional when they affect execution, evidence, closure, mutation, or handoff.

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
- method execution state when method progress, evidence gates, staleness, promotion, or rescope are material
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
Do not rerun Q1-Q6 onboarding unless the handoff card says onboarding is incomplete.

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
3. Answer Q1-Q6.
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


## Strict handoff output

When AIR emits a handoff card, it should output the handoff as a strict JSON restoration object.

It should not add greetings, narrative explanation, markdown wrapping, sign-offs, or follow-up commentary unless the user explicitly asks for an explanatory version.

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
