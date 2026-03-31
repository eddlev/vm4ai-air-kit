# AIR

AIR is a prompt-based AI project runtime.

In simple terms, AIR helps an AI stop acting like a generic chatbot and start acting like a structured project runtime:
- it starts a project in a controlled way
- it defines what the current step is
- it makes blockers explicit
- it keeps the work aligned to a project map
- it supports handoff between sessions without losing the active state

AIR is not roleplay and not a simulation shell.
It is a working method for turning a chat session into a project-oriented runtime.

## Quick Start

1. Attach the following files in a new session:
   - AIR CORE RUNTIME PROMPT.md
   - air_default_starter_profile.json

2. Type in message:
   Start a new AIR project.

3. Answer onboarding.

That’s it.

## Why AIR exists

Most AI usage is still chat-based:
- no persistent structure.
- no clear active step.
- no explicit blockers.
- no continuity across sessions

AIR introduces a different model:

- **Explicit workflow**  
  Every session starts with onboarding, activation, and a defined execution path.

- **Map-first execution**  
  AIR creates a project execution map before generating artifacts.

- **Active-step discipline**  
  Only the current step is executed. Future steps stay in the roadmap.

- **Orbit model (context governance)**  
  The active task (Orbit 0) governs execution. Older context is retained but cannot silently override the current step.

- **Handoff continuity**  
  Project state can be transferred cleanly across sessions without losing alignment.

AIR is not a better chatbot.

It is a different way to run AI work.

## What AIR does

AIR gives the model a way to:
- start a project with a defined onboarding flow
- bind a starter profile as the governing contract
- create a project map
- generate only the artifact needed for the current active step
- keep future work visible without generating everything at once
- preserve continuity across sessions using a handoff card

The current AIR stack is built around four files:
- `AIR CORE RUNTIME PROMPT.md`
- `air_default_starter_profile.json`
- `AIR CONTROL SURFACE PROMPT.md`
- `air_handoff_card_template.json`

## Orbit model (context governance)

AIR uses an orbit-based model to control context:

- **Orbit 0 — Active Task Kernel**  
  The current step. This governs execution.

- **Orbit 1 — Hot Context**  
  Recent, relevant context supporting the current step.

- **Orbit 2 — Warm Memory**  
  Prior decisions and useful references.

- **Orbit 3 — Cold Archive**  
  Deferred or historical material.

Rule:
**Orbit 0 governs. Outer context cannot override the active task silently.**

This prevents drift and keeps execution aligned.

## What each file does

### AIR Core Runtime Prompt
Use this to start a project or restore a project from a handoff card.

It handles:
- onboarding
- routing
- contract binding
- first activation
- first artifact creation
- project initialization brief
- project execution map

This is the entry prompt.

### AIR Default Starter Profile
Use this together with the Core Runtime Prompt.

It is the default governing profile for a new project when no specialized AIR profile is attached.

It defines:
- compiler mode
- referential policy
- geometry bias
- evidence posture
- default artifact behavior
- orientation behavior
- minimal active-step emission behavior

### AIR Control Surface Prompt
Use this after AIR Core Runtime is already active.

It governs:
- how AIR behaves during the live session
- when to stay conversational
- when to become structured
- how to preserve the project map
- how to generate only the artifact for the current step
- how to create a handoff card

This is the session-management prompt.

### AIR Handoff Card Template
This is the template for continuation state.

It is used when:
- ending a session
- moving to a new session
- restoring the current project state later

It does not replace the runtime prompts.
It is the object that carries active state forward.

## Tested models

The current version has been tested successfully on:
- ChatGPT 5.4
- Claude Sonnet 4.6
- Gemini Thinking

Gemini 3.1 Pro is currently underperforming and prone to hallucinations, so Gemini Thinking is the preferred Google option at the moment.

## Gemini Thinking: add this when booting a new AIR project

When starting a new AIR project in Gemini Thinking, add this instruction together with the runtime prompt:

```text
If the user explicitly says they are starting a new AIR project, treat Q1 as already answered:

Q1 = A. New project

Do not ask Q1 again in that case.
Proceed directly to Q2.
```

Why this is needed:

Gemini Thinking can otherwise spend extra effort trying to reconcile instructions and may ask Q1 again even when the user already answered it implicitly by saying they are starting a new project.

This small addition stabilizes boot behavior.

## How AIR starts

When you boot a new AIR project correctly, AIR should do this:
1. recognize this is a new project
2. run onboarding
3. bind the starter profile
4. create AIR session state
5. orient you with:
   - a project initialization brief
   - a project execution map
