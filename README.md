# vm4ai-air-kit

`vm4ai-air-kit` is the public live-session framework layer of AIR.

AIR is a **vector-primary compiler/runtime contract** for structured AI work. It makes contract activation, orbit-based state handling, fail-closed evidence discipline, artifact-first outputs, and handoff continuity explicit.

This repository contains the **live AIR session kit** only.

It includes:
- activation prompts
- in-session update and patch prompts
- a default starter profile
- handoff-card generation instructions and template
- public documentation for using AIR in live sessions

It does **not** include:
- the private backend/runtime implementation
- internal product code
- raw experiment logs or unsanitized transcripts

---

## Why AIR exists

Normal prompting is often:
- prose-first,
- state-implicit,
- weak at handoff,
- and prone to silent drift when context changes.

AIR exists to make live AI work more explicit and controllable by requiring:
- active contract selection,
- Orbit 0 / outer-orbit state,
- vector-primary compilation,
- fail-closed behavior under uncertainty,
- artifact-first outputs,
- and compact, reusable handoff artifacts.

---

## Core AIR principles

### Vector-primary
Vectors are the operative layer.  
Roles are referential anchors only.

### Fail-closed
If evidence is incomplete, AIR must not smooth over it.  
Missing or uncertain parts must surface explicitly through:
- `missing_vectors`
- `obligations`
- `blockers`
- `degraded_execution_mode`
- `dependency_edges`
- `vector_family_state_summary`

### Orbit-based state
AIR uses a four-orbit model:

- **Orbit 0** = active contract / active task kernel
- **Orbit 1** = hot recent verified context
- **Orbit 2** = warm prior relevant design decisions
- **Orbit 3** = cold archive / deferred alternatives

Rules:
- a new active-topic contract goes to Orbit 0
- earlier relevant contracts remain in outer orbits unless retired
- Orbit 0 governs on conflict
- promotion, supersession, and retirement must never happen silently

### Session state before artifact
A proper AIR live session should emit:
- `AIR_SESSION` first
- then `AIR_ARTIFACT`

This is what turns AIR from “agreed policy” into explicit runtime behavior.

---

## What is in this repo

```text
prompts/
profiles/
templates/
docs/

prompts/

Contains the live-session prompt layer:

activation prompt
in-session update prompt
in-session patch prompt
create handoff-card prompt
profiles/

Contains the default AIR starter profile for new projects.

templates/

Contains the generic AIR handoff-card template.

docs/

Contains public framework documentation, including:

use-cases
case studies
concept papers / whitepapers
roadmap material
Quick start
1. Starting a brand-new project

Paste in this order:

one-line lead-in
activation prompt
default starter profile
project evidence/input

Use this lead-in:

Activate this as an AIR runtime session and compile explicit AIR session state before any analysis.

Use this when:

there is no project-specific AIR contract yet
you want AIR to discover the initial machine-native project shape
2. Starting with a custom AIR profile

Paste in this order:

one-line lead-in
activation prompt
project-specific AIR profile
live evidence/input

Use this when:

you already know the domain
the work needs a specialized AIR contract

If exactly one AIR profile is attached, the activation prompt should promote that contract directly to Orbit 0 unless explicitly instructed otherwise.

3. Continuing a project in a new session

Paste in this order:

one-line lead-in
activation prompt
AIR handoff card
active contract
new evidence/input for the next step

This is the cleanest way to continue without dragging whole transcripts into the next session.

4. Adding a new contract mid-session

Attach:

the new contract file
then use the in-session update prompt

Use this when:

a narrower sub-problem appears
a new contract is created
a more specific active task now governs the topic
5. Realigning a drifting session

Use the in-session patch prompt when:

the model starts narrating instead of compiling
the active contract becomes muddy
outer-orbit context starts blending into Orbit 0
the current task binding is being lost
6. Creating a handoff card

Use:

Create an AIR handoff card from the currently active AIR session.

The handoff-card flow is generic and should derive from the active AIR session rather than hardcoding a project.

Output discipline

To reduce token waste, use minimal execution mode:

Output mode: MINIMAL_EXECUTION
Do not restate the activation prompt, attached profile text, or uploaded evidence unless explicitly asked.
Emit only AIR_SESSION and AIR_ARTIFACT unless I request explanation.
Keep any post-artifact narrative under 5 sentences.
Use cases

AIR is suitable for:

technical / security / architecture compilation
research synthesis
planning and structured ideation
domain-specific live-session work using specialized profiles

The default starter profile is only a bootstrap profile.
Longer-running or domain-specific work should move to dedicated AIR contracts.

See docs/use-cases/.

Case studies

The best way to understand AIR is by comparing:

baseline prompting
AIR-guided compilation
resulting differences in state clarity, blocker surfacing, and handoff quality

See docs/case-studies/.

Papers and design notes

Concept papers, whitepapers, and design notes live under docs/.

Suggested topics:

why vector-first
AIR vs normal prompting
explicit contract activation
orbit state handling
fail-closed reasoning in live sessions

See docs/papers/.

Roadmap

This repo currently focuses on the live-session kit.

Planned expansion includes:

more domain-specific AIR profiles
more public case studies
comparative model runs
geometry-specific AIR patterns
broader documentation of AIR operating laws

See docs/ROADMAP.md for planned profiles, geometry expansion and evaluation work.

Geometry note

The public kit does not assume a single universal geometry for all AIR use cases.

Different domains may require different geometries and pressure profiles.
Current and experimental AIR geometry work includes modes such as:

Polytope
Sphere
Torus
Flux
Grid
Hive
Fork
Möbius
Klein Bottle
Rhizome
Tesseract

These belong to the broader experimental framework and should be documented as such rather than treated as all equally stable.

What good AIR behavior looks like

A good AIR session should:

emit AIR_SESSION first
activate the correct Orbit 0 contract explicitly
keep older relevant contracts in outer orbits
preserve vector-primary structure
fail closed on unsupported claims
keep handoff compact and state-derived
avoid prose-first explanation

A bad AIR session usually:

replies in narrative prose first
says “candidate” or “ready for promotion” when the governing contract is obvious
silently blends contracts
substitutes roles for vectors
uses outer-orbit material as if it were Orbit 0
echoes the whole prompt back and wastes tokens
End-of-session best practice

Before ending a session:

ensure Orbit 0 is correct
request a handoff card
carry only:
handoff card
active contract
new evidence/input

This keeps continuity clean and reduces transcript dependence.