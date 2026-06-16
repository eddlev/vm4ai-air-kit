# AIR Prompt Runtime Roadmap

This roadmap is for the public prompt-based AIR Kit.

It does not cover the private AIR backend/client runtime.

## Scope

This repository is limited to prompt-native AIR.

In scope:

- AIR prompt files
- starter profiles
- optional specialist profiles
- optional domain packages
- optional method packs
- handoff templates
- public documentation
- prompt-side usage guidance
- prompt-side model portability notes
- examples and case studies for prompt-native AIR

Out of scope:

- backend validation
- runtime enforcement outside the model session
- signed or tamper-evident contracts
- autonomous agent execution
- private AIR backend/client features
- speculative backend-connected public roadmap

## Roadmap principles

- keep the public prompt kit honest about scope
- strengthen AIR as a prompt-native runtime
- preserve map-first, active-step-only execution
- improve first-use clarity
- preserve model portability
- avoid speculative feature promises
- avoid prompt sprawl unless a profile, domain package, or method pack has concrete public value
- keep capability layers explicit, approved, validated, and routed

## Current status

### v0.1.0 - Initial public prompt runtime

Status: released

Delivered:

- AIR Core Runtime Prompt
- AIR Control Surface Prompt
- AIR Default Starter Profile
- AIR Handoff Card Template
- README for prompt-version usage
- orientation-first startup
- project execution map
- active-step-only artifact discipline
- handoff continuity

### v0.2.0 - Public prompt-kit refresh

Status: released

Delivered:

- refreshed public README and documentation
- obsolete agent-bridge material removed
- prompt-only scope clarified
- licensing and notice metadata clarified
- onboarding and ambiguity handling docs improved
- grounding profile doctrine aligned across canonical JSON and human-readable Markdown references
- workflow declaration, model portability, and handoff restoration doctrine added
- AIR Core Runtime, Control Surface, starter profile, and handoff template updated

### v0.2.1 - Deterministic onboarding and capability-layer routing patch

Status: released

Goal:

Make AIR's prompt-runtime behavior more deterministic, easier to trust across models, and clearer about when additional capability layers are needed.

Delivered:

- document deterministic onboarding non-inference
- clarify that Q1 is a branch selector, not an intent classifier
- document that Q1-D beginner orientation must return to Q1 and must not activate a project
- document capability-layer need detection
- explain specialists, domain packages, and method packs in public-facing language
- document AIR Method Layer behavior
- clarify that `AIR_ARTIFACT.method` is the default task-local procedure layer
- clarify that `AIR_METHOD_PACK` is promoted only on reuse, low variance, portability, template need, or defect history
- harden Q1-D beginner orientation ordering and first-contact tone
- rename tutorial-facing language toward beginner orientation
- require Q1-D cooperative-work framing
- require Q1-D to visibly offer an optional dynamic interactive example AIR project before returning to Q1
- update README and User Guide with the new behavior
- preserve prompt/backend claim boundaries in all documentation
- create release notes for v0.2.1

Success criteria:

- new users understand that onboarding choices cannot be guessed from the boot prompt
- README describes specialists, domain packages, and method packs without implying backend tooling
- README describes Q1-D as beginner orientation, not project activation
- Q1-D orientation explains cooperative work and optional interactive examples
- User Guide explains when AIR should request capability layers
- release notes describe the patch clearly
- no public documentation implies backend validation, runtime enforcement, signed contracts, tool execution, or autonomous agent execution

### v0.2.2 - Documentation examples and release hygiene

Status: proposed

Goal:

Turn the newly hardened onboarding behavior into easy-to-follow public examples and release hygiene.

Candidate scope:

- add a short Q1-D beginner orientation example
- add a dynamic interactive example project transcript
- add a deterministic onboarding regression example
- add a prompt-kit release checklist
- add release notes for v0.2.1
- update user guide language from tutorial to beginner orientation where needed

Success criteria:

- users can understand Q1-D without reading runtime internals
- examples demonstrate cooperative work without implying backend validation
- release checklist catches stale roadmap/README wording after prompt patches
- documentation stays prompt-native and does not imply private backend features


