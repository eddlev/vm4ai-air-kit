# AIR

AIR is a prompt-based AI project runtime.

In simple terms, AIR helps an AI stop acting like a generic chatbot and start acting like a structured project runtime:

- it starts a project in a controlled way
- it defines what the current step is
- it makes blockers explicit
- it keeps the work aligned to a project map
- it preserves continuity across sessions
- it helps the user understand what the next step is entering
- it can recommend which files or prompts should be attached next

AIR is not roleplay and not a simulation shell.  
It is a working method for turning a chat session into a project-oriented runtime.

## Quick Start

### Recommended default boot bundle

In a new session, attach:

- `AIR CORE RUNTIME.md`
- `AIR CONTROL SURFACE.md`
- `AIR DEFAULT STARTER PROFILE.json`

Then type:

```text
Start a new AIR project.

Answer onboarding and provide your sources.

That is the recommended default prompt-based AIR boot flow.

Continuation boot bundle

To continue an AIR project in a new session, attach:

AIR CORE RUNTIME.md
your previous AIR_HANDOFF_CARD

Then type:
Continue project from handoff card.

If you want the live session-management layer active in that continuation session too, also attach:

AIR CONTROL SURFACE.md
Why AIR exists

Most AI usage is still chat-based:

no explicit workflow
no clear active step
no explicit blockers
no project map
no continuity across sessions
no stable distinction between discussion, execution, and review

AIR introduces a different model:

Explicit workflow
Every session starts with onboarding, activation, and a defined execution path.
Map-first execution
AIR creates a project execution map before deep artifact execution.
Active-step discipline
Only the current step is executed. Future steps stay in the roadmap.
Orbit model (context governance)
The active task (Orbit 0) governs execution. Older context may support the work, but cannot silently override the current step.
Readiness-aware execution
AIR can frame what maturity stage the current work is actually in, what that stage allows, and what should not be scaled yet.
Contract-governed coding
For coding tasks, AIR does not treat generated code as terminal output by default. It requires contract formation, generation under contract, review, and decision posture.
Handoff continuity
AIR can transfer compact project state across sessions without rerunning the whole project from scratch.

AIR is not a better chatbot.

It is a different way to run AI work.

What AIR is for

AIR is not only for coding.

AIR is useful for any work that benefits from:

explicit workflow
current-step discipline
blockers and missing information being surfaced
compact continuity across sessions
controlled execution instead of vague drift

Typical use cases include:

software design and implementation
code review and structured file-by-file generation
security- and architecture-sensitive technical planning
product and systems design
research synthesis
strategic planning
operational planning
policy and compliance work
long-running multi-step projects that need continuity

If the work benefits from structure, sequencing, clarity, and explicit next-step control, AIR is a good fit.

How AIR differs from vibe coding

AIR is not anti-AI and not anti-speed.

But AIR is intentionally not vibe coding.

Vibe coding

The usual pattern is:

user gives natural-language request
model generates code
human chips away obvious slop, errors, or missing pieces
sometimes the subtractive review step is skipped entirely
AIR coding

AIR changes that pattern:

user gives natural-language request
AIR turns it into a task-operation contract
AIR surfaces blockers, missing vectors, and readiness constraints
code is generated under that contract
AIR reviews the result against the contract
AIR returns an explicit decision posture such as ACCEPT, REVIEW, or REJECT

That means AIR is trying to restore some of the additive discipline that traditional development had:

structure first
implementation second
review before acceptance

So AIR does not aim to be “faster vibes.”
It aims to be a more trustworthy runtime for structured work.

The AIR stack

The current prompt-based AIR stack is built around four files:

AIR CORE RUNTIME.md
AIR CONTROL SURFACE.md
AIR DEFAULT STARTER PROFILE.json
AIR HANDOFF CARD TEMPLATE.json
What each file does
AIR Core Runtime

Use this to:

start a new project
import a project
restore a project from a handoff card

It handles:

onboarding
routing
contract binding
activation
project initialization brief
project execution map
active-step artifact creation
readiness framing
next-task-state guidance
recommended attachment guidance

This is the entry runtime.

AIR Control Surface

Use this to control how AIR shows up once AIR is already active.

It governs:

live conversational behavior
structured exploration mode
compile mode
patch mode
update mode
handoff mode
coding interaction behavior
compact coding review escalation
lightweight session-management behavior

This is the live session-management layer.

AIR Default Starter Profile

Use this as the default governing contract for a new AIR project when no specialized profile is attached.

It defines:

compiler mode
referential policy
geometry bias
evidence posture
default artifact behavior
minimal active-step emission behavior
readiness and coding-governance requirements in the default starter contract

This is the default governing profile.

AIR Handoff Card Template

This is the continuation-state template.

It is used when:

ending a session
continuing in a new session
preserving active project state compactly

It carries:

active task state
blockers
selected vectors
degraded mode
readiness state
coding review state
decision posture
next recommended step

It does not replace the runtime prompts.
It is the continuity object.

Recommended usage model
New project

Attach:

AIR CORE RUNTIME.md
AIR CONTROL SURFACE.md
AIR DEFAULT STARTER PROFILE.json

Then start the project.

Continuation

Attach:

AIR CORE RUNTIME.md
previous AIR_HANDOFF_CARD

Optionally also attach:

AIR CONTROL SURFACE.md
Working with files

Reattach the latest working file when exact version fidelity matters, especially:

when multiple codebases are in play
when a file changed recently
when the model must act on the newest exact version
when prompt-session memory might drift to an earlier cached version
How AIR starts

When booted correctly, AIR should:

recognize the entry path
run onboarding or restore from handoff
bind the governing contract
create AIR session state
orient the user
emit a project execution map
generate only the current active-step artifact by default

It should not generate the entire future artifact chain unless explicitly asked.

The onboarding rubric

When AIR starts a new project, it asks five onboarding questions.

Q1 — What are you doing today?

Options:

A. New project
B. Import project
C. Continue project from handoff card
Q2 — How strictly should AIR check your work?

Options:

A. Light
B. Balanced
C. Strict
Q3 — When something is unclear, how should AIR handle it?

Options:

A. Resolve it early
B. Keep it open for now
C. Keep it open on purpose
Q4 — What should AIR keep consistent as you work?

Options:

A. Structure and logic
B. Structure and tone
C. Voice, identity, or relationships
Q5 — Describe your project and attach initial supporting sources

This is the actual project input.

Provide:

what you are working on
your goal
important constraints
pain points
priorities
attached files, if you have them

If you have no sources yet, say so.
AIR can still start in provisional source-light mode.

What happens after the project starts

Once onboarding is complete, AIR should produce:

1. AIR Runtime Bridge

This is the routing summary.
It shows how AIR interpreted onboarding and what posture it is taking.

2. AIR Session

This is the active runtime state.

3. AIR Project Initialization Brief

This is the compact human-readable orientation layer.

It should tell you:

whether the project has started
what phase AIR is in
why artifacts come before execution
what the next active step is
what next task state you are entering
whether any attachments are recommended for the next step
4. AIR Project Execution Map

This is the roadmap.

It should show:

current phase
current active step
blockers
critical path
next best step
completion definition
next task state
recommended attachments
readiness fields when the step is maturity-bearing
5. Current Active-Step Artifact

This is the only full artifact AIR should generate by default.

Future steps should stay in the project map until they become active.

Next-task guidance

AIR now supports a small operator-facing next-step layer.

next_task_state

This tells you what kind of step AIR believes is next.

Examples:

STRUCTURED_EXPLORATION
CODING_EXECUTION
COMPACT_REVIEW
DRIFT_RECOVERY
HANDOFF_GENERATION
SPECIALIZED_PROFILE_SWITCH
BACKEND_COMPILE_REQUIRED

This is there to prepare you for the next move:

mindset
focus
likely interaction type
whether new attachments may be needed
recommended_attachments

This tells you what AIR recommends attaching for the next step.

Examples:

["AIR_CONTROL_SURFACE", "latest_working_files"]
["AIR_CONTROL_SURFACE"]
["AIR_HANDOFF_CARD"]
["CODING_PROFILE", "latest_working_files"]

This is guidance, not magic.
It helps reduce operator guesswork.

AIR Maturity Readiness Scale

AIR uses a readiness framing model to help prevent premature scaling.

AMRS-0 — Problem Framing

Clarify objective, scope, and blockers.

AMRS-1 — Concept Shape

Define architecture candidates, vectors, and dependencies.

AMRS-2 — Executable Design

Define interfaces, boundaries, invariants, and review/test expectations.

AMRS-3 — Controlled Prototype

Allow narrow-scope implementation with explicit limits and visible incompleteness.

AMRS-4 — Integrated System

Allow subsystem connection, integration work, and reproducible execution paths.

AMRS-5 — Production Candidate

Allow deployment preparation, hardening, and stricter operational review.

AMRS-6 — Production Approved

Allow production-approval claims when the required checks are satisfied.

AIR uses AMRS as the operative model.
A future README revision may map AMRS to TRL as a human translation layer.

AIR Contract-Governed Code Generation Law

For coding tasks, AIR should not treat generated code as terminal output by default.

The coding sequence is:

contract formation
code generation under contract
contract-governed review
decision state

That means coding output should be shaped by:

the active task contract
blockers
missing vectors
readiness stage
architectural constraints
security and testing requirements
review posture

For coding tasks, AIR should surface:

review obligations
security checks
test requirements
architectural invariants
rejection conditions
decision state
Coding workflow in practice

When using AIR for coding, the working model is:

AIR takes technical lead on:
architecture
implementation structure
error handling
security considerations
the user may act as:
manual tester
operator
reviewer of exact outputs

AIR should not silently downgrade:

complete implementation into illustrative output
full code into snippets
implementation into pseudocode
production-grade work into placeholders or mockups

If AIR cannot complete the requested implementation safely, it should surface the blocker instead of pretending completion.

Using AIR during a live project

Once AIR is active, keep using:

AIR CONTROL SURFACE.md

This is the live session-management layer.

It is especially useful for:

coding execution
compact code review
drift correction
interaction-mode changes
handoff generation
Important rule

You do not need to attach AIR CONTROL_SURFACE.md on every single coding turn if the session is already behaving correctly.

Use it:

at boot by default
at continuation when you want live session control
when interaction mode changes
when drift occurs
when handoff or compact review behavior is needed
When to reattach files
Reattach working files when:
the file changed
multiple codebases are in play
precision matters
you suspect the model may be leaning on an older in-session version
Reattach AIR Control Surface when:
starting a fresh active session
the session drifted
interaction mode changed materially
coding/review/handoff behavior needs to be restored explicitly

Do not turn Control Surface reattachment into a ritual on every single turn.

Handoff continuity

A handoff card is AIR’s continuation object.

It is not narrative memory.
It is not a summary essay.
It is a restoration object.

A handoff can now carry:

active contract
task key
topic
blockers
selected vectors
degraded mode
dependency edges
next recommended step
runtime origin
artifact presence
project phase
current active step
current active-step artifact
readiness stage
readiness reason
stage constraints
promotion requirements
blocked capabilities
decision state
review obligations
security checks
test requirements
architectural invariants
rejection conditions
How to create a handoff

Use:

AIR CONTROL SURFACE.md
AIR HANDOFF CARD TEMPLATE.json

Then ask:
Generate an AIR handoff card for this project.

AIR should emit one JSON object with root key:
AIR_HANDOFF_CARD

Step-by-step: continuing from handoff
Step 1

Open a fresh session.

Step 2

Attach:

AIR CORE RUNTIME.md
the previous AIR_HANDOFF_CARD
Step 3

Type:
Continue project from handoff card.

Step 4

If you want the live interaction layer too, also attach:

AIR CONTROL SURFACE.md

AIR should restore the project state and continue from the restored active step.

Practical usage patterns
To start a new project

Attach:

AIR CORE RUNTIME.md
AIR CONTROL SURFACE.md
AIR DEFAULT STARTER PROFILE.json
To continue working in-session

Keep using:

the live session
latest working files when needed
AIR CONTROL SURFACE.md only if behavior needs to be restored or mode changes
To end cleanly

Generate:

AIR_HANDOFF_CARD
To resume later

Attach:

AIR CORE RUNTIME.md
previous AIR_HANDOFF_CARD
optionally AIR CONTROL SURFACE.md
Tested models

The current version has been tested successfully on:

ChatGPT 5.4
Claude Sonnet 4.6
Gemini Thinking

Gemini 3.1 Pro is currently underperforming and prone to hallucinations, so Gemini Thinking is the preferred Google option at the moment.

Gemini Thinking: add this when booting a new AIR project

When starting a new AIR project in Gemini Thinking, add this instruction together with the runtime prompt:
If the user explicitly says they are starting a new AIR project, treat Q1 as already answered:

Q1 = A. New project

Do not ask Q1 again in that case.
Proceed directly to Q2.

This stabilizes boot behavior for Gemini Thinking.

Agent integration (optional / experimental / untested)

AIR can be used together with external AI agent runtimes.

AIR does not execute tools itself.

Instead:

AIR defines the current active step
AIR determines when a step is ready for execution
AIR emits a structured execution specification

The agent runtime then:

executes tools
performs actions
returns outputs and evidence

This separation keeps AIR as the planning/control layer and the agent as the execution layer.

Notes
AIR is prompt-based unless connected to a real AIR backend.
Prompt-compiled AIR should remain explicit about being provisional when backend validation does not exist.
The current default behavior is designed to preserve focus by generating only the active-step artifact by default.
Specialized profiles are a future direction for domain-specific rulesets.
License

See LICENSE.