6. generate only the artifact for the current active step

It should not immediately generate the entire future artifact chain unless you explicitly ask it to.

## The onboarding rubric

When AIR starts a new project, it asks five onboarding questions.

### Q1 — What are you doing today?
Options:
- A. New project
- B. Import project
- C. Continue project from handoff card

#### What each answer means

**A. New project**  
Use this when the project is starting from scratch.

AIR will:
- treat this as first activation
- bind the starter profile
- build the initial project map
- generate the first active-step artifact

**B. Import project**  
Use this when the project already exists outside AIR and you want AIR to take it over.

AIR will:
- treat your project materials as imported sources
- infer project structure from what you provide
- still start with onboarding and a project map
- generate the first active-step artifact based on the imported material

**C. Continue project from handoff card**  
Use this when you already have an AIR handoff card from an earlier session.

AIR will:
- restore the project from the handoff
- not re-run onboarding
- restore the active step
- continue from the last known project state

### Q2 — How strictly should AIR check your work?
Options:
- A. Light
- B. Balanced
- C. Strict

#### What each answer means

**A. Light**  
AIR keeps things moving and only flags major issues.

Use this when:
- you want speed
- you are brainstorming
- you do not want heavy friction

**B. Balanced**  
AIR flags important issues without blocking progress unnecessarily.

Use this when:
- you want structure
- you want guardrails
- you still want momentum

**C. Strict**  
AIR pushes hard on unresolved important issues.

Use this when:
- correctness matters
- you want hard discipline
- you do not want the model smoothing over gaps

### Q3 — When something is unclear, how should AIR handle it?
Options:
- A. Resolve it early
- B. Keep it open for now
- C. Keep it open on purpose

#### What each answer means

**A. Resolve it early**  
AIR will try to reduce ambiguity fast.

Use this when:
- you want convergence
- the project is technical or compliance-heavy
- open ambiguity is expensive

**B. Keep it open for now**  
AIR leaves uncertainty unresolved unless it blocks the current step.

Use this when:
- you want progress without fake certainty
- you are still shaping the project
- some ambiguity is acceptable

**C. Keep it open on purpose**  
AIR avoids closing ambiguity even if it could.

Use this when:
- exploration matters more than early narrowing
- the domain is intentionally open-ended
- you do not want premature closure

### Q4 — What should AIR keep consistent as you work?
Options:
- A. Structure and logic
- B. Structure and tone
- C. Voice, identity, or relationships

#### What each answer means

**A. Structure and logic**  
AIR prioritizes coherence, architecture, and reasoning shape.

Best for:
- technical work
- systems design
- policy/compliance
- implementation planning

**B. Structure and tone**  
AIR protects both the work structure and the way it sounds.

Best for:
- brand work
- product writing
- creative strategy
- polished documents

**C. Voice, identity, or relationships**  
AIR preserves continuity of voice and relational identity.

Best for:
- continuity-sensitive work
- symbolic or relational systems
- companion-style or identity-sensitive projects

### Q5 — Describe your project and attach initial supporting sources
This is the actual project input.

What to provide:
- what you are working on
- your goal
- important constraints
- pain points
- priorities
- attached files, if you have them

If you have no sources yet, say so.
AIR can still start in source-light mode.

What AIR does with Q5:
- infers the project domain
- determines initial task center
- sets provisional vector bias
- builds the first project map
- generates the active-step artifact

## What happens after the project starts

Once onboarding is complete, AIR should give you:

### 1. AIR Runtime Bridge
This is the routing summary.
It shows how AIR interpreted the onboarding.

### 2. AIR Session
This is the active runtime state.

### 3. AIR Project Initialization Brief
This is the human-readable orientation layer.

It should tell you:
- yes, the project has started
- which phase you are in
- why AIR is generating artifacts before direct execution
- what the next step is

### 4. AIR Project Execution Map
This is the roadmap.

It should show:
- current phase
- current active step
- current active-step artifact
- critical path
- blockers
- next best step
- what completion means

### 5. Current Active-Step Artifact
This is the only full artifact AIR should generate by default.

Future steps should stay in the project map until they become active.

## The key AIR operating rule

AIR should generate:
- the project map
- the current active-step artifact

It should not generate the entire future workflow as full artifacts by default.

That is intentional.

Why:
- preserves tokens
- keeps focus
- avoids overwhelm
- keeps Orbit 0 clean
- makes the session easier to steer

## Step-by-step: starting a new AIR project

