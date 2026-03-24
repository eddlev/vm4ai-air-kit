# ROADMAP — vm4ai-air-kit

## Purpose

This roadmap describes the planned evolution of `vm4ai-air-kit` as the public live-session framework layer of AIR.

This repository is intended to expose the **session/runtime method**, not the private backend implementation.

The focus of this roadmap is therefore:

- live-session usability
- contract activation correctness
- orbit-state handling
- artifact quality
- handoff continuity
- domain-specific AIR profiles
- geometry expansion
- comparative evaluation

---

## Current scope

The repository currently contains the **core live-session kit**:

- AIR activation prompt
- AIR in-session update prompt
- AIR in-session patch prompt
- AIR handoff-card creation prompt
- AIR handoff-card template
- AIR default starter profile
- public README and supporting documentation

This is the stable public starting layer.

---

## Development principles

The roadmap follows these principles:

1. **Vector-primary**
   AIR remains vector-first. Roles stay referential only.

2. **Fail-closed**
   Unsupported claims should become blockers, obligations, missing vectors, or degraded modes.

3. **Explicit state**
   Session state, contract activation, orbit placement, and handoff continuity should be materialized, not implied.

4. **Artifact-first**
   AIR should emit structured runtime artifacts before narrative explanation.

5. **Public framework / private implementation boundary**
   The public repo should document the method and live-session kit without exposing private backend/runtime code.

---

# Phase 1 — Stabilize the public live-session kit

## Goal
Make the current public kit consistent, easy to understand, and reusable.

## Priorities
- finalize README and public framing
- normalize file naming and folder structure
- stabilize activation / update / patch / handoff prompt set
- ensure all templates are consistent with runtime law
- reduce prompt echoing and token waste
- document minimal execution mode clearly

## Deliverables
- stable `README.md`
- stable `docs/ROADMAP.md`
- stable prompt set under `/prompts`
- stable starter profile under `/profiles`
- stable handoff template under `/templates`

## Success criteria
- a new user can run a live AIR session without additional explanation
- the activation prompt produces explicit AIR session state
- update and patch flows behave predictably
- handoff cards can be generated consistently from active session state

---

# Phase 2 — Domain-specific AIR profiles

## Goal
Expand beyond the default starter profile into reusable domain contracts.

The default starter profile is a **bootstrap profile**, not a universal production profile.

## Planned profiles
- technical / security / architecture profile
- research synthesis profile
- creative / brand / narrative profile
- sales / GTM / market strategy profile
- relational / companion / symbolic profile

## Why this matters
Different project types require different:
- geometry bias
- vector family preferences
- blocking conditions
- evidence thresholds
- output constraints

## Deliverables
- curated domain-specific AIR profiles
- documentation for when to use each one
- guidance for moving from starter profile to specialized profile

## Success criteria
- users can choose an appropriate domain profile instead of overusing the default starter
- high-dimensional use cases no longer rely on the grid/polytope starter alone

---

# Phase 3 — Geometry expansion

## Goal
Document and progressively expose AIR’s broader geometry model.

The public kit should not assume that one geometry is correct for every domain.

## Current direction
The default starter profile currently biases toward:
- `GRID_LATTICE`
- `POLYTOPE_CORE`

This is appropriate for:
- deterministic compilation
- technical scoping
- security-sensitive and auditable work

But AIR is intended to support broader geometries for broader use cases.

## Planned geometry documentation
### Standard / near-term geometries
- Polytope
- Sphere
- Torus
- Flux
- Grid

### Experimental / radical geometries
- Hive
- Fork / Purple Swarm
- Möbius
- Klein Bottle
- Rhizome
- Tesseract

## Deliverables
- geometry overview document
- per-geometry intent notes
- stability labels for each geometry
- guidance on which domains each geometry is likely to support best

## Success criteria
- geometry choice becomes a documented AIR design decision
- users understand that starter geometry is a bootstrap, not a universal default

---

# Phase 4 — Use cases and case studies

## Goal
Show AIR in practice instead of only describing it abstractly.

## Planned documentation
### Use cases
- technical security architecture
- trust/protocol design
- creative brand development
- sales/GTM planning
- relational / symbolic interaction design

### Case studies
- AIR vs normal prompting
- AIR contract activation in live sessions
- AIR handoff continuity across sessions
- AIR under contract narrowing / sub-contract promotion
- comparative model behavior:
  - ChatGPT
  - Gemini
  - Claude

## Deliverables
- `docs/use-cases/`
- `docs/case-studies/`
- sanitized examples of AIR session + artifact outputs

## Success criteria
- readers can see concrete advantages of AIR
- the repo demonstrates actual practice, not just theory

---

# Phase 5 — Concept papers / whitepapers

## Goal
Explain the reasoning behind AIR in a more rigorous way.

## Planned papers
- why vector-first
- AIR vs normal prompting
- explicit contract activation and orbit state
- fail-closed live-session reasoning
- handoff continuity and session persistence
- geometry as a task-shaping mechanism

## Deliverables
- `docs/papers/`
- at least one foundational design paper
- comparative examples supporting AIR’s design decisions

## Success criteria
- AIR’s intent is understandable without relying on private context
- the framework has a clear public conceptual foundation

---

# Phase 6 — Evaluation and comparison

## Goal
Evaluate AIR behavior across models and across prompting modes.

## Areas of comparison
- AIR vs baseline prompting
- AIR under session continuation
- AIR under contract updates
- AIR under drift / patch correction
- AIR across models:
  - ChatGPT
  - Gemini
  - Claude

## What to measure
Not scientific benchmarking yet, but structured qualitative comparison:
- contract activation correctness
- orbit handling correctness
- artifact normalization quality
- drift resistance
- handoff quality
- hallucination control / fail-closed behavior

## Deliverables
- evaluation rubric
- model comparison notes
- example transcripts and artifact comparisons

## Success criteria
- AIR’s practical benefits become observable and demonstrable
- differences between models become documented rather than anecdotal

---

# Phase 7 — Toward implementation bridge

## Goal
Prepare the public framework layer for clean integration with a private implementation/runtime.

## Focus
- keep public repo method-focused
- define stable contract and artifact structures
- reduce ambiguity between public prompts and private runtime behavior
- make AIR_SESSION / AIR_ARTIFACT / AIR_HANDOFF_CARD shapes more reusable

## Deliverables
- stable public schemas
- clearer separation between framework kit and implementation layer
- improved interoperability between public docs and private runtime

## Success criteria
- the public repo remains useful on its own
- the private implementation can evolve without confusing the public method

---

# Known risks

- overfitting AIR to one project or one domain
- letting the default starter profile stand in for domain-specific profiles too long
- confusing “agreement with the contract” for true AIR session-state execution
- allowing verbose prompt echoing to waste tokens and degrade usability
- treating experimental geometries as stable before they are documented clearly

---

# Near-term next steps

## Immediate
- finalize `README.md`
- finalize `docs/ROADMAP.md`
- add `docs/use-cases/`
- add `docs/case-studies/`
- add `docs/papers/`

## After that
- create first domain-specific AIR profiles
- document geometry classes and their intended uses
- produce first AIR vs normal prompting case study
- produce first cross-model comparison case study

---

# Long-term vision

`vm4ai-air-kit` should become the public, reusable framework layer for structured AIR live sessions:

- explicit contract activation
- orbit-based state management
- vector-first compilation
- fail-closed evidence discipline
- artifact-first output
- clean handoff continuity
- domain-specific profiles
- geometry-aware task shaping

The public kit should make AIR understandable, inspectable, and reusable — while leaving private implementation details outside the repository.