### v0.2.3 - Prompt runtime mechanics and usability hardening

Status: proposed

Goal:

Harden prompt-side mechanics discovered through critique review without implying backend validation.

Candidate scope:

- clarify Q1 selection detours and Q1-B import-project behavior
- add prompt-side Orbit 0 anchoring and compact benchmark visibility when material
- add capability brief permission gates with output-effect explanations
- clarify prompt-binding vs provisional workflow convention authority
- require strict JSON-only handoff output when emitting handoff cards
- bound Q1-D examples as example-project loops rather than single-feature demos
- add a minimal boot orientation header after required boot evidence
- clarify benchmark identity as a synthetic role scoped to the active step
- add visionary grounding question-loop behavior
- add regulatory pressure discovery gates

Success criteria:

- Q1 remains deterministic while allowing user questions during onboarding
- users can distinguish import from handoff continuation
- active-step anchoring is visible when drift risk is material
- capability-layer approval explains what output behavior changes
- workflow assumptions are not silently treated as binding
- handoff cards remain clean restoration objects
- Q1-D examples demonstrate the AIR loop without bloating context or implying backend features
- benchmark labels are understandable as synthetic roles rather than ordinary human job titles
- ambitious/frontier ideas are grounded through questions and kernel extraction rather than blanket rejection
- possible regulatory pressure triggers jurisdiction/data/release discovery without legal-advice claims
- all documentation preserves prompt/backend claim boundaries

## Candidate prompt-only improvements

These are concrete prompt-kit improvements that may be worth adding if they remain useful and non-speculative.

### Better examples

Possible additions:

- example new-project boot
- example Q1-D beginner orientation flow
- example dynamic interactive AIR project from Q1-D
- example deterministic onboarding correction
- example import flow
- example handoff card
- example continuation session
- example AIR help response
- example AIR compact vs verbose response
- example REVIEW_GATE and REJECT_REPORT
- example capability-layer check
- example method promotion decision

Value:

Examples make AIR easier to understand without adding new runtime claims.

### Compatibility test log

Possible additions:

- small public table of tested model behavior
- status labels for boot and handoff tests
- recommended prompt variants per model class
- known failure modes
- deterministic onboarding regression notes

Value:

This supports model portability without pretending compatibility is permanent.

### Prompt-kit release checklist

Possible additions:

- README check
- prompt file consistency check
- Q1-Q5 check
- deterministic onboarding check
- capability-layer routing check
- method-layer check
- handoff template check
- model portability note check
- claim boundary check
- mojibake/encoding check

Value:

This helps keep the public kit clean after prompt changes.

### Lightweight case studies

Possible additions:

- small project planning case
- coding-planning case
- research synthesis case
- handoff continuation case
- ambiguity handling case
- deterministic onboarding failure/regression case
- capability-layer recommendation case

Value:

Case studies demonstrate AIR behavior without requiring backend features.

### Additional specialist profiles

Possible additions only if clearly useful:

- research synthesis specialist
- technical architecture review specialist
- product strategy specialist
- documentation/rewrite specialist

Rules:

- do not add profiles just to fill the repo
- each profile must have a clear public prompt-side use case
- each profile must remain compatible with AIR Core Runtime
- each profile must preserve prompt/backend claim boundaries
- each profile should have a matching domain package only when domain facts or evidence expectations materially matter
- method packs should be promoted only after recurring procedure value is established

## Non-goals

The public prompt-version repo will not aim to:

- publish an SDK
- pretend the prompt kit is a backend runtime
- provide runtime enforcement outside the model session
- provide signed or tamper-evident artifacts
- act as an autonomous agent executor
- promise provider-independent reliability
- bloat the repo with too many profiles too early
- create method packs for one-off tasks
- replace the private backend/client implementation

## Working model

AIR should continue to operate as:

1. project activation
2. deterministic onboarding
3. project map creation
4. current active-step artifact generation
5. capability-layer need detection when material
6. review and receiver delivery
7. handoff
8. continuation

The public kit should remain useful without backend access.