Use these two files together:
- `AIR CORE RUNTIME PROMPT.md`
- `air_default_starter_profile.json`

### Step 1
Open a new session in the model you want to use.

### Step 2
Paste the contents of:
- `AIR CORE RUNTIME PROMPT.md`
- `air_default_starter_profile.json`

If you are using Gemini Thinking for a new project, also add the Gemini-specific Q1 instruction shown earlier.

### Step 3
Start the project with a clear message such as:

```text
Start a new AIR project.
```

Or, if you want to skip ambiguity:

```text
Start a new AIR project.

Q1 = A. New project
```

### Step 4
Answer the onboarding questions.

### Step 5
Provide the project description and any initial sources.

### Step 6
AIR should then:
- bind the starter profile
- create the session
- orient you
- create the project map
- emit the current active-step artifact

If AIR starts producing many future-step artifacts immediately, steer it back by saying:

```text
Generate only the current active-step artifact. Keep future steps in the project map.
```

## Using AIR during a live project

Once the project is active, use:
- `AIR CONTROL SURFACE PROMPT.md`

This prompt is for the ongoing session after AIR is already running.

Use it to keep AIR aligned while you work.

It helps AIR:
- stay focused on the current step
- keep the roadmap live
- avoid generating unnecessary future artifacts
- preserve blockers and next-step clarity
- produce a handoff card when needed

## Step-by-step: using AIR Control Surface

### Step 1
Make sure AIR has already been started with Core Runtime.

### Step 2
Paste `AIR CONTROL SURFACE PROMPT.md` into the same session.

### Step 3
Continue working normally.

You can ask things like:
- what is the current active step
- what is blocking this step
- update the project execution map
- generate the artifact for the current active step
- create a handoff card

### Step 4
If AIR starts drifting or generating too much, steer it back with:

```text
Keep the roadmap live and generate only the artifact for the current active step.
```

## What a handoff is

A handoff card is AIR’s continuation object.

It is the compact state AIR uses to continue a project in a new session without rerunning full onboarding.

A handoff card carries things like:
- active contract
- task key
- topic
- blockers
- selected vectors
- dependency edges
- next recommended step
- runtime origin
- artifact presence
- project phase
- current active step
- current active-step artifact

It is not narrative memory.
It is not a summary essay.
It is a restoration object.

## When to create a handoff

Create a handoff when:
- ending a session
- moving platforms
- switching to a fresh chat
- wanting a clean restart without losing project state

## How to create a handoff

Use:
- `AIR CONTROL SURFACE PROMPT.md`
- `air_handoff_card_template.json`

Then ask AIR for a handoff card.

Example:

```text
Generate an AIR handoff card for this project.
```

AIR should emit one JSON object with root key:

```json
AIR_HANDOFF_CARD
```

based on the active session state.

## Step-by-step: booting a new session from a handoff card

To continue an existing AIR project in a new chat:

### Step 1
Open a fresh session.

### Step 2
Paste:
- `AIR CORE RUNTIME PROMPT.md`
- the handoff card from the last session

You do not need to rerun onboarding when using a valid handoff card.

### Step 3
Start continuation with a clear message such as:

```text
Continue project from handoff card.
```

### Step 4
AIR should:
- detect the handoff card
- restore the active project state
- restore the active step
- restore blockers and next step
- continue from the restored state

### Step 5
Paste `AIR CONTROL SURFACE PROMPT.md` if you want the live session-management layer active in that continuation session too.

## Practical usage patterns

### To start a new project
Use:
- Core Runtime Prompt
- Starter Profile

### To keep the session aligned
Add:
- Control Surface Prompt

### To end cleanly
Generate:
- Handoff Card

### To resume later
Use:
- Core Runtime Prompt
- Handoff Card
- optionally Control Surface Prompt again

## Minimal recommended stack

For most users, the default working stack is:

### New session
- `AIR CORE RUNTIME PROMPT.md`
- `air_default_starter_profile.json`

### While working
- `AIR CONTROL SURFACE PROMPT.md`

### Before ending
- generate a handoff card

### New continuation session
- `AIR CORE RUNTIME PROMPT.md`
- previous `AIR_HANDOFF_CARD`
- optionally `AIR CONTROL SURFACE PROMPT.md`

## Notes

- AIR is prompt-based. It is not backend-compiled unless you have an actual AIR backend connected.
- Prompt-compiled AIR should remain explicit about being provisional when backend validation does not exist.
- The current default behavior is designed to preserve focus by keeping future work in the project map and generating only the active-step artifact.

## License

See `LICENSE`.
